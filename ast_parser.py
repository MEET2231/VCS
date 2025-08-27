"""
AST Parser for SVCS.
Converts Python source code to a structured AST representation.
"""

import ast
import json
from typing import Any, Dict, List, Union


def parse_ast(filepath: str) -> Dict[str, Any]:
    """
    Parse a Python file and return its AST structure in JSON-like format.
    
    Args:
        filepath: Path to the Python file to parse
        
    Returns:
        Dictionary representing the AST structure
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        tree = ast.parse(source_code, filename=filepath)
        return ast_to_dict(tree)
    
    except SyntaxError as e:
        raise Exception(f"Syntax error in {filepath}: {e}")
    except Exception as e:
        raise Exception(f"Error parsing {filepath}: {e}")


def ast_to_dict(node: ast.AST) -> Dict[str, Any]:
    """
    Convert an AST node to a dictionary representation.
    
    Args:
        node: AST node to convert
        
    Returns:
        Dictionary representation of the AST node
    """
    if node is None:
        return None
    
    result = {
        'type': node.__class__.__name__
    }
    
    # Add location information if available
    if hasattr(node, 'lineno'):
        result['lineno'] = node.lineno
    if hasattr(node, 'col_offset'):
        result['col_offset'] = node.col_offset
    
    # Process node fields
    for field, value in ast.iter_fields(node):
        if isinstance(value, list):
            result[field] = [ast_to_dict(item) if isinstance(item, ast.AST) else item for item in value]
        elif isinstance(value, ast.AST):
            result[field] = ast_to_dict(value)
        else:
            result[field] = value
    
    return result


def extract_semantic_elements(ast_dict: Dict[str, Any]) -> Dict[str, List[Dict]]:
    """
    Extract semantic elements from AST for easier comparison.
    
    Args:
        ast_dict: AST dictionary representation
        
    Returns:
        Dictionary with semantic elements grouped by type
    """
    elements = {
        'functions': [],
        'classes': [],
        'assignments': [],
        'imports': []
    }
    
    def traverse(node):
        if not isinstance(node, dict) or 'type' not in node:
            return
        
        node_type = node['type']
        
        if node_type == 'FunctionDef':
            func_info = {
                'name': node.get('name'),
                'args': _extract_function_args(node.get('args', {})),
                'returns': _extract_return_info(node.get('body', [])),
                'lineno': node.get('lineno')
            }
            elements['functions'].append(func_info)
        
        elif node_type == 'ClassDef':
            class_info = {
                'name': node.get('name'),
                'bases': _extract_bases(node.get('bases', [])),
                'methods': _extract_methods(node.get('body', [])),
                'lineno': node.get('lineno')
            }
            elements['classes'].append(class_info)
        
        elif node_type == 'Assign':
            for target in node.get('targets', []):
                if isinstance(target, dict) and target.get('type') == 'Name':
                    assign_info = {
                        'target': target.get('id'),
                        'value_type': node.get('value', {}).get('type'),
                        'lineno': node.get('lineno')
                    }
                    elements['assignments'].append(assign_info)
        
        elif node_type in ['Import', 'ImportFrom']:
            import_info = {
                'type': node_type,
                'module': node.get('module'),
                'names': [alias.get('name') for alias in node.get('names', []) if isinstance(alias, dict)],
                'lineno': node.get('lineno')
            }
            elements['imports'].append(import_info)
        
        # Recursively traverse child nodes
        for key, value in node.items():
            if isinstance(value, list):
                for item in value:
                    traverse(item)
            elif isinstance(value, dict):
                traverse(value)
    
    traverse(ast_dict)
    return elements


def _extract_function_args(args_node: Dict) -> List[str]:
    """Extract function argument names."""
    if not isinstance(args_node, dict):
        return []
    
    arg_names = []
    for arg in args_node.get('args', []):
        if isinstance(arg, dict) and 'arg' in arg:
            arg_names.append(arg['arg'])
    
    return arg_names


def _extract_return_info(body: List[Dict]) -> Union[str, None]:
    """Extract return statement information from function body."""
    for stmt in body:
        if isinstance(stmt, dict) and stmt.get('type') == 'Return':
            value = stmt.get('value')
            if isinstance(value, dict):
                if value.get('type') == 'Constant':
                    return str(value.get('value'))
                elif value.get('type') == 'Name':
                    return value.get('id')
                else:
                    return value.get('type')
    return None


def _extract_bases(bases: List[Dict]) -> List[str]:
    """Extract base class names."""
    base_names = []
    for base in bases:
        if isinstance(base, dict) and base.get('type') == 'Name':
            base_names.append(base.get('id'))
    return base_names


def _extract_methods(body: List[Dict]) -> List[str]:
    """Extract method names from class body."""
    methods = []
    for item in body:
        if isinstance(item, dict) and item.get('type') == 'FunctionDef':
            methods.append(item.get('name'))
    return methods
