# Boilerplate Tools

A collection of utility functions and tools to simplify common development tasks.

## Installation

```bash
pip install boilerplate-tools
```

## Features

- **Smart String Formatting**: String templating with variable validation
- **Configuration Management**: Load and process configuration files
- **JSON I/O**: Simple functions for reading, writing, and appending JSON data
- **Path Management**: Easily handle Python path configuration

## Usage Examples

### Smart Format

```python
from boilerplate_tools import smart_format

# Format a string with required variables
result = smart_format("Hello, {name}!", {"name": "World"})
print(result)  # Output: Hello, World!

# Will raise KeyError for missing variables
try:
    smart_format("Hello, {name}!", {})
except KeyError as e:
    print(e)  # Missing required template variable: 'name'

# Will warn about unused variables
import warnings
with warnings.catch_warnings(record=True) as w:
    smart_format("Hello, {name}!", {"name": "World", "unused": "value"})
    if w:
        print(w[0].message)  # Unused variables provided that are not in the template: unused
```

### Configuration Loading

```python
from boilerplate_tools import load_config

# Load a configuration file with variable resolution
config = load_config("config.yaml")
print(config.some_key)
```

### JSON I/O

```python
from boilerplate_tools import read_json, write_json, append_json

# Read a JSON file
data = read_json("data.json")

# Write a JSON file
write_json("output.json", {"name": "John", "age": 30})

# Append to a JSON list file
append_json("list.json", [{"name": "John"}, {"name": "Jane"}])
```

### Path Management

```python
from boilerplate_tools import setup_root

# Add the current directory to sys.path
setup_root()

# Add the parent directory to sys.path
setup_root(n_up=1)

# Get the root directory path
root_dir = setup_root(n_up=1, return_root=True)
print(f"Root directory: {root_dir}")
```

## Development

Distribution creation:

```bash
python setup.py sdist bdist_wheel
``` 

Upload to PyPI:

```bash
twine upload dist/*
```

## TODO
- Add Pytest tests for all functions
