# Import core functions from the core module
from jsoninja.core import (
    traverse_json,
    get_value_at_path,
    find_all_paths_for_element
)

# Import custom exceptions from the exceptions module
from jsoninja.exceptions import (
    InvalidPathError,
    ElementNotFoundError
)

# Define what is exposed when someone uses `from nested_json_utils import *`
__all__ = [
    "traverse_json",
    "get_value_at_path",
    "find_all_paths_for_element",
    "InvalidPathError",
    "ElementNotFoundError"
]

# Optionally, define package metadata
__version__ = "0.1.0"
__author__ = "Nikhil Singh"
__email__ = "nikhilraj7654@gmail.com"