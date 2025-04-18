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
    """Process OpenRouter/OpenAI messages to handle special content types"""
    # Handle different input types
    if messages is None:
        return []
    
    # Create a new list for the processed messages
    processed_messages = []
    
    # Process each message based on its type
    for idx, msg in enumerate(messages):
        # Handle dictionary messages
        if isinstance(msg, dict) or hasattr(msg, "keys"):
            # Convert to regular dict if it's a frozen dict or similar
            msg_dict = dict(msg) if not isinstance(msg, dict) else msg
            
            # Create a copy to avoid modifying the original
            processed_msg = msg_dict.copy()
            
            # Process different message roles
            if msg_dict.get("role") == "assistant" and "content" in msg_dict:
                # Handle assistant messages with tool calls (function calls)
                if "tool_calls" in msg_dict or "function_call" in msg_dict:
                    # Extract tool calls
                    tool_calls = []
                    
                    # Process new tool_calls format
                    if "tool_calls" in msg_dict:
                        tool_calls = msg_dict.get("tool_calls", [])
                    # Process legacy function_call format
                    elif "function_call" in msg_dict:
                        function_call = msg_dict.get("function_call", {})
                        if function_call and isinstance(function_call, dict):
                            tool_calls = [{
                                "id": function_call.get("id", str(uuid.uuid4())),
                                "type": "function",
                                "function": {
                                    "name": function_call.get("name", ""),
                                    "arguments": function_call.get("arguments", "{}")
                                }
                            }]
                    
                    # Add tool calls as a formatted string in content for easier matching
                    # Only do this if content is empty or None
                    if not msg_dict.get("content"):
                        tool_call_descriptions = []
                        for tool_call in tool_calls:
                            if isinstance(tool_call, dict) and "function" in tool_call:
                                func = tool_call["function"]
                                name = func.get("name", "")
                                args = func.get("arguments", "{}")
                                # Format in a way that's recognizable but not overwhelming
                                tool_call_descriptions.append(f"Tool: {name}, Args: {args}")
                        
                        # Join all tool call descriptions
                        if tool_call_descriptions:
                            processed_msg["content"] = "[TOOL_CALLS]\n" + "\n".join(tool_call_descriptions)
            
            # Process content if it's a string
            if isinstance(processed_msg.get("content"), str):
                # Strip leading and trailing whitespace/newlines
                processed_msg["content"] = processed_msg["content"].strip()
            
            # Add to processed messages
            processed_messages.append(processed_msg)
        
        # Handle message objects (from SDK)
        elif not isinstance(msg, (str, dict)) and hasattr(msg, "role"):
            # This is likely an OpenAI message object
            processed_msg = {
                "role": getattr(msg, "role", "unknown")
            }
            
            # Extract content
            if hasattr(msg, "content"):
                content = getattr(msg, "content")
                if isinstance(content, str):
                    processed_msg["content"] = content.strip()
                else:
                    processed_msg["content"] = str(content)
            
            # Handle tool calls in assistant messages
            if getattr(msg, "role", "") == "assistant" and hasattr(msg, "tool_calls") and getattr(msg, "tool_calls"):
                tool_calls = getattr(msg, "tool_calls", [])
                
                # If content is empty, create a representation of tool calls
                if not processed_msg.get("content"):
                    tool_call_descriptions = []
                    for tool_call in tool_calls:
                        # Extract function info
                        if hasattr(tool_call, "function"):
                            func = getattr(tool_call, "function")
                            name = getattr(func, "name", "")
                            args = getattr(func, "arguments", "{}")
                            tool_call_descriptions.append(f"Tool: {name}, Args: {args}")
                    
                    if tool_call_descriptions:
                        processed_msg["content"] = "[TOOL_CALLS]\n" + "\n".join(tool_call_descriptions)
            
            # Add processed message
            processed_messages.append(processed_msg)
        
        # Handle string messages (not common, but just in case)
        elif isinstance(msg, str):
            # Simple text message
            processed_messages.append({
                "role": "user",  # Assume user role for simple strings
                "content": msg.strip()
            })
        
        # Fallback for any other types
        else:
            # Try to convert to string
            processed_messages.append({
                "role": "unknown",
                "content": str(msg)
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
    """Log an OpenRouter LLM API call according to the unified TROPIR schema."""
    try:
        # Get stack trace for template substitutions
        stack = traceback.extract_stack()
        stack_info = format_stack_trace(stack)

        # Extract and process messages from request_args
        messages = request_args.get("messages", [])
        processed_messages = process_messages(messages)
        
        # Extract assistant messages for tool call processing
        assistant_messages = [msg for msg in processed_messages if msg.get("role") == "assistant"]
        
        # Prepare standardized request structure
        standardized_request = {
            "model": request_args.get("model", ""),
            "messages": processed_messages,
            "temperature": request_args.get("temperature"),
            "max_tokens": request_args.get("max_tokens") or request_args.get("maxTokens"),
            "top_p": request_args.get("top_p") or request_args.get("topP"),
            "frequency_penalty": request_args.get("frequency_penalty"),
            "presence_penalty": request_args.get("presence_penalty"),
            "stop": request_args.get("stop", None),
            "n": request_args.get("n")
        }

        response_text = ""
        usage = {}
        function_call_info = None
        
        # Check for stored JSON data on HTTP response objects
        response_json = None
        if hasattr(response, '_tropir_json_data'):
            response_json = response._tropir_json_data
        elif hasattr(response, 'status_code') and hasattr(response, 'json') and callable(response.json):
            try:
                response_json = response.json()
            except Exception as e:
                logger.warning(f"Failed to get JSON from HTTP response: {e}")
                
        # Process HTTP response with JSON data
        if response_json:
            # Extract content from JSON response
            if "choices" in response_json and response_json["choices"]:
                choices = response_json["choices"]
                first_choice = choices[0] if choices else {}
                
                if "message" in first_choice:
                    message = first_choice["message"]
                    
                    # Extract content
                    if "content" in message:
                        response_text = message["content"]
                    
                    # Extract function call
                    if "function_call" in message:
                        function_call = message["function_call"]
                        function_call_info = {
                            "name": function_call.get("name", ""),
                            "arguments": function_call.get("arguments", "{}")
                        }
                    
                    # Extract tool calls (newer structure)
                    elif "tool_calls" in message:
                        tool_calls = message["tool_calls"]
                        if tool_calls:
                            function_calls = []
                            for tool_call in tool_calls:
                                if tool_call.get("type") == "function":
                                    function_details = tool_call.get("function", {})
                                    function_calls.append({
                                        "id": tool_call.get("id", str(uuid.uuid4())),
                                        "type": "function",
                                        "function": {
                                            "name": function_details.get("name", ""),
                                            "arguments": function_details.get("arguments", "{}")
                                        }
                                    })
                            
                            if function_calls:
                                function_call_info = {
                                    "calls": function_calls
                                }
                                
                                # Try to extract parsed arguments
                                try:
                                    first_call = function_calls[0]
                                    args_json = first_call["function"]["arguments"]
                                    function_call_info["parsed_arguments"] = json.loads(args_json)
                                except (IndexError, KeyError, json.JSONDecodeError):
                                    function_call_info["parsed_arguments"] = {}
            
            # Extract usage information if available
            if "usage" in response_json:
                usage = {
                    "prompt_tokens": response_json["usage"].get("prompt_tokens", 0),
                    "completion_tokens": response_json["usage"].get("completion_tokens", 0),
                    "total_tokens": response_json["usage"].get("total_tokens", 0)
                }
        
        # Process SDK response object
        elif success and hasattr(response, "model_dump"):
            # For Pydantic models
            try:
                response_dict = response.model_dump()
                
                # Extract content
                choices = response_dict.get("choices", [])
                if choices:
                    first_choice = choices[0]
                    message = first_choice.get("message", {})
                    
                    # Get content
                    response_text = message.get("content", "")
                    
                    # Get function call
                    if "function_call" in message:
                        function_call = message["function_call"]
                        function_call_info = {
                            "name": function_call.get("name", ""),
                            "arguments": function_call.get("arguments", "{}")
                        }
                    
                    # Get tool calls
                    elif "tool_calls" in message:
                        tool_calls = message["tool_calls"]
                        if tool_calls:
                            function_calls = []
                            for tool_call in tool_calls:
                                if tool_call.get("type") == "function":
                                    function_details = tool_call.get("function", {})
                                    function_calls.append({
                                        "id": tool_call.get("id", str(uuid.uuid4())),
                                        "type": "function",
                                        "function": {
                                            "name": function_details.get("name", ""),
                                            "arguments": function_details.get("arguments", "{}")
                                        }
                                    })
                            
                            if function_calls:
                                function_call_info = {
                                    "calls": function_calls
                                }
                                
                                # Extract parsed arguments
                                try:
                                    first_call = function_calls[0]
                                    args_json = first_call["function"]["arguments"]
                                    function_call_info["parsed_arguments"] = json.loads(args_json)
                                except (IndexError, KeyError, json.JSONDecodeError):
                                    function_call_info["parsed_arguments"] = {}
                
                # Extract usage
                if "usage" in response_dict:
                    usage_data = response_dict["usage"]
                    usage = {
                        "prompt_tokens": usage_data.get("prompt_tokens", 0),
                        "completion_tokens": usage_data.get("completion_tokens", 0),
                        "total_tokens": usage_data.get("total_tokens", 0)
                    }
            except Exception as e:
                logger.warning(f"Failed to process SDK response object: {e}")
        
        # Process error responses
        elif isinstance(response, dict) and "error" in response:
            response_text = response.get("error", {}).get("message", str(response))
            usage = {}
        
        # Create the log entry
        log_entry = create_base_log_entry(provider, standardized_request)
        
        # Get assistant messages for tool call display
        assistant_msgs = [msg for msg in log_entry["request"]["messages"] if msg.get("role") == "assistant"]
        
        # Add remaining fields
        log_entry.update({
            "response": response_text,
            "usage": {
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
            },
            "duration": duration,
            "success": success,
        })
        
        # Add function_call or tool_calls
        if function_call_info:
            if "calls" in function_call_info:
                log_entry["tool_calls"] = function_call_info
            else:
                # Legacy function_call format
                log_entry["function_call"] = {
                    "name": function_call_info.get("name", ""),
                    "arguments": function_call_info.get("arguments", "{}")
                }
        
        # Get user_id from API
        user_id = get_user_id()
        if user_id:
            log_entry["user_id"] = user_id
            
        # Call template matching API and update log entry
        log_entry = process_template_matching(processed_messages, user_id, stack_info, log_entry)

        # Send log
        send_log(log_entry)

    except Exception as e:
        logger.error(f"Error logging OpenRouter call: {str(e)}")
        logger.error(traceback.format_exc())

def patched_requests_post(original_post, *args, **kwargs):
    """
    Patched version of requests.post to track direct HTTP calls to OpenRouter API.
    """
    url = args[0] if args else kwargs.get('url')
    
    # Only process OpenRouter API endpoints
    is_openrouter_api = is_openrouter_url(url)
    
    if is_openrouter_api:
        try:
            start_time = time.time()
            success = True
            
            # Handle both JSON and data parameters
            if 'json' in kwargs:
                request_data = kwargs.get('json', {})
            elif 'data' in kwargs:
                # Try to parse data if it's a JSON string
                data = kwargs.get('data', '{}')
                if isinstance(data, str):
                    try:
                        request_data = json.loads(data)
                    except:
                        request_data = {'data': data}
                else:
                    request_data = {'data': data}
            else:
                request_data = {}
            
            # Extract assistant messages from request data
            assistant_messages = []
            if "messages" in request_data:
                messages = request_data["messages"]
                for msg in messages:
                    if isinstance(msg, dict) and msg.get("role") == "assistant":
                        assistant_messages.append(msg)
            
            # Make the actual request
            try:
                response = original_post(*args, **kwargs)
                
                # Extract JSON data from the response
                try:
                    response_json = response.json()
                    # Save JSON data on response object for use by log_openrouter_call
                    response._tropir_json_data = response_json
                    success = response.status_code < 400
                except Exception as json_error:
                    logger.error(f"Failed to parse JSON from OpenRouter response: {json_error}")
                    response_json = {"error": {"message": f"Failed to parse response: {str(json_error)}"}}
                    success = False
            except Exception as e:
                success = False
                response_json = {"error": {"message": str(e)}}
                response = response_json  # Set response to the error JSON
                logger.error(f"Error making OpenRouter HTTP request: {str(e)}")
                raise
            finally:
                duration = time.time() - start_time
                
                # Only log if this wasn't already logged by the SDK
                if not getattr(request_data, '_tropir_logged', False):
                    log_openrouter_call("openrouter", request_data, response, duration, success)
                    
                    # Mark as logged to prevent double-logging
                    if isinstance(request_data, dict):
                        request_data['_tropir_logged'] = True
            
            return response
        except Exception as e:
            logger.error(f"Error in patched requests.post for OpenRouter: {str(e)}")
            logger.error(traceback.format_exc())
            # Always let the original request proceed even if tracking fails
            return original_post(*args, **kwargs)
    else:
        # For non-OpenRouter URLs, just call the original function
        return original_post(*args, **kwargs)

def patch_openai_client_init():
    """Patch OpenAI client initialization to detect OpenRouter usage"""
    try:
        from openai import OpenAI
        
        # Store original __init__ method
        if not getattr(OpenAI.__init__, '_openrouter_patched', False):
            original_init = OpenAI.__init__
            
            @functools.wraps(original_init)
            def patched_init(self, *args, **kwargs):
                # Call the original __init__
                original_init(self, *args, **kwargs)
                
                # Check if this is an OpenRouter client by examining base_url
                base_url = getattr(self, "base_url", None)
                if base_url and is_openrouter_url(base_url):
                    # Mark this client as an OpenRouter client
                    setattr(self, "_is_openrouter", True)
                else:
                    setattr(self, "_is_openrouter", False)
            
            # Replace the original __init__ method
            OpenAI.__init__ = patched_init
            OpenAI.__init__._openrouter_patched = True
            
        return True
    except (ImportError, AttributeError) as e:
        logger.warning(f"Failed to patch OpenAI client initialization: {e}")
        return False

def setup_openrouter_patching():
    """Set up tracking for OpenRouter by patching API methods."""
    try:
        # Try to patch the OpenAI library first - this handles OpenRouter using the OpenAI SDK
        try:
            # Patch requests library for direct HTTP calls
            setup_http_patching()
            
            # Patch the OpenAI client initialization to detect OpenRouter
            patch_openai_client_init()
            
            # Try to patch the OpenAI v1 SDK
            try:
                from openai.resources.chat.completions import Completions
                
                # Patch the create method if it exists
                if hasattr(Completions, "create") and not getattr(Completions.create, '_openrouter_patched', False):
                    original_create_method = Completions.create
                    
                    @functools.wraps(original_create_method)
                    def patched_create_method(self, *args, **kwargs):
                        # Check if the client is configured for OpenRouter
                        is_openrouter = False
                        base_url = None
                        
                        # Check for OpenRouter markers on the client
                        if hasattr(self, "_client"):
                            if getattr(self._client, "_is_openrouter", False):
                                is_openrouter = True
                            
                            # Check base_url
                            if hasattr(self._client, "base_url"):
                                base_url = self._client.base_url
                                if is_openrouter_url(base_url):
                                    is_openrouter = True
                                    
                            # Check organization (OR appends 'openrouter' to organization)
                            if hasattr(self._client, "organization") and "openrouter" in getattr(self._client, "organization", ""):
                                is_openrouter = True
                        
                        # Check model format if present (openai/gpt-4 format)
                        if "model" in kwargs and is_openrouter_model_format(kwargs.get("model", "")):
                            is_openrouter = True
                        
                        # Process messages for better analysis
                        if "messages" in kwargs:
                            messages = kwargs["messages"]
                            assistant_messages = [msg for msg in messages if (
                                (isinstance(msg, dict) and msg.get("role") == "assistant") or
                                (hasattr(msg, "role") and getattr(msg, "role") == "assistant")
                            )]
                        else:
                            assistant_messages = []
                        
                        # Execute the original method
                        start_time = time.perf_counter()
                        success = True
                        response = None
                        
                        try:
                            response = original_create_method(self, *args, **kwargs)
                            
                            # Process and log the API call if it's an OpenRouter call
                            if is_openrouter and not getattr(kwargs, '_tropir_logged', False):
                                duration = time.perf_counter() - start_time
                                
                                # Get all assistant messages in the request
                                assistant_msgs = []
                                for msg in kwargs.get('messages', []):
                                    if isinstance(msg, dict) and msg.get('role') == 'assistant':
                                        assistant_msgs.append(msg)
                                    elif hasattr(msg, 'role') and getattr(msg, 'role') == 'assistant':
                                        # Convert to dict representation
                                        assistant_dict = {'role': 'assistant'}
                                        if hasattr(msg, 'content'):
                                            assistant_dict['content'] = getattr(msg, 'content')
                                        assistant_msgs.append(assistant_dict)
                                
                                # Log the call
                                log_openrouter_call("openrouter", kwargs, response, duration, success)
                                
                                # Mark as logged to prevent duplicate logging
                                if isinstance(kwargs, dict):
                                    kwargs['_tropir_logged'] = True
                                
                            return response
                        except Exception as e:
                            success = False
                            # Log the failed call
                            if is_openrouter:
                                duration = time.perf_counter() - start_time
                                log_openrouter_call("openrouter", kwargs, {"error": str(e)}, duration, success)
                            raise
                    
                    # Replace the original method
                    Completions.create = patched_create_method
                    Completions.create._openrouter_patched = True
                
                # Try to patch other methods in the SDK
                sdk_methods = []
                try:
                    # Add other methods to patch
                    from openai.resources import chat
                    sdk_methods.append(("create", chat.completions.Completions))
                except (ImportError, AttributeError):
                    pass
                
                # Patch each method
                for method_name, cls in sdk_methods:
                    if hasattr(cls, method_name) and not getattr(getattr(cls, method_name), '_openrouter_patched', False):
                        original_method = getattr(cls, method_name)
                        
                        @functools.wraps(original_method)
                        def patched_method(self, *args, **kwargs):
                            # Check if the client is configured for OpenRouter
                            is_openrouter = False
                            
                            # Check client markers
                            if hasattr(self, "_client"):
                                if getattr(self._client, "_is_openrouter", False):
                                    is_openrouter = True
                                
                                # Check base_url
                                if hasattr(self._client, "base_url") and is_openrouter_url(self._client.base_url):
                                    is_openrouter = True
                                
                                # Check organization
                                if hasattr(self._client, "organization") and "openrouter" in getattr(self._client, "organization", ""):
                                    is_openrouter = True
                            
                            # Check model format
                            if "model" in kwargs and is_openrouter_model_format(kwargs.get("model", "")):
                                is_openrouter = True
                            
                            # Process messages
                            if "messages" in kwargs:
                                messages = kwargs["messages"]
                                assistant_messages = [msg for msg in messages if (
                                    (isinstance(msg, dict) and msg.get("role") == "assistant") or
                                    (hasattr(msg, "role") and getattr(msg, "role") == "assistant")
                                )]
                            else:
                                assistant_messages = []
                            
                            # Execute the original method
                            start_time = time.perf_counter()
                            success = True
                            response = None
                            
                            try:
                                response = original_method(self, *args, **kwargs)
                                
                                # Log the call if it's OpenRouter
                                if is_openrouter and not getattr(kwargs, '_tropir_logged', False):
                                    duration = time.perf_counter() - start_time
                                    log_openrouter_call("openrouter", kwargs, response, duration, success)
                                    
                                    # Mark as logged
                                    if isinstance(kwargs, dict):
                                        kwargs['_tropir_logged'] = True
                                
                                return response
                            except Exception as e:
                                success = False
                                # Log the failed call
                                if is_openrouter:
                                    duration = time.perf_counter() - start_time
                                    log_openrouter_call("openrouter", kwargs, {"error": str(e)}, duration, success)
                                raise
                        
                            # Replace the method
                            setattr(cls, method_name, patched_method)
                            getattr(cls, method_name)._openrouter_patched = True
            
            except (ImportError, AttributeError) as e:
                logger.warning(f"Failed to patch OpenAI SDK for OpenRouter tracking: {e}")
            
        except ImportError:
            logger.warning("Could not import 'openai'. Only direct API calls will be tracked.")
    
    except Exception as e:
        logger.error(f"Failed during OpenRouter patching process: {e}")
        logger.error(traceback.format_exc()) 