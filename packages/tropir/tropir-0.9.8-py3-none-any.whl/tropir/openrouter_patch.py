"""
OpenRouter-specific patching logic for LLM tracking.
"""

import functools
import time
import traceback
import json
import os
import uuid
import requests
from datetime import datetime
from loguru import logger

from .constants import (
    TOKEN_COUNT_KEYS,
    DEFAULT_TOKEN_COUNT
)
from .stack_tracing import format_stack_trace
from .transport import send_log
from .utils import (
    create_base_log_entry,
    create_generic_method_wrapper,
    get_user_id,
    process_template_matching,
)

def is_openrouter_url(url):
    """Check if a URL is an OpenRouter API endpoint"""
    return url and isinstance(url, str) and "openrouter.ai/api" in url

def is_openrouter_request(base_url=None, url=None, api_base=None, client=None):
    """More comprehensive check for OpenRouter requests"""
    # Check base_url parameter
    if is_openrouter_url(base_url):
        return True
        
    # Check url parameter
    if is_openrouter_url(url):
        return True
        
    # Check api_base parameter
    if is_openrouter_url(api_base):
        return True
        
    # Check client's base_url
    if client and hasattr(client, "base_url") and is_openrouter_url(client.base_url):
        return True
        
    # Check self._client.base_url if self is an object with _client attribute
    if client and hasattr(client, "_client") and hasattr(client._client, "base_url"):
        if is_openrouter_url(client._client.base_url):
            return True
            
    return False

def is_openrouter_model_format(model):
    """Check if a model string follows OpenRouter format (provider/model)"""
    if model and isinstance(model, str) and "/" in model:
        model_parts = model.split("/")
        if len(model_parts) >= 2 and model_parts[0] in ["openai", "anthropic", "google", "meta", "cohere"]:
            return True
    return False

def process_messages(messages):
    """Process OpenAI messages to handle special content types"""
    processed_messages = []
    
    # Handle single string input (responses.create input parameter)
    if isinstance(messages, str):
        return [{"role": "user", "content": messages.strip('\n')}]
    
    # Handle input parameter with instructions from responses.create
    if isinstance(messages, dict) and "input" in messages and isinstance(messages["input"], str):
        result = []
        if "instructions" in messages and messages["instructions"]:
            result.append({"role": "system", "content": messages["instructions"].strip('\n')})
        result.append({"role": "user", "content": messages["input"].strip('\n')})
        return result
        
    # Handle input list format from responses.create
    if isinstance(messages, list) and messages and isinstance(messages[0], dict) and "role" in messages[0] and "content" in messages[0]:
        result = []
        for msg in messages:
            result.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "").strip('\n') if isinstance(msg.get("content"), str) else msg.get("content")
            })
        return result
    
    # Original processing logic for standard messages format
    for msg in messages:
        if isinstance(msg, dict) or hasattr(msg, "keys"):
            # Convert frozendict to dict if needed
            msg_dict = dict(msg) if not isinstance(msg, dict) else msg
            processed_msg = msg_dict.copy()
            content = msg_dict.get("content")

            # Handle list-type content (multimodal messages)
            if isinstance(content, list):
                processed_content = []
                for item in content:
                    if isinstance(item, dict):
                        item_copy = item.copy()
                        # Handle image types in OpenAI messages
                        if "image_url" in item_copy:
                            url = item_copy["image_url"].get("url", "")
                            if url and url.startswith("data:image"):
                                item_copy["image_url"]["url"] = "[BASE64_IMAGE_REMOVED]"
                        processed_content.append(item_copy)
                    else:
                        processed_content.append(item)
                processed_msg["content"] = processed_content
            elif isinstance(content, str):
                # Strip leading and trailing newlines from string content
                processed_msg["content"] = content.strip('\n')

            processed_messages.append(processed_msg)
        else:
            # Handle non-dict message objects
            try:
                # For OpenAI message objects
                content = getattr(msg, "content", str(msg))
                if isinstance(content, str):
                    content = content.strip('\n')
                
                processed_msg = {
                    "role": getattr(msg, "role", "unknown"),
                    "content": content
                }
                
                # Add tool calls if present
                if getattr(msg, "tool_calls", None):
                    if hasattr(msg.tool_calls, "model_dump"):
                        processed_msg["tool_calls"] = [t.model_dump() for t in msg.tool_calls]
                    else:
                        # Try to extract tool calls as dictionaries
                        tool_calls = []
                        for t in msg.tool_calls:
                            if hasattr(t, "__dict__"):
                                tool_calls.append(vars(t))
                            else:
                                tool_calls.append(str(t))
                        processed_msg["tool_calls"] = tool_calls
                
                # Add tool call ID if present (for tool results)
                if getattr(msg, "tool_call_id", None):
                    processed_msg["tool_call_id"] = msg.tool_call_id
                
                # Add name if present (for functions/tools)
                if getattr(msg, "name", None):
                    processed_msg["name"] = msg.name
                
                processed_messages.append(processed_msg)
            except Exception as e:
                # If all else fails, create a basic message
                logger.warning(f"Error processing message object: {e}")
                processed_messages.append({
                    "role": getattr(msg, "role", "unknown"),
                    "content": str(getattr(msg, "content", str(msg)))
                })

    return processed_messages

def count_tokens_openrouter(text, model):
    """Count tokens in text using tiktoken for OpenRouter models"""
    try:
        import tiktoken
        # Extract the base model name from OpenRouter format (e.g., "openai/gpt-4" -> "gpt-4")
        base_model = model.split("/")[-1] if "/" in model else model
        encoding = tiktoken.encoding_for_model(base_model)
        return {
            TOKEN_COUNT_KEYS["PROMPT_TOKENS"]: len(encoding.encode(text)),
            TOKEN_COUNT_KEYS["COMPLETION_TOKENS"]: 0,
            TOKEN_COUNT_KEYS["TOTAL_TOKENS"]: len(encoding.encode(text))
        }
    except Exception as e:
        logger.warning(f"Failed to count tokens for OpenRouter: {e}")
        return DEFAULT_TOKEN_COUNT

def log_openrouter_call(provider, request_args, response, duration, success):
    """Log an OpenRouter API call according to the unified TROPIR schema."""
    try:
        # Prepend "Openrouter - " to the provider name in the response object
        if hasattr(response, 'provider'):
            response.provider = f"Openrouter - {response.provider}"
        elif isinstance(response, dict) and 'provider' in response:
            response['provider'] = f"Openrouter - {response['provider']}"
        elif hasattr(response, 'json') and callable(response.json):
            try:
                response_dict = response.json()
                if isinstance(response_dict, dict) and 'provider' in response_dict:
                    response_dict['provider'] = f"Openrouter - {response_dict['provider']}"
            except Exception:
                pass
                
        # Determine provider for the log entry
        modified_provider = provider
        
        # If we have a provider from the response, use that
        if isinstance(response, dict) and 'provider' in response:
            modified_provider = f"Openrouter - {response['provider']}"
        # Otherwise, just prepend Openrouter to whatever provider was passed in (if not already "openrouter")
        elif provider != "openrouter":
            modified_provider = f"Openrouter - {provider}"
            
        # Get stack trace for template substitutions
        stack = traceback.extract_stack()
        stack_info = format_stack_trace(stack)

        # Extract messages and model from request_args
        # request_args is a direct dictionary with model and messages
        messages = request_args.get("messages", [])
        model = request_args.get("model", "unknown")
        
        processed_messages = process_messages(messages)
        
        # Filter out any assistant messages - we only want user and system messages
        filtered_messages = [msg for msg in processed_messages if msg.get("role") != "assistant"]
        
        # Create standardized request structure
        standardized_request = {
            "model": model,
            "messages": filtered_messages,
            "temperature": request_args.get("temperature"),
            "max_tokens": request_args.get("max_tokens"),
            "top_p": request_args.get("top_p"),
            "frequency_penalty": request_args.get("frequency_penalty"),
            "presence_penalty": request_args.get("presence_penalty"),
            "stop": request_args.get("stop"),
            "n": request_args.get("n")
        }
        
        # Standardize tools format if present
        if "tools" in request_args:
            standardized_tools = []
            for tool in request_args.get("tools", []):
                if "function" in tool:
                    function = tool["function"]
                    standardized_tool = {
                        "name": function.get("name", ""),
                        "description": function.get("description", ""),
                        "parameters": function.get("parameters", {})
                    }
                    standardized_tools.append(standardized_tool)
            
            if standardized_tools:
                standardized_request["tools"] = standardized_tools
                
        # Add tool_choice if specified
        if "tool_choice" in request_args:
            standardized_request["tool_choice"] = request_args["tool_choice"]
        
        # Extract response text and usage from response
        response_text = ""
        usage = {}
        function_call_info = None
        
        # Handle different response types
        try:
            # First try to handle as OpenAI SDK response
            if hasattr(response, "choices") or hasattr(response, "model_dump") or hasattr(response, "to_dict"):
                # Convert response to dictionary if possible
                if hasattr(response, "model_dump"):
                    response_dict = response.model_dump()
                elif hasattr(response, "to_dict"):
                    response_dict = response.to_dict()
                else:
                    response_dict = vars(response)
                
                logger.debug(f"Response dict: {response_dict}")
                
                # Extract response text from choices
                if "choices" in response_dict and response_dict["choices"]:
                    choice = response_dict["choices"][0]
                    if "message" in choice:
                        message = choice["message"]
                        if "content" in message:
                            response_text = message["content"]
                        
                        # Handle tool calls
                        if "tool_calls" in message and message["tool_calls"]:
                            tool_calls = []
                            for tool_call in message["tool_calls"]:
                                if "function" in tool_call:
                                    function = tool_call["function"]
                                    tool_calls.append({
                                        "id": tool_call.get("id", str(uuid.uuid4())),
                                        "type": "function",
                                        "function": {
                                            "name": function.get("name", "unknown"),
                                            "arguments": function.get("arguments", "{}")
                                        }
                                    })
                            
                            if tool_calls:
                                function_call_info = {
                                    "calls": tool_calls
                                }
                                
                                # If we didn't get any content text, create a placeholder
                                if not response_text:
                                    response_text = f"[TOOL_CALLS: {len(tool_calls)}]"
                
                # Extract usage information
                if "usage" in response_dict:
                    usage = response_dict["usage"]
            
            # If not an SDK response, try as HTTP response
            elif hasattr(response, "json") and callable(response.json):
                response_dict = response.json()
                # Extract response text from choices
                if "choices" in response_dict and response_dict["choices"]:
                    choice = response_dict["choices"][0]
                    if "message" in choice and "content" in choice["message"]:
                        response_text = choice["message"]["content"]
                
                # Extract usage information
                if "usage" in response_dict:
                    usage = response_dict["usage"]
            
        except Exception as e:
            logger.error(f"Error processing response: {e}")
            logger.error(f"Response type: {type(response)}")
            logger.error(f"Response dir: {dir(response)}")
            logger.error(f"Response repr: {repr(response)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            response_text = f"[ERROR_PROCESSING_RESPONSE: {str(e)}]"
        
        # Count tokens if not provided
        if not usage:
            prompt_text = " ".join(str(msg.get("content", "")) for msg in processed_messages if msg.get("content"))
            resp_text_str = str(response_text) if response_text else ""
            usage = count_tokens_openrouter(prompt_text + resp_text_str, standardized_request["model"])
        
        # Standardize the usage structure with token_details
        standardized_usage = {
            "prompt_tokens": usage.get("prompt_tokens", 0),
            "completion_tokens": usage.get("completion_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0),
            "token_details": {
                "cached_tokens": None,
                "audio_tokens": None,
                "reasoning_tokens": None,
                "accepted_prediction_tokens": None,
                "rejected_prediction_tokens": None
            }
        }

        # Only try to get details if they exist
        if usage and isinstance(usage, dict):
            prompt_details = usage.get("prompt_tokens_details", {}) or {}
            completion_details = usage.get("completion_tokens_details", {}) or {}
            
            if isinstance(prompt_details, dict):
                standardized_usage["token_details"]["cached_tokens"] = prompt_details.get("cached_tokens")
                standardized_usage["token_details"]["audio_tokens"] = prompt_details.get("audio_tokens")
            
            if isinstance(completion_details, dict):
                standardized_usage["token_details"]["reasoning_tokens"] = completion_details.get("reasoning_tokens")
                standardized_usage["token_details"]["accepted_prediction_tokens"] = completion_details.get("accepted_prediction_tokens")
                standardized_usage["token_details"]["rejected_prediction_tokens"] = completion_details.get("rejected_prediction_tokens")
                
                # If we have audio tokens in completion details, add them to any existing audio tokens
                if completion_details.get("audio_tokens") is not None:
                    if standardized_usage["token_details"]["audio_tokens"] is None:
                        standardized_usage["token_details"]["audio_tokens"] = 0
                    standardized_usage["token_details"]["audio_tokens"] += completion_details["audio_tokens"]

        # Generate log entry with standardized request
        log_entry = create_base_log_entry(modified_provider, standardized_request)
        
        # Add remaining fields
        log_entry.update({
            "response": response_text,
            "usage": standardized_usage,
            "duration": duration,
            "success": success,
        })
        
        # Convert function_call to tool_calls format with parsed arguments
        if function_call_info:
            parsed_arguments = {}
            
            # Try to parse arguments from any tool calls
            for call in function_call_info.get("calls", []):
                if "function" in call and "arguments" in call["function"]:
                    try:
                        args_json = call["function"]["arguments"]
                        parsed_args = json.loads(args_json)
                        # If this is the first tool call, use its parsed arguments
                        if not parsed_arguments:
                            parsed_arguments = parsed_args
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {args_json}")
            
            log_entry["tool_calls"] = {
                "calls": function_call_info.get("calls", []),
                "parsed_arguments": parsed_arguments
            }
        
        # Remove any leftover function_call field if it exists (to be consistent with schema)
        if "function_call" in log_entry:
            del log_entry["function_call"]
        
        # Get user_id from API
        user_id = get_user_id()
        if user_id:
            log_entry["user_id"] = user_id

        # Call template matching API with filtered messages (only user messages)
        # to avoid assistant_0, assistant_1, etc. in the template_substitutions
        filtered_for_template = [msg for msg in processed_messages if msg.get("role") != "assistant"]
        log_entry = process_template_matching(filtered_for_template, user_id, stack_info, log_entry)
                
        # Write to log file
        send_log(log_entry)
        logger.debug(f"Successfully logged OpenRouter call for model: {standardized_request['model']}")

    except Exception as e:
        logger.error(f"Error logging OpenRouter call: {str(e)}")
        logger.error(traceback.format_exc())

def patched_requests_post(original_post, *args, **kwargs):
    """
    Patched version of requests.post to track direct HTTP calls to OpenRouter API.
    """
    url = args[0] if args else kwargs.get('url')
    
    # Only process OpenRouter API calls
    if url and isinstance(url, str) and "openrouter.ai/api" in url:
        try:
            start_time = time.time()
            success = True
            
            # Get the request data from the data parameter
            request_data = {}
            if 'data' in kwargs:
                try:
                    request_data = json.loads(kwargs['data'])
                except (json.JSONDecodeError, TypeError):
                    request_data = {}
            
            # Make the actual request
            try:
                response = original_post(*args, **kwargs)
            except Exception as e:
                success = False
                response = None
                logger.error(f"Error making OpenRouter HTTP request: {str(e)}")
                raise e
            finally:
                duration = time.time() - start_time
                
                # Only log if this is a chat completion or similar endpoint
                if "chat/completions" in url or "completions" in url:
                    # Log the API call
                    logger.debug(f"Logging direct OpenRouter API call to {url}")
                    log_openrouter_call("openrouter", request_data, response, duration, success)
            
            return response
            
        except Exception as e:
            logger.error(f"Error in patched requests.post: {str(e)}")
            logger.error(traceback.format_exc())
            # Let the original request proceed even if tracking fails
            return original_post(*args, **kwargs)
    else:
        # For non-OpenRouter URLs, just call the original function
        return original_post(*args, **kwargs)

def patch_openai_client_init():
    """Patch the OpenAI client initialization to detect OpenRouter base URLs"""
    try:
        from openai import OpenAI
        
        # Store the original __init__ method
        original_init = OpenAI.__init__
        
        @functools.wraps(original_init)
        def patched_init(self, *args, **kwargs):
            # Call the original __init__
            original_init(self, *args, **kwargs)
            
            # Check if this client is configured for OpenRouter
            if "base_url" in kwargs and is_openrouter_url(kwargs["base_url"]):
                # Mark this client as an OpenRouter client
                logger.debug(f"OpenAI client initialized with OpenRouter base_url: {kwargs['base_url']}")
                setattr(self, "_is_openrouter_client", True)
        
        # Apply the patch
        OpenAI.__init__ = patched_init
        logger.info("Successfully patched OpenAI client initialization for OpenRouter detection")
    
    except ImportError:
        logger.warning("Could not import OpenAI. Client initialization patching skipped.")
    except Exception as e:
        logger.error(f"Failed to patch OpenAI client initialization: {e}")
        logger.error(traceback.format_exc())

def setup_openrouter_patching():
    """Set up tracking for OpenRouter by patching target methods."""
    try:
        # Patch requests.post for direct API calls
        if not getattr(requests.post, '_openrouter_patched', False):
            original_post = requests.post
            patched_post = functools.wraps(original_post)(
                lambda *args, **kwargs: patched_requests_post(original_post, *args, **kwargs)
            )
            patched_post._openrouter_patched = True
            requests.post = patched_post
            logger.info("Successfully patched requests.post for OpenRouter API tracking")

        # Patch the OpenAI client initialization
        patch_openai_client_init()
            
        # Import the specific class where the 'create' method resides
        from openai.resources.chat.completions import Completions as OpenAICompletions

        # Check if the 'create' method exists and hasn't been patched yet
        if hasattr(OpenAICompletions, "create") and not getattr(OpenAICompletions.create, '_openrouter_patched', False):
            original_create_method = OpenAICompletions.create  # Get the original function

            # Create a wrapper that checks if this is an OpenRouter request
            @functools.wraps(original_create_method)
            def patched_create_method(self, *args, **kwargs):
                # Check if the client is configured for OpenRouter
                base_url = getattr(self._client, "base_url", None)
                client_is_openrouter = getattr(self._client, "_is_openrouter_client", False) or is_openrouter_url(base_url)
                
                # Check for OpenRouter model format
                model_is_openrouter = False
                if "model" in kwargs and is_openrouter_model_format(kwargs["model"]):
                    model_is_openrouter = True
                
                # If this looks like an OpenRouter call, track it as such
                if client_is_openrouter or model_is_openrouter:
                    start_time = time.time()
                    success = True
                    try:
                        response = original_create_method(self, *args, **kwargs)
                    except Exception as e:
                        success = False
                        response = None
                        logger.error(f"Error in OpenRouter call: {str(e)}")
                        raise e
                    finally:
                        duration = time.time() - start_time
                        logger.debug(f"Logging OpenRouter call via OpenAI SDK - model: {kwargs.get('model', 'unknown')}, base_url: {base_url}")
                        log_openrouter_call("openrouter", kwargs, response, duration, success)
                    return response
                
                # For non-OpenRouter requests, let the original method handle it
                return original_create_method(self, *args, **kwargs)

            # Replace the original method with the patched one
            OpenAICompletions.create = patched_create_method
            OpenAICompletions.create._openrouter_patched = True
            logger.info("Successfully patched OpenAI Completions.create for OpenRouter tracking")

        # Patch the responses methods
        try:
            from openai.resources.responses import Responses as OpenAIResponses
            
            # Patch synchronous Responses methods
            methods_to_patch = ['create', 'stream', 'parse', 'retrieve', 'delete']
            
            for method_name in methods_to_patch:
                if hasattr(OpenAIResponses, method_name) and not getattr(getattr(OpenAIResponses, method_name), '_openrouter_patched', False):
                    original_method = getattr(OpenAIResponses, method_name)
                    
                    # Create patched version that handles OpenRouter requests
                    @functools.wraps(original_method)
                    def patched_method(self, *args, **kwargs):
                        # Check if the client is configured for OpenRouter
                        base_url = getattr(self._client, "base_url", None)
                        client_is_openrouter = getattr(self._client, "_is_openrouter_client", False) or is_openrouter_url(base_url)
                        
                        # Check for OpenRouter model format
                        model_is_openrouter = False
                        if "model" in kwargs and is_openrouter_model_format(kwargs["model"]):
                            model_is_openrouter = True
                        
                        # If this looks like an OpenRouter call, track it as such
                        if client_is_openrouter or model_is_openrouter:
                            start_time = time.time()
                            success = True
                            try:
                                response = original_method(self, *args, **kwargs)
                            except Exception as e:
                                success = False
                                response = None
                                logger.error(f"Error in OpenRouter {method_name} call: {str(e)}")
                                raise e
                            finally:
                                duration = time.time() - start_time
                                logger.debug(f"Logging OpenRouter {method_name} call via OpenAI SDK")
                                log_openrouter_call("openrouter", kwargs, response, duration, success)
                            return response
                        
                        # For non-OpenRouter requests, let the original method handle it
                        return original_method(self, *args, **kwargs)
                    
                    # Set the method with the patched version
                    setattr(OpenAIResponses, method_name, patched_method)
                    getattr(OpenAIResponses, method_name)._openrouter_patched = True
            
            logger.info("Successfully patched OpenAI Responses methods for OpenRouter tracking")
                    
        except ImportError:
            logger.warning("Could not import OpenAI responses classes. OpenRouter responses tracking may not work.")
        except Exception as e:
            logger.error(f"Failed during OpenRouter responses patching: {e}")
            logger.error(traceback.format_exc())

    except ImportError:
        logger.warning("Could not import 'openai.resources.chat.completions.Completions'. OpenRouter tracking may not work.")
    except Exception as e:
        logger.error(f"Failed during OpenRouter patching process: {e}")
        logger.error(traceback.format_exc()) 