"""
AST Diff module for SVCS.
Compares two AST structures and generates semantic change descriptions.
"""

from typing import Dict, List, Any
from ast_parser import extract_semantic_elements


def diff_ast(old_ast: Dict[str, Any], new_ast: Dict[str, Any]) -> List[str]:
    """
    Compare two AST structures and return semantic changes.
    
    Args:
        old_ast: Previous AST structure
        new_ast: Current AST structure
        
    Returns:
        List of semantic change descriptions
    """
    changes = []
    
    # Extract semantic elements from both ASTs
    old_elements = extract_semantic_elements(old_ast)
    new_elements = extract_semantic_elements(new_ast)
    
    # Compare functions
    changes.extend(_diff_functions(old_elements['functions'], new_elements['functions']))
    
    # Compare classes
    changes.extend(_diff_classes(old_elements['classes'], new_elements['classes']))
    
    # Compare assignments
    changes.extend(_diff_assignments(old_elements['assignments'], new_elements['assignments']))
    
    # Compare imports
    changes.extend(_diff_imports(old_elements['imports'], new_elements['imports']))
    
    return changes


def _diff_functions(old_functions: List[Dict], new_functions: List[Dict]) -> List[str]:
    """Compare function definitions between old and new AST."""
    changes = []
    
    # Create lookup dictionaries
    old_func_dict = {func['name']: func for func in old_functions}
    new_func_dict = {func['name']: func for func in new_functions}
    
    # Find added functions
    for func_name in new_func_dict:
        if func_name not in old_func_dict:
            changes.append(f"Function `{func_name}` added")
    
    # Find removed functions
    for func_name in old_func_dict:
        if func_name not in new_func_dict:
            changes.append(f"Function `{func_name}` removed")
    
    # Find modified functions
    for func_name in old_func_dict:
        if func_name in new_func_dict:
            old_func = old_func_dict[func_name]
            new_func = new_func_dict[func_name]
            
            func_changes = _compare_function_details(old_func, new_func)
            changes.extend(func_changes)
    
    return changes


def _compare_function_details(old_func: Dict, new_func: Dict) -> List[str]:
    """Compare details of a specific function."""
    changes = []
    func_name = old_func['name']
    
    # Compare arguments
    old_args = set(old_func.get('args', []))
    new_args = set(new_func.get('args', []))
    
    if old_args != new_args:
        if len(new_args) > len(old_args):
            changes.append(f"Function `{func_name}` signature modified (arguments added)")
        elif len(new_args) < len(old_args):
            changes.append(f"Function `{func_name}` signature modified (arguments removed)")
        else:
            changes.append(f"Function `{func_name}` signature modified (arguments changed)")
    
    # Compare return values
    old_return = old_func.get('returns')
    new_return = new_func.get('returns')
    
    if old_return != new_return:
        if old_return is None and new_return is not None:
            changes.append(f"Function `{func_name}` modified (return statement added)")
        elif old_return is not None and new_return is None:
            changes.append(f"Function `{func_name}` modified (return statement removed)")
        else:
            changes.append(f"Function `{func_name}` modified (return value changed)")
    
    return changes


def _diff_classes(old_classes: List[Dict], new_classes: List[Dict]) -> List[str]:
    """Compare class definitions between old and new AST."""
    changes = []
    
    # Create lookup dictionaries
    old_class_dict = {cls['name']: cls for cls in old_classes}
    new_class_dict = {cls['name']: cls for cls in new_classes}
    
    # Find added classes
    for class_name in new_class_dict:
        if class_name not in old_class_dict:
            changes.append(f"Class `{class_name}` added")
    
    # Find removed classes
    for class_name in old_class_dict:
        if class_name not in new_class_dict:
            changes.append(f"Class `{class_name}` removed")
    
    # Find modified classes
    for class_name in old_class_dict:
        if class_name in new_class_dict:
            old_class = old_class_dict[class_name]
            new_class = new_class_dict[class_name]
            
            class_changes = _compare_class_details(old_class, new_class)
            changes.extend(class_changes)
    
    return changes


def _compare_class_details(old_class: Dict, new_class: Dict) -> List[str]:
    """Compare details of a specific class."""
    changes = []
    class_name = old_class['name']
    
    # Compare base classes
    old_bases = set(old_class.get('bases', []))
    new_bases = set(new_class.get('bases', []))
    
    if old_bases != new_bases:
        changes.append(f"Class `{class_name}` inheritance modified")
    
    # Compare methods
    old_methods = set(old_class.get('methods', []))
    new_methods = set(new_class.get('methods', []))
    
    added_methods = new_methods - old_methods
    removed_methods = old_methods - new_methods
    
    for method in added_methods:
        changes.append(f"Method `{method}` added to class `{class_name}`")
    
    for method in removed_methods:
        changes.append(f"Method `{method}` removed from class `{class_name}`")
    
    return changes


def _diff_assignments(old_assignments: List[Dict], new_assignments: List[Dict]) -> List[str]:
    """Compare variable assignments between old and new AST."""
    changes = []
    
    # Create lookup dictionaries by variable name
    old_assign_dict = {}
    for assign in old_assignments:
        target = assign.get('target')
        if target:
            old_assign_dict[target] = assign
    
    new_assign_dict = {}
    for assign in new_assignments:
        target = assign.get('target')
        if target:
            new_assign_dict[target] = assign
    
    # Find new assignments
    for var_name in new_assign_dict:
        if var_name not in old_assign_dict:
            value_type = new_assign_dict[var_name].get('value_type', 'unknown')
            changes.append(f"Variable `{var_name}` assigned ({value_type})")
    
    # Find modified assignments
    for var_name in old_assign_dict:
        if var_name in new_assign_dict:
            old_type = old_assign_dict[var_name].get('value_type')
            new_type = new_assign_dict[var_name].get('value_type')
            
            if old_type != new_type:
                changes.append(f"Variable `{var_name}` assigned new value ({new_type})")
    
    return changes


def _diff_imports(old_imports: List[Dict], new_imports: List[Dict]) -> List[str]:
    """Compare import statements between old and new AST."""
    changes = []
    
    # Convert to sets for comparison
    old_import_set = set()
    for imp in old_imports:
        import_str = _import_to_string(imp)
        old_import_set.add(import_str)
    
    new_import_set = set()
    for imp in new_imports:
        import_str = _import_to_string(imp)
        new_import_set.add(import_str)
    
    # Find added imports
    added_imports = new_import_set - old_import_set
    for imp in added_imports:
        changes.append(f"Import added: {imp}")
    
    # Find removed imports
    removed_imports = old_import_set - new_import_set
    for imp in removed_imports:
        changes.append(f"Import removed: {imp}")
    
    return changes


def _import_to_string(import_dict: Dict) -> str:
    """Convert import dictionary to string representation."""
    if import_dict['type'] == 'Import':
        names = ', '.join(import_dict.get('names', []))
        return f"import {names}"
    elif import_dict['type'] == 'ImportFrom':
        module = import_dict.get('module', '')
        names = ', '.join(import_dict.get('names', []))
        return f"from {module} import {names}"
    return str(import_dict)
