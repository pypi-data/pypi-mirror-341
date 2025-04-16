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

def process_openrouter_messages(messages):
    """Process OpenRouter messages to handle special content types"""
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
    
    # Process each message
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
                        # Handle image types in messages
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
                # For message objects with attributes
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
    """Count tokens in text for OpenRouter models"""
    try:
        import tiktoken
        
        # Extract the model name from the OpenRouter format (provider/model)
        model_name = model.split('/')[-1] if '/' in model else model
        
        # For Claude models
        if model_name.startswith("claude"):
            # Claude models use roughly ~4 characters per token on average
            approx_tokens = len(text) // 4
            return {
                TOKEN_COUNT_KEYS["PROMPT_TOKENS"]: approx_tokens,
                TOKEN_COUNT_KEYS["COMPLETION_TOKENS"]: 0,
                TOKEN_COUNT_KEYS["TOTAL_TOKENS"]: approx_tokens
            }
        
        # For other models, try to use tiktoken
        try:
            encoding = tiktoken.encoding_for_model(model_name)
            return {
                TOKEN_COUNT_KEYS["PROMPT_TOKENS"]: len(encoding.encode(text)),
                TOKEN_COUNT_KEYS["COMPLETION_TOKENS"]: 0,
                TOKEN_COUNT_KEYS["TOTAL_TOKENS"]: len(encoding.encode(text))
            }
        except KeyError:
            # Fallback to general purpose encoding if model specific is not available
            encoding = tiktoken.get_encoding("cl100k_base")  # General encoding that works for many models
            return {
                TOKEN_COUNT_KEYS["PROMPT_TOKENS"]: len(encoding.encode(text)),
                TOKEN_COUNT_KEYS["COMPLETION_TOKENS"]: 0,
                TOKEN_COUNT_KEYS["TOTAL_TOKENS"]: len(encoding.encode(text))
            }
    except Exception as e:
        logger.warning(f"Failed to count tokens for OpenRouter: {e}")
        return DEFAULT_TOKEN_COUNT

def extract_openai_sdk_response_content(response):
    """Extract content from OpenAI SDK response objects"""
    try:
        # For modern OpenAI SDK responses
        if hasattr(response, "choices") and len(response.choices) > 0:
            choice = response.choices[0]
            if hasattr(choice, "message") and hasattr(choice.message, "content"):
                return choice.message.content or ""
    except Exception as e:
        logger.error(f"Error extracting content from SDK response: {e}")
    return ""

def extract_tool_calls_from_sdk_response(response):
    """Extract tool calls from OpenAI SDK response objects"""
    try:
        if hasattr(response, "choices") and len(response.choices) > 0:
            choice = response.choices[0]
            if hasattr(choice, "message") and hasattr(choice.message, "tool_calls"):
                tool_calls = choice.message.tool_calls
                if tool_calls:
                    tool_call_details = []
                    parsed_args_combined = {}
                    
                    for tool in tool_calls:
                        if hasattr(tool, "function"):
                            args_str = tool.function.arguments if hasattr(tool.function, "arguments") else "{}"
                            
                            try:
                                args_obj = json.loads(args_str) if isinstance(args_str, str) else {}
                                if not parsed_args_combined or len(args_obj) > len(parsed_args_combined):
                                    parsed_args_combined = args_obj
                            except Exception:
                                pass
                                
                            tool_details = {
                                "id": tool.id if hasattr(tool, "id") else f"call_{uuid.uuid4().hex[:8]}",
                                "type": "function",
                                "function": {
                                    "name": tool.function.name if hasattr(tool.function, "name") else "unknown_function",
                                    "arguments": args_str
                                }
                            }
                            tool_call_details.append(tool_details)
                    
                    if tool_call_details:
                        return {
                            "calls": tool_call_details,
                            "parsed_arguments": parsed_args_combined
                        }
    except Exception as e:
        logger.error(f"Error extracting tool calls from SDK response: {e}")
        logger.error(traceback.format_exc())
    
    return None

def create_safe_token_details(usage):
    """Create a standardized token_details structure from usage data, handling nulls safely"""
    if not usage:
        return {
            "cached_tokens": None,
            "audio_tokens": None,
            "reasoning_tokens": None,
            "accepted_prediction_tokens": None,
            "rejected_prediction_tokens": None
        }
    
    # Safely get nested values
    prompt_tokens_details = usage.get("prompt_tokens_details", {}) or {}
    completion_tokens_details = usage.get("completion_tokens_details", {}) or {}
    
    # Avoid NoneType errors by using empty dict as fallback
    if prompt_tokens_details is None:
        prompt_tokens_details = {}
    if completion_tokens_details is None:
        completion_tokens_details = {}
    
    # Extract values with safe fallbacks
    cached_tokens = prompt_tokens_details.get("cached_tokens") if isinstance(prompt_tokens_details, dict) else None
    
    # Get audio tokens safely
    prompt_audio = prompt_tokens_details.get("audio_tokens", 0) if isinstance(prompt_tokens_details, dict) else 0
    completion_audio = completion_tokens_details.get("audio_tokens", 0) if isinstance(completion_tokens_details, dict) else 0
    audio_tokens = (prompt_audio + completion_audio) or None
    
    # Get other token details
    reasoning_tokens = completion_tokens_details.get("reasoning_tokens") if isinstance(completion_tokens_details, dict) else None
    accepted_tokens = completion_tokens_details.get("accepted_prediction_tokens") if isinstance(completion_tokens_details, dict) else None
    rejected_tokens = completion_tokens_details.get("rejected_prediction_tokens") if isinstance(completion_tokens_details, dict) else None
    
    return {
        "cached_tokens": cached_tokens,
        "audio_tokens": audio_tokens,
        "reasoning_tokens": reasoning_tokens,
        "accepted_prediction_tokens": accepted_tokens,
        "rejected_prediction_tokens": rejected_tokens
    }

def log_openrouter_call(provider, request_args, response, duration, success):
    """Log an OpenRouter API call according to the unified TROPIR schema."""
    try:
        # Always set provider to "openrouter" regardless of what was passed
        provider = "openrouter"
        
        # Get stack trace for template substitutions
        stack = traceback.extract_stack()
        stack_info = format_stack_trace(stack)

        # Extract messages from request_args
        messages = request_args.get("messages", [])
        processed_messages = process_openrouter_messages(messages)
        
        # Create standardized request structure
        standardized_request = {
            "model": request_args.get("model", "unknown"),
            "messages": processed_messages,
            "temperature": request_args.get("temperature"),
            "max_tokens": request_args.get("max_tokens"),
            "top_p": request_args.get("top_p"),
            "frequency_penalty": request_args.get("frequency_penalty"),
            "presence_penalty": request_args.get("presence_penalty"),
            "stop": request_args.get("stop"),
            "n": request_args.get("n")
        }
        
        # Standardize tools format if present
        tools = []
        
        # Check if this is a function/tool call request
        if "functions" in request_args:
            for func in request_args.get("functions", []):
                standardized_tool = {
                    "name": func.get("name", ""),
                    "description": func.get("description", ""),
                    "parameters": func.get("parameters", {})
                }
                tools.append(standardized_tool)
                
            # Add tool_choice if function_call was specified
            if "function_call" in request_args:
                if isinstance(request_args["function_call"], dict):
                    standardized_request["tool_choice"] = {
                        "type": "function",
                        "function": {
                            "name": request_args["function_call"].get("name", "auto")
                        }
                    }
                else:
                    standardized_request["tool_choice"] = request_args["function_call"]
                    
        # Process tools field if it exists
        elif "tools" in request_args:
            tools = request_args.get("tools", [])
            if "tool_choice" in request_args:
                standardized_request["tool_choice"] = request_args["tool_choice"]
                
        # Add tools to request if we have any
        if tools:
            standardized_request["tools"] = tools

        response_text = ""
        usage = {}
        function_call_info = None
        model = standardized_request.get("model", "unknown")
        
        # Process response based on type
        if success and response:
            # Handle modern SDK response objects - direct extraction
            tool_calls = extract_tool_calls_from_sdk_response(response)
            if tool_calls:
                function_call_info = tool_calls
                response_text = f"[TOOL_CALLS: {len(tool_calls['calls'])}]"
            else:
                # Try to extract content directly from SDK response
                sdk_content = extract_openai_sdk_response_content(response)
                if sdk_content:
                    response_text = sdk_content
            
            # Extract usage from SDK response
            if hasattr(response, "usage"):
                usage = {
                    "prompt_tokens": getattr(response.usage, "prompt_tokens", 0),
                    "completion_tokens": getattr(response.usage, "completion_tokens", 0),
                    "total_tokens": getattr(response.usage, "total_tokens", 0)
                }
            
            # If we still don't have content, try various response formats
            if not response_text:
                # Try to handle response as dictionary or JSON
                response_dict = None
                
                # Convert response to dictionary if possible
                if hasattr(response, "model_dump"):
                    try:
                        response_dict = response.model_dump()
                    except Exception as e:
                        logger.debug(f"Error in model_dump: {e}")
                elif isinstance(response, dict):
                    response_dict = response
                elif hasattr(response, "json") and callable(response.json):
                    try:
                        response_dict = response.json()
                    except Exception as e:
                        logger.debug(f"Error in json(): {e}")
                
                # Process dictionary response
                if response_dict and isinstance(response_dict, dict):
                    # Extract response text from choices
                    if "choices" in response_dict and response_dict["choices"]:
                        choice = response_dict["choices"][0]
                        
                        if isinstance(choice, dict) and "message" in choice and choice["message"]:
                            message = choice["message"]
                            
                            # Get content if available
                            if "content" in message and message["content"] is not None:
                                response_text = message["content"]
                            
                            # Check for tool calls
                            if "tool_calls" in message and message["tool_calls"]:
                                tool_calls = message["tool_calls"]
                                tool_call_details = []
                                parsed_args_combined = {}
                                
                                for tool in tool_calls:
                                    if isinstance(tool, dict) and "function" in tool and isinstance(tool["function"], dict):
                                        tool_details = {
                                            "id": tool.get("id", f"call_{uuid.uuid4().hex[:8]}"),
                                            "type": tool.get("type", "function"),
                                            "function": {
                                                "name": tool["function"].get("name", "unknown_function"),
                                                "arguments": tool["function"].get("arguments", "{}")
                                            }
                                        }
                                        
                                        # Try to parse arguments
                                        try:
                                            args_str = tool_details["function"]["arguments"]
                                            args_obj = json.loads(args_str) if isinstance(args_str, str) else {}
                                            if not parsed_args_combined or len(args_obj) > len(parsed_args_combined):
                                                parsed_args_combined = args_obj
                                        except Exception:
                                            pass
                                            
                                        tool_call_details.append(tool_details)
                                
                                if tool_call_details:
                                    # Store all tool calls
                                    function_call_info = {
                                        "calls": tool_call_details,
                                        "parsed_arguments": parsed_args_combined
                                    }
                                    
                                    # Format response text if content was None
                                    if not response_text:
                                        response_text = f"[TOOL_CALLS: {len(tool_calls)}]"
                    
                    # Extract usage information if available
                    if "usage" in response_dict and isinstance(response_dict["usage"], dict):
                        usage = response_dict["usage"]

        # If still no response text, mark as unknown
        if not response_text:
            response_text = "[UNKNOWN_RESPONSE_FORMAT]"

        # Count tokens if not provided
        if not usage:
            prompt_text = " ".join(str(msg.get("content", "")) for msg in processed_messages if msg.get("content"))
            resp_text_str = str(response_text) if response_text else ""
            usage = count_tokens_openrouter(prompt_text + resp_text_str, model)
        
        # Standardize the usage structure with token_details - safely handle nulls
        standardized_usage = {
            "prompt_tokens": usage.get("prompt_tokens", 0),
            "completion_tokens": usage.get("completion_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0),
            "token_details": create_safe_token_details(usage)
        }

        # Generate log entry with standardized request
        log_entry = create_base_log_entry(provider, standardized_request)
        
        # Add remaining fields
        log_entry.update({
            "response": response_text,
            "usage": standardized_usage,
            "duration": duration,
            "success": success,
            "provider": provider,  # Explicitly set provider again to ensure it's correct
        })
        
        # Add tool_calls field if we have function call information
        if function_call_info:
            log_entry["tool_calls"] = function_call_info
        
        # Remove any existing function_call field to adhere to schema
        if "function_call" in log_entry:
            del log_entry["function_call"]
        
        # Remove functions_info field from request if it exists
        if "functions_info" in log_entry["request"]:
            del log_entry["request"]["functions_info"]
        
        # Get user_id from API
        user_id = get_user_id()
        if user_id:
            log_entry["user_id"] = user_id

        # Call template matching API and update log entry
        log_entry = process_template_matching(processed_messages, user_id, stack_info, log_entry)
        
        # Final check to ensure provider is set to "openrouter"
        log_entry["provider"] = "openrouter"
                
        # Write to log file
        send_log(log_entry)

    except Exception as e:
        logger.error(f"Error logging OpenRouter call: {str(e)}")
        logger.error(traceback.format_exc())

def is_openrouter_url(url):
    """Check if a URL is an OpenRouter API endpoint"""
    return url and isinstance(url, str) and "openrouter.ai/api" in url

def is_openrouter_completion(url):
    """Check if a URL is an OpenRouter completion endpoint"""
    return is_openrouter_url(url) and ("/completions" in url or "/chat/completions" in url)

def force_openrouter_provider(wrapped_function):
    """Decorator to ensure the provider is always 'openrouter' for any OpenRouter API calls"""
    @functools.wraps(wrapped_function)
    def wrapper(*args, **kwargs):
        # Always pass "openrouter" as the provider
        args = list(args)
        if len(args) > 0:
            args[0] = "openrouter"  # First arg is provider
        return wrapped_function(*args, **kwargs)
    return wrapper

def patched_openai_request(original_function, *args, **kwargs):
    """Patched version of OpenAI request method when used with OpenRouter"""
    # Check if this is an OpenRouter API call
    base_url = kwargs.get("base_url", "")
    url = kwargs.get("url", "")
    
    if is_openrouter_url(base_url) or is_openrouter_url(url):
        start_time = time.time()
        success = True
        
        try:
            response = original_function(*args, **kwargs)
        except Exception as e:
            success = False
            response = None
            logger.error(f"Error making OpenRouter API call via OpenAI SDK: {str(e)}")
            raise e
        finally:
            duration = time.time() - start_time
            
            # Only log completions endpoints
            if is_openrouter_completion(url) or (is_openrouter_url(base_url) and "/completions" in url):
                # Extract request data
                # The json payload is usually in the "json" kwarg
                request_data = kwargs.get("json", {})
                
                # Log the API call with explicit provider="openrouter"
                log_openrouter_call("openrouter", request_data, response, duration, success)
                
        return response
    else:
        # Not an OpenRouter call, just pass through
        return original_function(*args, **kwargs)
        
def patched_requests_post(original_post, *args, **kwargs):
    """
    Patched version of requests.post to track direct HTTP calls to OpenRouter API.
    """
    url = args[0] if args else kwargs.get('url')
    
    # Only process OpenRouter API calls
    if is_openrouter_url(url):
        start_time = time.time()
        success = True
        
        # Get the request data
        json_data = kwargs.get('json', {})
        
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
            if is_openrouter_completion(url):
                # Log the API call with explicit provider="openrouter"
                log_openrouter_call("openrouter", json_data, response, duration, success)
                
        return response
    else:
        # For non-OpenRouter URLs, just call the original function
        return original_post(*args, **kwargs)

def intercept_openai_client_calls(self, original_create, *args, **kwargs):
    """Intercept OpenAI client create calls when used with OpenRouter base URL"""
    start_time = time.time()
    success = True
    
    try:
        response = original_create(*args, **kwargs)
    except Exception as e:
        success = False
        response = None
        logger.error(f"Error in OpenRouter client call: {str(e)}")
        raise e
    finally:
        duration = time.time() - start_time
        # Ensure provider is set to "openrouter"
        log_openrouter_call("openrouter", kwargs, response, duration, success)
        
    return response

def setup_openrouter_patching():
    """Set up tracking for OpenRouter by patching target methods."""
    try:
        # Import the necessary classes from OpenAI SDK
        try:
            # For newer OpenAI SDK versions
            from openai.resources.chat.completions import Completions as OpenAICompletions
            from openai._base_client import APIRequestor

            # Check if the 'create' method exists and hasn't been patched yet
            if hasattr(OpenAICompletions, "create") and not getattr(OpenAICompletions.create, '_openrouter_tracker_patched', False):
                original_create_method = OpenAICompletions.create

                # Create a wrapped version specifically for OpenRouter
                @functools.wraps(original_create_method)
                def openrouter_aware_create(self, *args, **kwargs):
                    # First check if base_url is in the client object
                    base_url = getattr(self._client, "base_url", None)
                    
                    if (base_url and is_openrouter_url(base_url)) or ('api_base' in kwargs and is_openrouter_url(kwargs['api_base'])):
                        return intercept_openai_client_calls(self, original_create_method, *args, **kwargs)
                    else:
                        # Regular OpenAI call, let it proceed normally
                        return original_create_method(self, *args, **kwargs)
                
                # Replace the original method
                OpenAICompletions.create = openrouter_aware_create
                OpenAICompletions.create._openrouter_tracker_patched = True
                logger.info("Patched OpenAI Completions.create for OpenRouter tracking")
                
            # Try to patch APIRequestor for more general coverage
            if hasattr(APIRequestor, "request") and not getattr(APIRequestor.request, '_openrouter_tracker_patched', False):
                original_request = APIRequestor.request
                patched_request = functools.wraps(original_request)(
                    lambda self, *args, **kwargs: patched_openai_request(original_request, self, *args, **kwargs)
                )
                patched_request._openrouter_tracker_patched = True
                APIRequestor.request = patched_request
                logger.info("Patched OpenAI APIRequestor.request for OpenRouter tracking")
                
        except ImportError:
            logger.warning("Could not import 'openai.resources.chat.completions'. Trying legacy approach.")
            
            # Try legacy approach for older OpenAI SDK versions
            try:
                import openai
                
                # Check if the ChatCompletion class exists (v0.x)
                if hasattr(openai, "ChatCompletion") and hasattr(openai.ChatCompletion, "create"):
                    original_create = openai.ChatCompletion.create
                    
                    if not getattr(original_create, '_openrouter_tracker_patched', False):
                        # Create patch for ChatCompletion.create
                        @functools.wraps(original_create)
                        def patched_chat_completion_create(*args, **kwargs):
                            if 'api_base' in kwargs and is_openrouter_url(kwargs['api_base']):
                                start_time = time.time()
                                success = True
                                
                                try:
                                    response = original_create(*args, **kwargs)
                                except Exception as e:
                                    success = False
                                    response = None
                                    logger.error(f"Error in legacy OpenRouter-via-OpenAI call: {str(e)}")
                                    raise e
                                finally:
                                    duration = time.time() - start_time
                                    # Use explicit provider="openrouter"
                                    log_openrouter_call("openrouter", kwargs, response, duration, success)
                                    
                                return response
                            else:
                                return original_create(*args, **kwargs)
                        
                        # Apply the patch
                        openai.ChatCompletion.create = patched_chat_completion_create
                        openai.ChatCompletion.create._openrouter_tracker_patched = True
                        logger.info("Patched legacy OpenAI ChatCompletion.create for OpenRouter tracking")
                        
                # Also check and patch Completion for non-chat completions
                if hasattr(openai, "Completion") and hasattr(openai.Completion, "create"):
                    original_completion_create = openai.Completion.create
                    
                    if not getattr(original_completion_create, '_openrouter_tracker_patched', False):
                        # Create patch for Completion.create
                        @functools.wraps(original_completion_create)
                        def patched_completion_create(*args, **kwargs):
                            if 'api_base' in kwargs and is_openrouter_url(kwargs['api_base']):
                                start_time = time.time()
                                success = True
                                
                                try:
                                    response = original_completion_create(*args, **kwargs)
                                except Exception as e:
                                    success = False
                                    response = None
                                    logger.error(f"Error in legacy OpenRouter-via-OpenAI Completion call: {str(e)}")
                                    raise e
                                finally:
                                    duration = time.time() - start_time
                                    # Convert prompt to messages format for consistency
                                    prompt = kwargs.get("prompt", "")
                                    if isinstance(prompt, str):
                                        kwargs["messages"] = [{"role": "user", "content": prompt}]
                                    # Use explicit provider="openrouter"
                                    log_openrouter_call("openrouter", kwargs, response, duration, success)
                                    
                                return response
                            else:
                                return original_completion_create(*args, **kwargs)
                        
                        # Apply the patch
                        openai.Completion.create = patched_completion_create
                        openai.Completion.create._openrouter_tracker_patched = True
                        logger.info("Patched legacy OpenAI Completion.create for OpenRouter tracking")
            except ImportError:
                logger.warning("Could not import 'openai'. OpenRouter tracking via OpenAI SDK may not work.")
            except Exception as e:
                logger.error(f"Failed during legacy OpenAI patching for OpenRouter: {e}")
                logger.error(traceback.format_exc())

        # Check for OpenAI v1+ client
        try:
            from openai import OpenAI
            original_init = OpenAI.__init__
            
            if not getattr(original_init, '_openrouter_tracker_patched', False):
                @functools.wraps(original_init)
                def patched_init(self, *args, **kwargs):
                    # Call original init
                    original_init(self, *args, **kwargs)
                    
                    # Check if this is an OpenRouter client
                    base_url = kwargs.get("base_url", "")
                    if is_openrouter_url(base_url):
                        # This is an OpenRouter client
                        logger.info(f"Detected OpenRouter client initialization with base_url: {base_url}")
                        
                        # We need to hook the completions.create method
                        if hasattr(self, "chat") and hasattr(self.chat, "completions") and hasattr(self.chat.completions, "create"):
                            original_completions_create = self.chat.completions.create
                            
                            if not getattr(original_completions_create, '_openrouter_tracker_patched', False):
                                @functools.wraps(original_completions_create)
                                def patched_completions_create(*args, **kwargs):
                                    start_time = time.time()
                                    success = True
                                    
                                    try:
                                        response = original_completions_create(*args, **kwargs)
                                    except Exception as e:
                                        success = False
                                        response = None
                                        logger.error(f"Error in OpenRouter client chat.completions.create: {str(e)}")
                                        raise e
                                    finally:
                                        duration = time.time() - start_time
                                        # Use explicit provider="openrouter"
                                        log_openrouter_call("openrouter", kwargs, response, duration, success)
                                        
                                    return response
                                
                                # Apply patch
                                patched_completions_create._openrouter_tracker_patched = True
                                self.chat.completions.create = patched_completions_create
                                logger.info("Patched OpenAI client chat.completions.create for OpenRouter")
                
                # Apply the init patch
                OpenAI.__init__ = patched_init
                OpenAI.__init__._openrouter_tracker_patched = True
                logger.info("Patched OpenAI client initialization for OpenRouter tracking")
        except ImportError:
            logger.warning("Could not import OpenAI client class. Some tracking may not work.")
        except Exception as e:
            logger.error(f"Failed to patch OpenAI client class: {e}")
            logger.error(traceback.format_exc())

        # Patch requests.post for direct HTTP API calls if not already patched
        if not getattr(requests.post, '_llm_tracker_patched', False):
            original_post = requests.post
            patched_post = functools.wraps(original_post)(
                lambda *args, **kwargs: patched_requests_post(original_post, *args, **kwargs)
            )
            patched_post._llm_tracker_patched = True
            patched_post._openrouter_tracker_patched = True
            requests.post = patched_post
            logger.info("Successfully patched requests.post for OpenRouter API tracking")
        elif not getattr(requests.post, '_openrouter_tracker_patched', False):
            # If already patched by another module, we need to chain our patch
            original_post = requests.post
            
            # Define a function that checks specifically for OpenRouter
            @functools.wraps(original_post)
            def openrouter_patched_post(*args, **kwargs):
                url = args[0] if args else kwargs.get('url')
                
                # Check if this is an OpenRouter call
                if is_openrouter_url(url):
                    start_time = time.time()
                    success = True
                    
                    # Get the request data
                    json_data = kwargs.get('json', {})
                    
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
                        if is_openrouter_completion(url):
                            # Log the API call with explicit provider="openrouter"
                            log_openrouter_call("openrouter", json_data, response, duration, success)
                            
                    return response
                else:
                    # Not an OpenRouter call, use the existing patched version
                    return original_post(*args, **kwargs)
            
            # Apply our chain patch
            openrouter_patched_post._openrouter_tracker_patched = True
            requests.post = openrouter_patched_post
            logger.info("Successfully chained OpenRouter tracking to existing requests.post patch")

        logger.info("OpenRouter patching setup complete")

    except Exception as e:
        logger.error(f"Failed during OpenRouter patching process: {e}")
        logger.error(traceback.format_exc())
