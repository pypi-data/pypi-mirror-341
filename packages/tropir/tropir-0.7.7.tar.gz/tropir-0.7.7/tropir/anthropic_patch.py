"""
Anthropic-specific patching logic for LLM tracking.
"""

import functools
import time
import traceback
import json
import os
import uuid
from datetime import datetime
from loguru import logger
import requests

from tropir.transport import send_log

from .constants import (
    TOKEN_COUNT_KEYS,
    DEFAULT_TOKEN_COUNT,
    ANTHROPIC_MODEL_PREFIXES
)
from .stack_tracing import format_stack_trace
from .utils import (
    create_base_log_entry,
    create_generic_method_wrapper,
    create_async_method_wrapper,
    get_user_id,
    process_template_matching,
)

def process_anthropic_messages(messages):
    """Process Anthropic messages to handle special content types"""
    processed_messages = []
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
                        # Handle Anthropic image types
                        if item_copy.get("type") == "image" and "source" in item_copy:
                            source = item_copy["source"]
                            if isinstance(source, dict) and "data" in source:
                                if source.get("media_type", "").startswith("image/"):
                                    item_copy["source"]["data"] = "[BASE64_IMAGE_REMOVED]"
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
                # For Anthropic message objects
                if hasattr(msg, "type") and hasattr(msg, "role"):
                    # This is likely an Anthropic message
                    role = getattr(msg, "role", "unknown")
                    content = getattr(msg, "content", "")
                    
                    # Process content if it's a list (multi-modal or tool calls)
                    if isinstance(content, list):
                        processed_content = []
                        for item in content:
                            if hasattr(item, "type"):
                                item_type = getattr(item, "type")
                                if item_type == "text" and hasattr(item, "text"):
                                    processed_content.append({
                                        "type": "text",
                                        "text": getattr(item, "text", "").strip('\n')
                                    })
                                elif item_type == "image" and hasattr(item, "source"):
                                    source = getattr(item, "source")
                                    if hasattr(source, "data") and hasattr(source, "media_type"):
                                        # Don't include actual image data
                                        processed_content.append({
                                            "type": "image",
                                            "source": {
                                                "media_type": getattr(source, "media_type", ""),
                                                "data": "[BASE64_IMAGE_REMOVED]"
                                            }
                                        })
                                elif item_type == "tool_use" and hasattr(item, "tool_use"):
                                    tool_use = getattr(item, "tool_use")
                                    processed_content.append({
                                        "type": "tool_use",
                                        "tool_use": {
                                            "name": getattr(tool_use, "name", ""),
                                            "input": getattr(tool_use, "input", {})
                                        }
                                    })
                        processed_messages.append({
                            "role": role,
                            "content": processed_content
                        })
                    else:
                        # For simple string content
                        if isinstance(content, str):
                            content = content.strip('\n')
                        processed_messages.append({
                            "role": role,
                            "content": content
                        })
                else:
                    # Generic object handling
                    processed_messages.append({
                        "role": getattr(msg, "role", "unknown"),
                        "content": str(getattr(msg, "content", str(msg)))
                    })
            except Exception as e:
                # If all else fails, create a basic message
                logger.warning(f"Error processing Anthropic message object: {e}")
                processed_messages.append({
                    "role": getattr(msg, "role", "unknown"),
                    "content": str(getattr(msg, "content", str(msg)))
                })

    return processed_messages

def count_tokens_anthropic(text, model):
    """Count tokens in text specifically for Anthropic models"""
    try:
        # Try to use Anthropic's built-in token counter
        from anthropic import Anthropic
        client = Anthropic()
        token_count = client.count_tokens(text)
        return {
            TOKEN_COUNT_KEYS["PROMPT_TOKENS"]: token_count,
            TOKEN_COUNT_KEYS["COMPLETION_TOKENS"]: 0,
            TOKEN_COUNT_KEYS["TOTAL_TOKENS"]: token_count
        }
    except (ImportError, AttributeError) as e:
        # Fallback to approximate counting for Anthropic models
        # Claude models use roughly ~4 characters per token on average
        logger.warning(f"Using approximate token counting for Anthropic: {e}")
        approx_tokens = len(text) // 4
        return {
            TOKEN_COUNT_KEYS["PROMPT_TOKENS"]: approx_tokens,
            TOKEN_COUNT_KEYS["COMPLETION_TOKENS"]: 0,
            TOKEN_COUNT_KEYS["TOTAL_TOKENS"]: approx_tokens
        }
    except Exception as e:
        logger.warning(f"Failed to count tokens for Anthropic model: {e}")
        return DEFAULT_TOKEN_COUNT

def log_anthropic_call(provider, request_args, response, duration, success):
    """Log an Anthropic LLM API call according to the unified TROPIR schema."""
    try:
        logger.info(f"log_anthropic_call called: provider={provider}, success={success}, duration={duration:.2f}s")
        
        # Log request args summary
        try:
            model = request_args.get("model", "unknown")
            msg_count = len(request_args.get("messages", []))
            logger.info(f"Request - Model: {model}, Message count: {msg_count}")
        except:
            logger.info("Could not log request args summary")
        
        # Get stack trace for template substitutions
        stack = traceback.extract_stack()
        stack_info = format_stack_trace(stack)

        # Extract messages from request_args
        messages = request_args.get("messages", [])
        processed_messages = process_anthropic_messages(messages)
        logger.debug(f"Processed {len(processed_messages)} messages")
        
        # Add system message if present as a separate field
        if request_args.get("system") and not any(msg.get("role") == "system" for msg in processed_messages):
            processed_messages = [{"role": "system", "content": request_args["system"]}] + processed_messages
            logger.debug("Added system message from system field")

        # Prepare standardized request structure
        standardized_request = {
            "model": request_args.get("model", ""),
            "messages": processed_messages,
            "temperature": request_args.get("temperature"),
            "max_tokens": request_args.get("max_tokens"),
            "top_p": request_args.get("top_p"),
            "frequency_penalty": None,  # Anthropic doesn't use these, but we include for schema consistency
            "presence_penalty": None,
            "stop": request_args.get("stop", None),
            "n": None
        }
        
        # Standardize tools format if present
        if "tools" in request_args:
            standardized_tools = []
            for tool in request_args.get("tools", []):
                standardized_tool = {
                    "name": tool.get("name", ""),
                    "description": tool.get("description", ""),
                    "parameters": {}
                }
                
                # Convert input_schema to parameters
                if "input_schema" in tool:
                    input_schema = tool["input_schema"]
                    standardized_tool["parameters"] = {
                        "type": input_schema.get("type", "object"),
                        "properties": input_schema.get("properties", {}),
                        "required": input_schema.get("required", [])
                    }
                
                standardized_tools.append(standardized_tool)
            
            if standardized_tools:
                standardized_request["tools"] = standardized_tools
                logger.debug(f"Standardized {len(standardized_tools)} tools")

        response_text = ""
        usage = {}
        function_call_info = None
        model = standardized_request.get("model", "")
        
        # Process Anthropic response
        if success and response:
            logger.info("Processing successful response")
            if isinstance(response, dict):
                logger.debug("Response is a dictionary")
                # Response is already a dictionary (likely a SDK response that's been unpacked)
                response_dict = response
                response_text = response.get("error", str(response))
                usage = response.get("usage", {})
            # Handle HTTP response objects from direct API calls
            elif hasattr(response, "json") and callable(response.json):
                logger.debug("Response is a JSON HTTP response")
                try:
                    response_dict = response.json()
                    logger.debug(f"Response keys: {list(response_dict.keys())}")
                    
                    # Extract content from Anthropic API response
                    if "content" in response_dict:
                        logger.debug("Found 'content' in response")
                        # For newer API versions that return a list of content blocks
                        if isinstance(response_dict["content"], list):
                            logger.debug("Content is a list")
                            text_blocks = []
                            tool_calls = []
                            
                            for block in response_dict["content"]:
                                if block.get("type") == "text":
                                    text_content = block.get("text", "")
                                    if text_content:
                                        text_blocks.append(text_content)
                                elif block.get("type") == "tool_use":
                                    tool_use = block.get("tool_use", {})
                                    tool_call = {
                                        "id": tool_use.get("id", str(uuid.uuid4())),
                                        "type": "function",
                                        "function": {
                                            "name": tool_use.get("name", "unknown"),
                                            "arguments": json.dumps(tool_use.get("input", {}))
                                        }
                                    }
                                    tool_calls.append(tool_call)
                                    
                                    # Add formatted version to text blocks
                                    tool_name = tool_use.get("name", "unknown")
                                    try:
                                        formatted_input = json.dumps(tool_use.get("input", {}), indent=2)
                                        tool_text = f"\n[TOOL_CALL: {tool_name}]\n{formatted_input}"
                                        text_blocks.append(tool_text)
                                    except:
                                        text_blocks.append(f"\n[TOOL_CALL: {tool_name}]")
                            
                            # Join text blocks
                            if text_blocks:
                                response_text = "\n".join(text_blocks)
                                logger.debug(f"Created response text from {len(text_blocks)} text blocks")
                            
                            # Store tool calls
                            if tool_calls:
                                function_call_info = {
                                    "calls": tool_calls
                                }
                                logger.debug(f"Processed {len(tool_calls)} tool calls")
                        # For simple text response
                        elif "text" in response_dict:
                            logger.debug("Found 'text' in response")
                            response_text = response_dict["text"]
                        # For completion API
                        elif "completion" in response_dict:
                            logger.debug("Found 'completion' in response")
                            response_text = response_dict["completion"]
                    
                    # Extract usage information if available
                    if "usage" in response_dict:
                        logger.debug("Found 'usage' in response")
                        usage = {
                            "prompt_tokens": response_dict["usage"].get("input_tokens", 0),
                            "completion_tokens": response_dict["usage"].get("output_tokens", 0),
                            "total_tokens": (
                                response_dict["usage"].get("input_tokens", 0) + 
                                response_dict["usage"].get("output_tokens", 0)
                            )
                        }
                        logger.debug(f"Usage: {usage}")
                except Exception as e:
                    logger.error(f"Error processing Anthropic HTTP response: {e}")
                    logger.error(traceback.format_exc())
                    response_text = f"[ERROR_PROCESSING_RESPONSE: {str(e)}]"
            # Original SDK object handling
            elif not isinstance(response, dict):
                logger.debug("Response is an SDK object")
                # Extract usage information if available
                if hasattr(response, "usage"):
                    usage = {
                        "prompt_tokens": getattr(response.usage, "input_tokens", 0),
                        "completion_tokens": getattr(response.usage, "output_tokens", 0),
                        "total_tokens": getattr(response.usage, "input_tokens", 0) + getattr(response.usage, "output_tokens", 0)
                    }
                    logger.debug(f"SDK usage: {usage}")
                
                # Handle content blocks from the response
                if hasattr(response, "content"):
                    logger.debug("Response has 'content' attribute")
                    tool_calls = []
                    text_blocks = []
                    
                    for block in response.content:
                        if hasattr(block, "type"):
                            if block.type == "text":
                                text_content = getattr(block, "text", "") 
                                if text_content:
                                    text_blocks.append(text_content)
                            elif block.type == "tool_use":
                                tool_call = {
                                    "id": getattr(block, "id", str(uuid.uuid4())),
                                    "type": "function",
                                    "function": {
                                        "name": getattr(block, "name", "unknown"),
                                        "arguments": json.dumps(getattr(block, "input", {}))
                                    }
                                }
                                tool_calls.append(tool_call)
                                
                                # Add a formatted version of the tool call to text blocks
                                tool_name = getattr(block, "name", "unknown")
                                tool_input = getattr(block, "input", {})
                                try:
                                    # Format the tool input for better readability
                                    formatted_input = json.dumps(tool_input, indent=2)
                                    tool_text = f"\n[TOOL_CALL: {tool_name}]\n{formatted_input}"
                                    text_blocks.append(tool_text)
                                except:
                                    # Fallback if formatting fails
                                    text_blocks.append(f"\n[TOOL_CALL: {tool_name}]")
                    
                    # Combine all text blocks
                    if text_blocks:
                        response_text = "\n".join(text_blocks)
                        logger.debug(f"Created response text from {len(text_blocks)} SDK text blocks")
                    
                    # If tool calls were found, save them for tool_calls field
                    if tool_calls:
                        function_call_info = {
                            "calls": tool_calls
                        }
                        logger.debug(f"Processed {len(tool_calls)} SDK tool calls")
                        
                        # If we didn't get any content text, create a placeholder
                        if not response_text:
                            response_text = f"[TOOL_CALLS: {len(tool_calls)}]"
        else:
            logger.warning(f"Response processing skipped: success={success}, response exists={response is not None}")
        
        # Count tokens if not provided
        if not usage:
            logger.debug("No usage info provided, estimating token count")
            # Determine if we should use Anthropic-specific token counting
            use_anthropic_counting = any(model.startswith(prefix) for prefix in ANTHROPIC_MODEL_PREFIXES)
            
            if use_anthropic_counting:
                logger.debug("Using Anthropic-specific token counting")
                # Join messages to count prompt tokens
                prompt_text = " ".join(str(msg.get("content", "")) for msg in messages if msg.get("content"))
                
                # Count completion tokens
                resp_text_str = str(response_text) if response_text else ""
                
                # Count tokens using Anthropic-specific method
                prompt_tokens = count_tokens_anthropic(prompt_text, model)
                completion_tokens = count_tokens_anthropic(resp_text_str, model) if resp_text_str else DEFAULT_TOKEN_COUNT
                
                usage = {
                    "prompt_tokens": prompt_tokens.get(TOKEN_COUNT_KEYS["PROMPT_TOKENS"], 0),
                    "completion_tokens": completion_tokens.get(TOKEN_COUNT_KEYS["COMPLETION_TOKENS"], 0),
                    "total_tokens": (
                        prompt_tokens.get(TOKEN_COUNT_KEYS["PROMPT_TOKENS"], 0) + 
                        completion_tokens.get(TOKEN_COUNT_KEYS["COMPLETION_TOKENS"], 0)
                    )
                }
            else:
                logger.debug("Using approximate token counting")
                # Fallback to basic token counting (very rough estimation)
                prompt_text = " ".join(str(msg.get("content", "")) for msg in messages if msg.get("content"))
                resp_text_str = str(response_text) if response_text else ""
                usage = {
                    "prompt_tokens": len(prompt_text) // 4,  # Very rough approximation
                    "completion_tokens": len(resp_text_str) // 4,
                    "total_tokens": (len(prompt_text) + len(resp_text_str)) // 4
                }
        
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

        # Generate log entry with standardized request
        log_entry = create_base_log_entry(provider, standardized_request)
        logger.debug("Created base log entry")
        
        # Add remaining fields
        log_entry.update({
            "response": response_text,
            "usage": standardized_usage,
            "duration": duration,
            "success": success,
        })
        
        # Add tool_calls field if we have function call information
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
            logger.debug(f"Added user_id: {user_id}")

        # Call template matching API and update log entry
        log_entry = process_template_matching(processed_messages, user_id, stack_info, log_entry)
        logger.debug("Applied template matching")

        # Write to log file
        logger.info("Sending log entry to transport")
        send_log(log_entry)
        logger.info("Successfully logged Anthropic call")

    except Exception as e:
        logger.error(f"Error logging Anthropic call: {str(e)}")
        logger.error(traceback.format_exc())

def patched_requests_post(original_post, *args, **kwargs):
    """
    Patched version of requests.post to track direct HTTP calls to Anthropic API.
    """
    url = args[0] if args else kwargs.get('url')
    
    # Only process Anthropic API calls - more permissive check
    if url and isinstance(url, str) and ("anthropic.com" in url or "anthropic.ai" in url):
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
                logger.error(f"Error making Anthropic HTTP request: {str(e)}")
                raise e
            finally:
                duration = time.time() - start_time
                
                # Log all Anthropic API calls
                # We're being more permissive here by not filtering by endpoint path
                logger.info(f"Logging direct Anthropic API call to: {url}")
                log_anthropic_call("anthropic", json_data, response, duration, success)
                    
            return response
        except Exception as e:
            logger.error(f"Error in patched requests.post for Anthropic: {str(e)}")
            logger.error(traceback.format_exc())
            # Let the original request proceed even if tracking fails
            return original_post(*args, **kwargs)
    else:
        # For non-Anthropic URLs, just call the original function
        return original_post(*args, **kwargs)

def setup_anthropic_patching():
    """Set up tracking for Anthropic by patching target methods."""

    try:
        # Patch requests.post for direct HTTP API calls - do this first
        # to ensure it's always patched regardless of SDK availability
        if not getattr(requests.post, '_llm_tracker_patched_anthropic', False):
            logger.info("Patching requests.post for Anthropic API tracking")
            original_post = requests.post
            patched_post = functools.wraps(original_post)(
                lambda *args, **kwargs: patched_requests_post(original_post, *args, **kwargs)
            )
            patched_post._llm_tracker_patched_anthropic = True
            requests.post = patched_post
            logger.info("Successfully patched requests.post for Anthropic API tracking")
        else:
            logger.info("requests.post already patched for Anthropic")

        # Try to import and patch the SDK
        try:
            from anthropic.resources.messages import Messages
            from anthropic.resources.messages import AsyncMessages

            # Patch synchronous Messages.create
            if hasattr(Messages, "create") and not getattr(Messages.create, '_llm_tracker_patched', False):
                original_messages_create = Messages.create
                
                # Create the wrapped version using our helper function
                patched_messages_create = create_generic_method_wrapper(
                    original_messages_create, 
                    "anthropic", 
                    log_anthropic_call
                )
                
                # Replace the original method with the patched one
                Messages.create = patched_messages_create
                logger.info("Successfully patched Anthropic Messages.create")
            elif hasattr(Messages, "create") and getattr(Messages.create, '_llm_tracker_patched', False):
                logger.debug("Anthropic Messages.create already patched.")
            else:
                logger.warning("Could not find 'create' method on Anthropic Messages class for patching.")
            
            # Patch asynchronous AsyncMessages.create
            if hasattr(AsyncMessages, "create") and not getattr(AsyncMessages.create, '_llm_tracker_patched', False):
                original_async_messages_create = AsyncMessages.create
                
                # Create an async-compatible wrapped version
                patched_async_messages_create = create_async_method_wrapper(
                    original_async_messages_create, 
                    "anthropic", 
                    log_anthropic_call
                )
                
                # Replace the original method with the patched one
                AsyncMessages.create = patched_async_messages_create
                logger.info("Successfully patched Anthropic AsyncMessages.create")
            elif hasattr(AsyncMessages, "create") and getattr(AsyncMessages.create, '_llm_tracker_patched', False):
                logger.debug("Anthropic AsyncMessages.create already patched.")
            else:
                logger.warning("Could not find 'create' method on Anthropic AsyncMessages class for patching.")
        except ImportError:
            logger.warning("Could not import 'anthropic.resources.messages'. Only direct API calls will be tracked.")
    except Exception as e:
        logger.error(f"Failed during Anthropic patching process: {e}")
        logger.error(traceback.format_exc())