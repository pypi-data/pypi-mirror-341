"""
OpenAI-specific patching logic for LLM tracking.
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

def count_tokens_openai(text, model):
    """Count tokens in text using tiktoken for OpenAI models"""
    try:
        import tiktoken
        encoding = tiktoken.encoding_for_model(model)
        return {
            TOKEN_COUNT_KEYS["PROMPT_TOKENS"]: len(encoding.encode(text)),
            TOKEN_COUNT_KEYS["COMPLETION_TOKENS"]: 0,
            TOKEN_COUNT_KEYS["TOTAL_TOKENS"]: len(encoding.encode(text))
        }
    except Exception as e:
        logger.warning(f"Failed to count tokens for OpenAI: {e}")
        return DEFAULT_TOKEN_COUNT

def log_openai_call(provider, request_args, response, duration, success):
    """Log an OpenAI API call according to the unified TROPIR schema."""
    try:
        # Get stack trace for template substitutions
        stack = traceback.extract_stack()
        stack_info = format_stack_trace(stack)

        # Extract messages from request_args, handling responses.create format
        messages = []
        if "messages" in request_args:
            # Standard chat.completions.create format
            messages = request_args.get("messages", [])
        elif "input" in request_args:
            # responses.create format
            if isinstance(request_args["input"], str):
                input_data = request_args["input"]
                instructions = request_args.get("instructions", "")
                
                if instructions:
                    messages = [
                        {"role": "system", "content": instructions},
                        {"role": "user", "content": input_data}
                    ]
                else:
                    messages = [{"role": "user", "content": input_data}]
            elif isinstance(request_args["input"], list):
                # Handle list of role/content pairs
                messages = request_args["input"]
        
        processed_messages = process_messages(messages)
        
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
        
        # Standardize tools format from functions or tools
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
        
        # Handle responses.create format response
        if hasattr(response, "output_text") or hasattr(response, "text"):
            # responses.create format uses output_text or text
            response_text = getattr(response, "output_text", None) or getattr(response, "text", "")
            
            # Extract usage if available
            if hasattr(response, "usage"):
                if hasattr(response.usage, "model_dump"):
                    usage = response.usage.model_dump()
                else:
                    try:
                        usage = vars(response.usage)
                    except:
                        usage = {}
            
            # Handle streaming in_progress attribute
            if hasattr(response, "in_progress") and response.in_progress:
                if not response_text:
                    response_text = "[STREAMING_RESPONSE]"
        
        # Handle OpenAI responses
        elif hasattr(response, "to_dict"):
            # Dictionary approach
            response_dict = response.to_dict()
            
            # Extract response text from choices
            if "choices" in response_dict and response_dict["choices"]:
                choice = response_dict["choices"][0]
                
                if "message" in choice and choice["message"]:
                    message = choice["message"]
                    
                    # Check for content
                    if "content" in message and message["content"] is not None:
                        response_text = message["content"]
                    
                    # Check for function call
                    if "function_call" in message and message["function_call"]:
                        func_call = message["function_call"]
                        name = func_call.get("name", "unknown_function")
                        args = func_call.get("arguments", "{}")
                        
                        # Store function call info in tool_calls format
                        function_call_info = {
                            "calls": [
                                {
                                    "id": f"call_{uuid.uuid4().hex[:8]}",
                                    "type": "function",
                                    "function": {
                                        "name": name,
                                        "arguments": args
                                    }
                                }
                            ]
                        }
                        
                        # Try to parse arguments
                        try:
                            args_obj = json.loads(args)
                            function_call_info["parsed_arguments"] = args_obj
                        except Exception:
                            function_call_info["parsed_arguments"] = {}
                        
                        # Format response text if content was None
                        if not response_text:
                            response_text = f"[FUNCTION_CALL: {name}({args})]"
                    
                    # Check for tool calls
                    elif "tool_calls" in message and message["tool_calls"]:
                        tool_calls = message["tool_calls"]
                        tool_call_details = []
                        parsed_args_combined = {}
                        
                        for tool in tool_calls:
                            tool_details = {
                                "id": tool.get("id", f"call_{uuid.uuid4().hex[:8]}"),
                                "type": tool.get("type", "function"),
                                "function": {
                                    "name": tool.get("function", {}).get("name", "unknown_function"),
                                    "arguments": tool.get("function", {}).get("arguments", "{}")
                                }
                            }
                            
                            # Try to parse arguments
                            try:
                                args_obj = json.loads(tool_details["function"]["arguments"])
                                # Store args for the first tool call or the one with most data
                                if not parsed_args_combined or len(args_obj) > len(parsed_args_combined):
                                    parsed_args_combined = args_obj
                            except Exception:
                                pass
                                
                            tool_call_details.append(tool_details)
                        
                        # Store all tool calls
                        function_call_info = {
                            "calls": tool_call_details,
                            "parsed_arguments": parsed_args_combined
                        }
                        
                        # Format response text if content was None
                        if not response_text:
                            response_text = f"[TOOL_CALLS: {len(message['tool_calls'])}]"
                
                elif "delta" in choice and choice["delta"]:
                    # Streaming response
                    if "content" in choice["delta"] and choice["delta"]["content"]:
                        response_text = choice["delta"]["content"]
                    else:
                        response_text = "[STREAMING_RESPONSE]"
            
            # Extract usage information
            if "usage" in response_dict:
                usage = response_dict["usage"]
        
        # Attribute-based approach if dictionary approach failed
        if not response_text and hasattr(response, "choices") and response.choices:
            if hasattr(response.choices[0], "message") and response.choices[0].message:
                message = response.choices[0].message
                
                # Check content
                if hasattr(message, "content") and message.content is not None:
                    response_text = message.content
                
                # Check function call
                if hasattr(message, "function_call") and message.function_call:
                    try:
                        func_call = message.function_call
                        name = getattr(func_call, "name", "unknown_function")
                        args = getattr(func_call, "arguments", "{}")
                        
                        # Store function call info in tool_calls format
                        function_call_info = {
                            "calls": [
                                {
                                    "id": f"call_{uuid.uuid4().hex[:8]}",
                                    "type": "function",
                                    "function": {
                                        "name": name,
                                        "arguments": args
                                    }
                                }
                            ]
                        }
                        
                        # Try to parse arguments
                        try:
                            if isinstance(args, str):
                                args_obj = json.loads(args)
                                function_call_info["parsed_arguments"] = args_obj
                            else:
                                function_call_info["parsed_arguments"] = {}
                        except Exception:
                            function_call_info["parsed_arguments"] = {}
                        
                        # Format response text if content was None
                        if not response_text:
                            response_text = f"[FUNCTION_CALL: {name}({args})]"
                    except Exception as e:
                        logger.error(f"Error extracting function call: {e}")
                
                # Check tool calls
                elif hasattr(message, "tool_calls") and message.tool_calls:
                    try:
                        tool_calls = message.tool_calls
                        tool_call_details = []
                        parsed_args_combined = {}
                        
                        for tool in tool_calls:
                            tool_details = {
                                "id": getattr(tool, "id", f"call_{uuid.uuid4().hex[:8]}"),
                                "type": getattr(tool, "type", "function"),
                            }
                            
                            if hasattr(tool, "function"):
                                func = tool.function
                                tool_details["function"] = {
                                    "name": getattr(func, "name", "unknown_function"),
                                    "arguments": getattr(func, "arguments", "{}")
                                }
                                
                                # Try to parse arguments
                                try:
                                    if isinstance(tool_details["function"]["arguments"], str):
                                        args_obj = json.loads(tool_details["function"]["arguments"])
                                        # Store args for the first tool call or the one with most data
                                        if not parsed_args_combined or len(args_obj) > len(parsed_args_combined):
                                            parsed_args_combined = args_obj
                                except Exception:
                                    pass
                            
                            tool_call_details.append(tool_details)
                        
                        # Store all tool calls in standardized format
                        function_call_info = {
                            "calls": tool_call_details,
                            "parsed_arguments": parsed_args_combined
                        }
                        
                        # Format response text if content was None
                        if not response_text:
                            response_text = f"[TOOL_CALLS: {len(tool_calls)}]"
                    except Exception as e:
                        logger.error(f"Error extracting tool calls: {e}")
            
            # Check for streaming response
            elif hasattr(response.choices[0], "delta") and response.choices[0].delta:
                if hasattr(response.choices[0].delta, "content") and response.choices[0].delta.content is not None:
                    response_text = response.choices[0].delta.content
                else:
                    response_text = "[STREAMING_RESPONSE]"
                    
        # Handle HTTP response from direct API calls with requests
        elif hasattr(response, "json") and callable(response.json):
            try:
                response_dict = response.json()
                
                # Extract response text from choices
                if "choices" in response_dict and response_dict["choices"]:
                    choice = response_dict["choices"][0]
                    
                    if "message" in choice and choice["message"]:
                        message = choice["message"]
                        
                        # Check for content
                        if "content" in message and message["content"] is not None:
                            response_text = message["content"]
                        
                        # Check for function call
                        if "function_call" in message and message["function_call"]:
                            func_call = message["function_call"]
                            name = func_call.get("name", "unknown_function")
                            args = func_call.get("arguments", "{}")
                            
                            # Store function call info in tool_calls format
                            function_call_info = {
                                "calls": [
                                    {
                                        "id": f"call_{uuid.uuid4().hex[:8]}",
                                        "type": "function",
                                        "function": {
                                            "name": name,
                                            "arguments": args
                                        }
                                    }
                                ]
                            }
                            
                            # Try to parse arguments
                            try:
                                args_obj = json.loads(args)
                                function_call_info["parsed_arguments"] = args_obj
                            except Exception:
                                function_call_info["parsed_arguments"] = {}
                            
                            # Format response text if content was None
                            if not response_text:
                                response_text = f"[FUNCTION_CALL: {name}({args})]"
                        
                        # Check for tool calls
                        elif "tool_calls" in message and message["tool_calls"]:
                            tool_calls = message["tool_calls"]
                            tool_call_details = []
                            parsed_args_combined = {}
                            
                            for tool in tool_calls:
                                tool_details = {
                                    "id": tool.get("id", f"call_{uuid.uuid4().hex[:8]}"),
                                    "type": tool.get("type", "function"),
                                    "function": {
                                        "name": tool.get("function", {}).get("name", "unknown_function"),
                                        "arguments": tool.get("function", {}).get("arguments", "{}")
                                    }
                                }
                                
                                # Try to parse arguments
                                try:
                                    args_obj = json.loads(tool_details["function"]["arguments"])
                                    # Store args for the first tool call or the one with most data
                                    if not parsed_args_combined or len(args_obj) > len(parsed_args_combined):
                                        parsed_args_combined = args_obj
                                except Exception:
                                    pass
                                    
                                tool_call_details.append(tool_details)
                            
                            # Store all tool calls
                            function_call_info = {
                                "calls": tool_call_details,
                                "parsed_arguments": parsed_args_combined
                            }
                            
                            # Format response text if content was None
                            if not response_text:
                                response_text = f"[TOOL_CALLS: {len(message['tool_calls'])}]"
                
                # Extract usage information
                if "usage" in response_dict:
                    usage = response_dict["usage"]
            except Exception as e:
                logger.error(f"Error processing HTTP response: {e}")
                response_text = f"[ERROR_PROCESSING_RESPONSE: {str(e)}]"

        # Extract usage if available
        if not usage and hasattr(response, "usage"):
            if hasattr(response.usage, "model_dump"):
                usage = response.usage.model_dump()
            else:
                try:
                    usage = vars(response.usage)
                except:
                    usage = {}

        # Count tokens if not provided
        if not usage:
            prompt_text = " ".join(str(msg.get("content", "")) for msg in processed_messages if msg.get("content"))
            resp_text_str = str(response_text) if response_text else ""
            usage = count_tokens_openai(prompt_text + resp_text_str, model)
        
        # Standardize the usage structure with token_details
        standardized_usage = {
            "prompt_tokens": usage.get("prompt_tokens", 0),
            "completion_tokens": usage.get("completion_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0),
            "token_details": {
                "cached_tokens": usage.get("prompt_tokens_details", {}).get("cached_tokens", None),
                "audio_tokens": (
                    usage.get("prompt_tokens_details", {}).get("audio_tokens", 0) + 
                    usage.get("completion_tokens_details", {}).get("audio_tokens", 0)
                ) or None,
                "reasoning_tokens": usage.get("completion_tokens_details", {}).get("reasoning_tokens", None),
                "accepted_prediction_tokens": usage.get("completion_tokens_details", {}).get("accepted_prediction_tokens", None),
                "rejected_prediction_tokens": usage.get("completion_tokens_details", {}).get("rejected_prediction_tokens", None)
            }
        }

        # Generate log entry with standardized request
        log_entry = create_base_log_entry(provider, standardized_request)
        
        # Add remaining fields
        log_entry.update({
            "response": response_text,
            "usage": standardized_usage,
            "duration": duration,
            "success": success,
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
                
        # Write to log file
        send_log(log_entry)

    except Exception as e:
        logger.error(f"Error logging OpenAI call: {str(e)}")
        logger.error(traceback.format_exc())

def patched_requests_post(original_post, *args, **kwargs):
    """
    Patched version of requests.post to track direct HTTP calls to OpenAI API.
    """
    url = args[0] if args else kwargs.get('url')
    
    # Only process OpenAI API calls
    if url and isinstance(url, str) and "api.openai.com" in url:
        try:
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
                logger.error(f"Error making OpenAI HTTP request: {str(e)}")
                raise e
            finally:
                duration = time.time() - start_time
                
                # Only log if this is a chat completion or similar endpoint
                if "chat/completions" in url or "completions" in url:
                    # Log the API call
                    log_openai_call("openai", json_data, response, duration, success)
                    
            return response
        except Exception as e:
            logger.error(f"Error in patched requests.post: {str(e)}")
            logger.error(traceback.format_exc())
            # Let the original request proceed even if tracking fails
            return original_post(*args, **kwargs)
    else:
        # For non-OpenAI URLs, just call the original function
        return original_post(*args, **kwargs)

def setup_openai_patching():
    """Set up tracking for OpenAI by patching target methods."""

    try:
        # Import the specific class where the 'create' method resides
        from openai.resources.chat.completions import Completions as OpenAICompletions

        # Check if the 'create' method exists and hasn't been patched yet
        if hasattr(OpenAICompletions, "create") and not getattr(OpenAICompletions.create, '_llm_tracker_patched', False):
            original_create_method = OpenAICompletions.create  # Get the original function

            # Create the wrapped version using our helper function
            patched_create = create_generic_method_wrapper(original_create_method, "openai", log_openai_call)

            # Replace the original method on the class with the patched one
            OpenAICompletions.create = patched_create

        # Patch the responses methods
        try:
            from openai.resources.responses import Responses as OpenAIResponses
            from openai.resources.responses import AsyncResponses as AsyncOpenAIResponses

            # Patch synchronous Responses methods
            methods_to_patch = ['create', 'stream', 'parse', 'retrieve', 'delete']
            
            for method_name in methods_to_patch:
                if hasattr(OpenAIResponses, method_name) and not getattr(getattr(OpenAIResponses, method_name), '_llm_tracker_patched', False):
                    original_method = getattr(OpenAIResponses, method_name)
                    patched_method = create_generic_method_wrapper(original_method, "openai", log_openai_call)
                    setattr(OpenAIResponses, method_name, patched_method)
            
            # Patch async Responses methods
            async_methods_to_patch = ['create', 'stream', 'parse', 'retrieve', 'delete']
            
            for method_name in async_methods_to_patch:
                if hasattr(AsyncOpenAIResponses, method_name) and not getattr(getattr(AsyncOpenAIResponses, method_name), '_llm_tracker_patched', False):
                    original_method = getattr(AsyncOpenAIResponses, method_name)
                    patched_method = create_generic_method_wrapper(original_method, "openai", log_openai_call)
                    setattr(AsyncOpenAIResponses, method_name, patched_method)
                
        except ImportError:
            logger.warning("Could not import OpenAI responses classes. OpenAI responses tracking may not work.")
        except Exception as e:
            logger.error(f"Failed during OpenAI responses patching: {e}")
            logger.error(traceback.format_exc())

        # Patch requests.post for direct HTTP API calls
        if not getattr(requests.post, '_llm_tracker_patched', False):
            original_post = requests.post
            patched_post = functools.wraps(original_post)(
                lambda *args, **kwargs: patched_requests_post(original_post, *args, **kwargs)
            )
            patched_post._llm_tracker_patched = True
            requests.post = patched_post
            logger.info("Successfully patched requests.post for OpenAI API tracking")

    except ImportError:
        logger.warning("Could not import 'openai.resources.chat.completions.Completions'. OpenAI tracking may not work.")
    except Exception as e:
        logger.error(f"Failed during OpenAI patching process: {e}")
        logger.error(traceback.format_exc())