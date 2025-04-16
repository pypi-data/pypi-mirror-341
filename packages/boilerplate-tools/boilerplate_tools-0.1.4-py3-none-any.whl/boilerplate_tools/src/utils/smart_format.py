"""Utility functions for string formatting and template variable management."""
from typing import Dict, Any, List
import re
import logging

# Configure logging
logger = logging.getLogger(__name__)


def smart_format(template: str, variables: Dict[str, Any]) -> str:
    """
    A strict string substitution utility that requires all template variables to be provided.
    
    This function performs substitution of variables in a template string,
    requiring all variables to be present in the provided dictionary.
    It also logs a warning about any unused variables.
    
    Args:
        template: The template string with placeholders like {variable}
        variables: Dictionary of variables to substitute into the template
        
    Returns:
        str: The formatted string with variables substituted
        
    Raises:
        KeyError: If any template variable is missing from the variables dictionary
        
    Examples:
        >>> smart_format("Hello, {name}!", {"name": "World"})
        'Hello, World!'
        >>> smart_format("Hello, {name}!", {"name": "World", "unused": "value"})  # Logs warning about unused variable
        'Hello, World!'
        >>> smart_format("Hello, {name}!", {})  # Raises KeyError
        Traceback (most recent call last):
            ...
        KeyError: "Missing required template variable: 'name'"
    """
    # Extract all variable names from the template
    required_variables = extract_variables(template)
    
    # Check if all required variables are present
    for var in required_variables:
        if var not in variables:
            raise KeyError(f"Missing required template variable: '{var}'")
    
    # Check for unused variables and log warnings
    used_variables = set(required_variables)
    all_variables = set(variables.keys())
    unused_variables = all_variables - used_variables
    
    if unused_variables:
        logger.warning(
            f"Unused variables provided that are not in the template: {', '.join(unused_variables)}"
        )
    
    # Use standard string formatting
    return template.format(**variables)


def extract_variables(template: str) -> List[str]:
    """
    Extract variable names from a template string.
    
    Args:
        template: The template string with placeholders like {variable}
        
    Returns:
        List[str]: List of variable names found in the template
        
    Note:
        Ignores escaped variables like {{not_a_variable}}
    """
    # Replace double braces temporarily (to avoid matching them)
    temp_template = template.replace('{{', '<<<').replace('}}', '>>>')
    
    # Find all patterns like {variable_name}
    pattern = r'\{([^{}]+)\}'
    variables = re.findall(pattern, temp_template)
    
    return variables