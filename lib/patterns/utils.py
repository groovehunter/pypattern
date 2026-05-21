"""
This module provides helper functions for handling patterns,
compatible with both CPython and MicroPython.
"""

def get_pattern_class_by_name(name, global_scope):
    """
    Finds a pattern class by its name in the provided global scope.
    This avoids platform-specific modules like 'inspect'.

    :param name: The name of the class (str).
    :param global_scope: The dictionary from globals().
    :return: The class object.
    :raises KeyError: If the class name is not found.
    """
    if name in global_scope:
        return global_scope[name]
    raise KeyError(f"Pattern class '{name}' not found. Make sure it's imported.")

