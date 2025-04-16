import traceback
from typing import Any, Callable, Dict, Optional, List, Tuple, TypeVar, Generic
import ast
import os
from loguru import logger

from .constants import EXCLUDED_STACK_FRAME_PATTERNS, SOURCE_CACHE

def get_source_code(filename: str) -> Optional[str]:
    """Get source code from a file, with caching"""
    if filename in SOURCE_CACHE:
        return SOURCE_CACHE[filename]
    
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                source = f.read()
                SOURCE_CACHE[filename] = source
                return source
    except Exception as e:
        logger.warning(f"Failed to read source file {filename}: {e}")
    
    return None

def get_imported_value(module_path: str, var_name: str) -> Any:
    """Get the value of an imported variable by reading and parsing its module."""
    try:
        # Convert module path to file path
        module_path = module_path.replace('.', '/')
        if not module_path.endswith('.py'):
            module_path += '.py'
        
        # Try to find the module in the project
        possible_paths = [
            os.path.join(os.getcwd(), 'src', module_path),
            os.path.join(os.getcwd(), module_path),
            os.path.join(os.path.dirname(__file__), '..', module_path)
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    source = f.read()
                    tree = ast.parse(source)
                    
                    # Look for assignments to the variable
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Assign):
                            for target in node.targets:
                                if isinstance(target, ast.Name) and target.id == var_name:
                                    # Try to evaluate the value
                                    try:
                                        # Create a new namespace for evaluation
                                        namespace = {}
                                        exec(compile(ast.Module(body=[node], type_ignores=[]), 
                                                    filename=path, mode='exec'), namespace)
                                        return namespace.get(var_name)
                                    except Exception as e:
                                        logger.debug(f"Failed to evaluate value for {var_name}: {e}")
                                        return ast.unparse(node.value)
        return None
    except Exception as e:
        logger.debug(f"Failed to get imported value for {module_path}.{var_name}: {e}")
        return None

def get_runtime_value(obj: Any, disable_repr: bool = False) -> str:
    """
    Safely get a string representation of a runtime value, handling various types.
    If the object is a complex type like dict or list, include its structure but limit item count.
    If disable_repr is True, don't use str or repr at all to avoid triggering side effects.
    """
    try:
        if disable_repr:
            return f"{type(obj).__name__}"
            
        if obj is None:
            return "None"
        elif isinstance(obj, (str, int, float, bool)):
            # For primitive types, just use the string representation
            return str(obj)
        elif isinstance(obj, (list, tuple)):
            # For lists and tuples, show type and length, plus a few sample items
            sample_count = min(3, len(obj))
            samples = []
            for i in range(sample_count):
                try:
                    item_value = get_runtime_value(obj[i], True)  # Avoid nested repr
                    samples.append(item_value)
                except Exception:
                    samples.append("?")
            
            return f"{type(obj).__name__}[{', '.join(samples)}...] (len={len(obj)})"
        elif isinstance(obj, dict):
            # For dictionaries, show type and a few sample keys
            sample_count = min(3, len(obj))
            samples = []
            for i, (k, v) in enumerate(obj.items()):
                if i >= sample_count:
                    break
                try:
                    key_str = str(k) if isinstance(k, (str, int, float, bool)) else f"{type(k).__name__}"
                    val_str = get_runtime_value(v, True)  # Avoid nested repr
                    samples.append(f"{key_str}: {val_str}")
                except Exception:
                    samples.append(f"{key_str}: ?")
            
            return f"{type(obj).__name__}{{{', '.join(samples)}...}} (len={len(obj)})"
        else:
            # For other types, just show the type name and a brief representation
            try:
                brief_repr = str(obj)
                if len(brief_repr) > 100:
                    brief_repr = brief_repr[:97] + "..."
                return f"{type(obj).__name__}({brief_repr})"
            except Exception:
                return f"{type(obj).__name__}(?)"
    except Exception as e:
        logger.debug(f"Failed to get runtime value: {e}")
        return f"<error getting value: {str(e)[:50]}>"

def evaluate_complex_expression(expr: str, frame_locals: Dict[str, Any], frame_globals: Dict[str, Any]) -> Any:
    """
    Try to evaluate a complex expression using the frame's locals and globals.
    Returns the result of evaluation or None if it fails.
    """
    try:
        # Make a safe copy of the dictionaries to avoid modifying the originals
        safe_locals = dict(frame_locals)
        safe_globals = dict(frame_globals)
        # Try to evaluate the expression
        result = eval(expr, safe_globals, safe_locals)
        return result
    except Exception as e:
        logger.debug(f"Failed to evaluate expression '{expr}': {e}")
        return None

def extract_runtime_values(node: ast.AST, frame_locals: Dict[str, Any], frame_globals: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract runtime values from an AST node by evaluating expressions.
    Focuses on capturing values of complex expressions like chained method calls.
    """
    try:
        # Try to convert the node to a string representation
        expr = ast.unparse(node)
        runtime_value = None
        
        # For simple variable names, just look them up directly
        if isinstance(node, ast.Name):
            var_name = node.id
            if var_name in frame_locals:
                runtime_value = frame_locals[var_name]
            elif var_name in frame_globals:
                runtime_value = frame_globals[var_name]
        
        # For attributes and method calls, try to evaluate the full expression
        elif isinstance(node, (ast.Attribute, ast.Call, ast.Subscript)):
            runtime_value = evaluate_complex_expression(expr, frame_locals, frame_globals)
        
        # For constants, just use the value directly
        elif isinstance(node, ast.Constant):
            runtime_value = node.value
            
        # Convert the runtime value to a string representation
        runtime_value_str = get_runtime_value(runtime_value)
        
        return {
            "expr": expr,
            "runtime_value": runtime_value,
            "runtime_value_str": runtime_value_str,
            "type": type(runtime_value).__name__ if runtime_value is not None else None
        }
    except Exception as e:
        logger.debug(f"Failed to extract runtime value: {e}")
        return {
            "expr": ast.unparse(node) if isinstance(node, ast.AST) else str(node),
            "runtime_value": None,
            "runtime_value_str": f"<error: {str(e)[:50]}>",
            "type": None
        }

def format_stack_trace(stack_frames: List[traceback.FrameSummary]) -> List[Dict[str, Any]]:
    """Format stack trace frames into a list of dictionaries with relevant information."""
    formatted_frames = []
    project_root = os.getcwd()
    excluded_patterns = EXCLUDED_STACK_FRAME_PATTERNS

    for frame in reversed(stack_frames):
        filename = frame.filename
        abs_filename = os.path.abspath(filename)

        # Skip frames matching excluded patterns
        if any(pattern in filename for pattern in excluded_patterns):
            continue

        # Skip frames outside project directory
        if not abs_filename.startswith(project_root):
            continue

        # Get function name from frame name attribute
        function_name = frame.name if hasattr(frame, 'name') else "unknown"
        
        # Get source code context and analyze it
        source_code = get_source_code(filename)
        code_context = []
        imports = []
        globals_used = []
        referenced_code = []
        imported_vars = {}
        message_arrays = {}  # Dictionary to track message arrays
        global_vars = {}     # Dictionary to track global variables
        string_to_var_map = {}  # Map string literals to their variable names
        runtime_values = {}  # Dictionary to track runtime values of expressions
        
        # Get local variables if available for runtime evaluation
        local_vars = {}
        if hasattr(frame, 'f_locals'):
            try:
                # Keep the actual objects for evaluation, not just string representations
                local_vars = frame.f_locals
            except Exception as e:
                logger.warning(f"Failed to get local variables: {e}")

        # Get global variables if available for runtime evaluation
        global_vars_raw = {}
        if hasattr(frame, 'f_globals'):
            try:
                global_vars_raw = frame.f_globals
            except Exception as e:
                logger.warning(f"Failed to get global variables: {e}")
        
        if source_code:
            try:
                # Get the AST to find function definitions and analyze the code
                tree = ast.parse(source_code)
                
                # Find the current function
                current_function = None
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef) and node.name == function_name:
                        current_function = node
                        # Get the function's source code
                        start_line = node.lineno
                        end_line = node.end_lineno
                        lines = source_code.split('\n')
                        code_context = lines[max(0, start_line-2):min(len(lines), end_line+2)]
                        break
                
                # First pass: collect all imports and their aliases
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for name in node.names:
                            imported_vars[name.asname or name.name] = {
                                "module": name.name,
                                "alias": name.asname,
                                "line": node.lineno,
                                "value": get_imported_value(name.name, name.name)
                            }
                    elif isinstance(node, ast.ImportFrom):
                        for name in node.names:
                            imported_vars[name.asname or name.name] = {
                                "module": f"{node.module}.{name.name}",
                                "alias": name.asname,
                                "line": node.lineno,
                                "value": get_imported_value(node.module, name.name)
                            }
                
                # First scan all assignments to build the map of string values to variable names
                for node in ast.walk(tree):
                    if isinstance(node, ast.Assign):
                        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                            # Map the string value to the variable name
                            for target in node.targets:
                                if isinstance(target, ast.Name):
                                    # Store both the variable name and whether it's a global (outside any function)
                                    is_global = not any(
                                        isinstance(parent, ast.FunctionDef) 
                                        for parent in ast.walk(tree) 
                                        if hasattr(parent, 'body') and node in ast.walk(ast.Module(body=parent.body, type_ignores=[]))
                                    )
                                    string_to_var_map[node.value.value] = {
                                        "name": target.id,
                                        "is_global": is_global,
                                        "line": node.lineno
                                    }
                
                # Analyze global variables in the module (outside of any function)
                for node in ast.walk(tree):
                    # Only process top-level assignments (not inside functions)
                    if isinstance(node, ast.Assign):
                        in_function = False
                        for func_node in ast.walk(tree):
                            if isinstance(func_node, ast.FunctionDef) and hasattr(func_node, 'body'):
                                if node in ast.walk(ast.Module(body=func_node.body, type_ignores=[])):
                                    in_function = True
                                    break
                        
                        if not in_function:  # It's a global assignment
                            for target in node.targets:
                                if isinstance(target, ast.Name):
                                    var_name = target.id
                                    # Try to extract the value
                                    if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                                        # String constant
                                        global_vars[var_name] = {
                                            "type": "constant",
                                            "value": node.value.value,
                                            "line": node.lineno
                                        }
                                        # Also add to referenced_code for template matching
                                        referenced_code.append({
                                            "type": "constant",
                                            "name": var_name, 
                                            "value": node.value.value,
                                            "line": node.lineno,
                                            "global_var_info": {
                                                "type": "constant",
                                                "value": node.value.value,
                                                "line": node.lineno
                                            }
                                        })
                                    elif isinstance(node.value, ast.JoinedStr):
                                        # This is an f-string
                                        try:
                                            f_string_src = ast.unparse(node.value)
                                            global_vars[var_name] = {
                                                "type": "f_string",
                                                "value": f_string_src,
                                                "line": node.lineno
                                            }
                                            # Also add to referenced_code
                                            referenced_code.append({
                                                "type": "f_string",
                                                "name": var_name,
                                                "value": f_string_src,
                                                "line": node.lineno,
                                                "global_var_info": {
                                                    "type": "f_string",
                                                    "value": f_string_src,
                                                    "line": node.lineno
                                                }
                                            })
                                        except Exception:
                                            pass
                
                # Second pass: look for LLM message arrays
                for node in ast.walk(tree):
                    if isinstance(node, ast.Assign):
                        # Check if this is assigning a list
                        if isinstance(node.value, ast.List):
                            # Get the target variable name
                            target_name = None
                            if isinstance(node.targets[0], ast.Name):
                                target_name = node.targets[0].id
                            elif isinstance(node.targets[0], ast.Attribute):
                                try:
                                    target_name = f"{ast.unparse(node.targets[0].value)}.{node.targets[0].attr}"
                                except Exception:
                                    pass
                            
                            if target_name:
                                # Check if the list contains message dictionaries
                                is_message_array = False
                                message_contents = []
                                
                                for elt in node.value.elts:
                                    if isinstance(elt, ast.Dict):
                                        # Check for key-value pairs like {"role": "...", "content": "..."}
                                        keys = []
                                        for k, v in zip(elt.keys, elt.values):
                                            if isinstance(k, ast.Constant) and isinstance(k.value, str):
                                                keys.append(k.value)
                                        
                                        if "role" in keys and "content" in keys:
                                            is_message_array = True
                                            
                                            # Extract content value if it's a constant or f-string
                                            for k, v in zip(elt.keys, elt.values):
                                                if isinstance(k, ast.Constant) and k.value == "content":
                                                    if isinstance(v, ast.Constant) and isinstance(v.value, str):
                                                        message_contents.append({
                                                            "type": "constant",
                                                            "value": v.value,
                                                            "line": v.lineno if hasattr(v, "lineno") else node.lineno
                                                        })
                                                    elif isinstance(v, ast.JoinedStr):
                                                        # This is an f-string
                                                        try:
                                                            # Get the original source for this f-string
                                                            f_string_src = ast.unparse(v)
                                                            message_contents.append({
                                                                "type": "f_string",
                                                                "value": f_string_src,
                                                                "line": v.lineno if hasattr(v, "lineno") else node.lineno
                                                            })
                                                        except Exception:
                                                            pass
                                
                                if is_message_array and message_contents:
                                    message_arrays[target_name] = {
                                        "line": node.lineno,
                                        "contents": message_contents
                                    }
                
                # Third pass: analyze the entire file and extract runtime values
                for node in ast.walk(tree):
                    # Collect global variables
                    if isinstance(node, ast.Global):
                        globals_used.extend(node.names)
                    
                    # If we found the current function, analyze its body
                    if current_function and node in ast.walk(current_function):
                        # Look for function calls
                        if isinstance(node, ast.Call):
                            try:
                                # Extract runtime values for this function call
                                runtime_info = extract_runtime_values(node, local_vars, global_vars_raw)
                                expr_id = f"call_{node.lineno}_{getattr(node, 'col_offset', 0)}"
                                runtime_values[expr_id] = runtime_info
                                
                                if isinstance(node.func, ast.Name):
                                    referenced_code.append({
                                        "type": "function_call",
                                        "name": node.func.id,
                                        "line": node.lineno,
                                        "args": [ast.unparse(arg) for arg in node.args],
                                        "keywords": [f"{kw.arg}={ast.unparse(kw.value)}" for kw in node.keywords],
                                        "runtime_values_key": expr_id
                                    })
                                    
                                    # Also try to evaluate each argument individually
                                    for i, arg in enumerate(node.args):
                                        arg_runtime = extract_runtime_values(arg, local_vars, global_vars_raw)
                                        arg_id = f"{expr_id}_arg_{i}"
                                        runtime_values[arg_id] = arg_runtime
                                    
                                    # And each keyword argument
                                    for i, kw in enumerate(node.keywords):
                                        kw_runtime = extract_runtime_values(kw.value, local_vars, global_vars_raw)
                                        kw_id = f"{expr_id}_kw_{kw.arg}"
                                        runtime_values[kw_id] = kw_runtime
                                        
                                elif isinstance(node.func, ast.Attribute):
                                    value = ast.unparse(node.func.value)
                                    
                                    # Extract runtime value of the attribute's base object
                                    value_runtime = extract_runtime_values(node.func.value, local_vars, global_vars_raw)
                                    value_id = f"{expr_id}_base"
                                    runtime_values[value_id] = value_runtime
                                    
                                    referenced_code.append({
                                        "type": "method_call",
                                        "name": f"{value}.{node.func.attr}",
                                        "line": node.lineno,
                                        "args": [ast.unparse(arg) for arg in node.args],
                                        "keywords": [f"{kw.arg}={ast.unparse(kw.value)}" for kw in node.keywords],
                                        "runtime_values_key": expr_id,
                                        "base_obj_runtime_values_key": value_id
                                    })
                                    
                                    # Also try to evaluate each argument individually
                                    for i, arg in enumerate(node.args):
                                        arg_runtime = extract_runtime_values(arg, local_vars, global_vars_raw)
                                        arg_id = f"{expr_id}_arg_{i}"
                                        runtime_values[arg_id] = arg_runtime
                                    
                                    # And each keyword argument
                                    for i, kw in enumerate(node.keywords):
                                        kw_runtime = extract_runtime_values(kw.value, local_vars, global_vars_raw)
                                        kw_id = f"{expr_id}_kw_{kw.arg}"
                                        runtime_values[kw_id] = kw_runtime
                                        
                                elif isinstance(node.func, ast.Call):
                                    # This is a nested call like (supabase.table('demo')).select()
                                    # We already have the full expression's runtime value, but also get the inner call
                                    inner_runtime = extract_runtime_values(node.func, local_vars, global_vars_raw)
                                    inner_id = f"{expr_id}_inner"
                                    runtime_values[inner_id] = inner_runtime
                                    
                                    referenced_code.append({
                                        "type": "nested_call",
                                        "name": ast.unparse(node.func),
                                        "line": node.lineno,
                                        "args": [ast.unparse(arg) for arg in node.args],
                                        "keywords": [f"{kw.arg}={ast.unparse(kw.value)}" for kw in node.keywords],
                                        "runtime_values_key": expr_id,
                                        "inner_call_runtime_values_key": inner_id
                                    })
                            except Exception as e:
                                logger.debug(f"Failed to process function call: {e}")
                        
                        # Look for variable references
                        if isinstance(node, ast.Name):
                            # Extract runtime value for this variable
                            runtime_info = extract_runtime_values(node, local_vars, global_vars_raw)
                            expr_id = f"var_{node.lineno}_{getattr(node, 'col_offset', 0)}"
                            runtime_values[expr_id] = runtime_info
                            
                            ref_info = {
                                "type": "variable_reference",
                                "name": node.id,
                                "line": node.lineno,
                                "runtime_values_key": expr_id
                            }
                            # Check if it's an imported variable
                            if node.id in imported_vars:
                                ref_info["import_info"] = imported_vars[node.id]
                            # Check if it's a message array
                            if node.id in message_arrays:
                                ref_info["message_array_info"] = message_arrays[node.id]
                            # Check if it's a global variable
                            if node.id in global_vars:
                                ref_info["global_var_info"] = global_vars[node.id]
                            referenced_code.append(ref_info)
                        
                        # Look for attribute access
                        if isinstance(node, ast.Attribute):
                            try:
                                # Extract runtime value for this attribute access
                                runtime_info = extract_runtime_values(node, local_vars, global_vars_raw)
                                expr_id = f"attr_{node.lineno}_{getattr(node, 'col_offset', 0)}"
                                runtime_values[expr_id] = runtime_info
                                
                                # Also get runtime value of the base object
                                base_runtime = extract_runtime_values(node.value, local_vars, global_vars_raw)
                                base_id = f"{expr_id}_base"
                                runtime_values[base_id] = base_runtime
                                
                                value = ast.unparse(node.value)
                                ref_info = {
                                    "type": "attribute_access",
                                    "name": f"{value}.{node.attr}",
                                    "line": node.lineno,
                                    "runtime_values_key": expr_id,
                                    "base_obj_runtime_values_key": base_id
                                }
                                # Check if it's an imported module attribute
                                if value in imported_vars:
                                    ref_info["import_info"] = imported_vars[value]
                                referenced_code.append(ref_info)
                            except Exception as e:
                                logger.debug(f"Failed to process attribute access: {e}")
                        
                        # Look for constants
                        if isinstance(node, ast.Constant):
                            referenced_code.append({
                                "type": "constant",
                                "name": str(node.value),
                                "line": node.lineno,
                                "value": node.value
                            })
                        
                        # Look for assignments
                        if isinstance(node, ast.Assign):
                            # Extract runtime value for the right side of the assignment
                            runtime_info = extract_runtime_values(node.value, local_vars, global_vars_raw)
                            expr_id = f"assign_{node.lineno}_{getattr(node, 'col_offset', 0)}"
                            runtime_values[expr_id] = runtime_info
                            
                            for target in node.targets:
                                if isinstance(target, ast.Name):
                                    ref_info = {
                                        "type": "assignment",
                                        "name": target.id,
                                        "line": node.lineno,
                                        "value": ast.unparse(node.value),
                                        "runtime_values_key": expr_id
                                    }
                                    # Check if it's an imported variable
                                    if target.id in imported_vars:
                                        ref_info["import_info"] = imported_vars[target.id]
                                    # Check if it's a message array
                                    if target.id in message_arrays:
                                        ref_info["message_array_info"] = message_arrays[target.id]
                                    referenced_code.append(ref_info)
                                elif isinstance(target, ast.Attribute):
                                    try:
                                        value = ast.unparse(target.value)
                                        ref_info = {
                                            "type": "attribute_assignment",
                                            "name": f"{value}.{target.attr}",
                                            "line": node.lineno,
                                            "value": ast.unparse(node.value),
                                            "runtime_values_key": expr_id
                                        }
                                        # Check if it's an imported module attribute
                                        if value in imported_vars:
                                            ref_info["import_info"] = imported_vars[value]
                                        referenced_code.append(ref_info)
                                    except Exception as e:
                                        logger.debug(f"Failed to process attribute assignment: {e}")
                        
                        # Look for subscript expressions (indexing/slicing)
                        if isinstance(node, ast.Subscript):
                            try:
                                # Extract runtime value for this subscript expression
                                runtime_info = extract_runtime_values(node, local_vars, global_vars_raw)
                                expr_id = f"subscript_{node.lineno}_{getattr(node, 'col_offset', 0)}"
                                runtime_values[expr_id] = runtime_info
                                
                                # Also get runtime value of the base object being subscripted
                                base_runtime = extract_runtime_values(node.value, local_vars, global_vars_raw)
                                base_id = f"{expr_id}_base"
                                runtime_values[base_id] = base_runtime
                                
                                # And get the index/slice value
                                slice_runtime = extract_runtime_values(node.slice, local_vars, global_vars_raw)
                                slice_id = f"{expr_id}_slice"
                                runtime_values[slice_id] = slice_runtime
                                
                                value = ast.unparse(node.value)
                                slice_str = ast.unparse(node.slice)
                                referenced_code.append({
                                    "type": "subscript",
                                    "name": f"{value}[{slice_str}]",
                                    "line": node.lineno,
                                    "runtime_values_key": expr_id,
                                    "base_obj_runtime_values_key": base_id,
                                    "slice_runtime_values_key": slice_id
                                })
                            except Exception as e:
                                logger.debug(f"Failed to process subscript: {e}")
                                
                        # Look for chained expressions that might be used for template substitution
                        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
                            try:
                                # This could be a string concatenation
                                runtime_info = extract_runtime_values(node, local_vars, global_vars_raw)
                                expr_id = f"binop_{node.lineno}_{getattr(node, 'col_offset', 0)}"
                                runtime_values[expr_id] = runtime_info
                                
                                # Also evaluate the left and right sides
                                left_runtime = extract_runtime_values(node.left, local_vars, global_vars_raw)
                                left_id = f"{expr_id}_left"
                                runtime_values[left_id] = left_runtime
                                
                                right_runtime = extract_runtime_values(node.right, local_vars, global_vars_raw)
                                right_id = f"{expr_id}_right"
                                runtime_values[right_id] = right_runtime
                                
                                referenced_code.append({
                                    "type": "binary_operation",
                                    "name": ast.unparse(node),
                                    "line": node.lineno,
                                    "runtime_values_key": expr_id,
                                    "left_runtime_values_key": left_id,
                                    "right_runtime_values_key": right_id
                                })
                            except Exception as e:
                                logger.debug(f"Failed to process binary operation: {e}")
                                
                        # Look for conditional expressions (ternary operators)
                        if isinstance(node, ast.IfExp):
                            try:
                                # Extract runtime value for this conditional expression
                                runtime_info = extract_runtime_values(node, local_vars, global_vars_raw)
                                expr_id = f"ifexp_{node.lineno}_{getattr(node, 'col_offset', 0)}"
                                runtime_values[expr_id] = runtime_info
                                
                                # Also evaluate the condition, true branch, and false branch
                                test_runtime = extract_runtime_values(node.test, local_vars, global_vars_raw)
                                test_id = f"{expr_id}_test"
                                runtime_values[test_id] = test_runtime
                                
                                body_runtime = extract_runtime_values(node.body, local_vars, global_vars_raw)
                                body_id = f"{expr_id}_body"
                                runtime_values[body_id] = body_runtime
                                
                                orelse_runtime = extract_runtime_values(node.orelse, local_vars, global_vars_raw)
                                orelse_id = f"{expr_id}_orelse"
                                runtime_values[orelse_id] = orelse_runtime
                                
                                referenced_code.append({
                                    "type": "conditional_expression",
                                    "name": ast.unparse(node),
                                    "line": node.lineno,
                                    "runtime_values_key": expr_id,
                                    "test_runtime_values_key": test_id,
                                    "body_runtime_values_key": body_id,
                                    "orelse_runtime_values_key": orelse_id
                                })
                            except Exception as e:
                                logger.debug(f"Failed to process conditional expression: {e}")
            except Exception as e:
                logger.warning(f"Failed to parse AST for {filename}: {e}")
                code_context = frame.code_context if hasattr(frame, "code_context") and frame.code_context else []

        # Filter and sanitize local variables for the output
        local_vars_output = {}
        if hasattr(frame, 'f_locals'):
            try:
                # Filter out internal variables and large objects
                local_vars_output = {
                    k: get_runtime_value(v)
                    for k, v in frame.f_locals.items()
                    if not k.startswith('__')
                }
            except Exception as e:
                logger.warning(f"Failed to get local variables for output: {e}")

        # Filter and sanitize global variables for the output
        global_vars_output = {}
        if hasattr(frame, 'f_globals'):
            try:
                global_vars_output = {
                    k: get_runtime_value(v)
                    for k, v in frame.f_globals.items()
                    if not k.startswith('__')
                }
            except Exception as e:
                logger.warning(f"Failed to get global variables for output: {e}")

        formatted_frame = {
            "filename": frame.filename,
            "lineno": frame.lineno,
            "function": function_name,
            "code_context": code_context,
            "local_vars": local_vars_output,
            "global_vars": global_vars_output,
            "imports": imports,
            "globals_used": globals_used,
            "referenced_code": referenced_code,
            "imported_vars": imported_vars,
            "message_arrays": message_arrays,
            "runtime_values": runtime_values,
            "module": frame.module if hasattr(frame, 'module') else None,
            "colno": frame.colno if hasattr(frame, 'colno') else None,
            "index": frame.index if hasattr(frame, 'index') else None
        }
        formatted_frames.append(formatted_frame)
    return formatted_frames
