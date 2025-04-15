
# JSONavigator

JSONavigator is a Python package designed to simplify working with nested JSON structures. It provides utilities for traversing, flattening, validating, and formatting JSON paths, making it easier to handle complex data structures.


## **Features**
- **Traverse Nested JSON**: Recursively traverse dictionaries and lists to extract paths and values.
- **Flatten JSON**: Convert nested JSON into a single-level dictionary for easier access.
- **Validate Paths**: Ensure that JSON paths are properly formatted and valid.
- **Format Paths**: Improve readability of JSON paths by replacing separators with more user-friendly formats.
- **Custom Exceptions**: Handle errors gracefully with custom exception classes.
## Installation

You can install `JSONavigator` using `pip`:

```bash
  pip install JSONavigator
```
Alternatively, if you’re installing from source:

```bash
git clone https://github.com/Nikhil-Singh-2503/JSONavigator.git
cd JSONavigator
```
Create Virtual envirnoment:
```bash
python -m venv venv
source venv/bin/activate
```
Install the requirements:
```bash
pip install -r requirements.txt
```
## Usage/Examples
Here’s how you can use the various features of JSONavigator:

**1. Traverse Nested JSON**

Use the `traverse_json` function to recursively traverse a nested JSON structure and extract paths and values. 

```python
from jsoninja.core import traverse_json

data = {"a": {"b": [1, 2], "c": 3}}

for path, value in traverse_json(data):
    print(f"Path: {path}, Value: {value}")
```

**Output**
```
Path: a.b[0], Value: 1
Path: a.b[1], Value: 2
Path: a.c, Value: 3 
```

**2. Get Value at a Specific Path**

Use the `get_value_at_path` function to retrieve the value at a specific path in the JSON structure.

```python
from jsoninja.core import get_value_at_path

data = {"a": {"b": [1, 2], "c": 3}}
value = get_value_at_path(data, "a.b[1]")
print(value)  # Output: 2
```

**Output**   
`2`

**3. Flatten JSON**

Use the `flatten_json` function to convert a nested JSON structure into a single-level dictionary.

```python
from jsoninja.utils import flatten_json

data = {"a": {"b": [1, 2], "c": 3}}
flattened = flatten_json(data)
print(flattened)
```

**Output**   
```
{
    "a.b[0]": 1,
    "a.b[1]": 2,
    "a.c": 3
}
```
**4. Validate JSON Paths**

Use the `validate_path` function to ensure that a JSON path is properly formatted.

```python
from jsoninja.utils import validate_path
from jsoninja.exceptions import InvalidPathError

try:
    validate_path("a.b[1]")
except InvalidPathError as e:
    print(f"Invalid path: {e}")
```
**Output**   
```
True
```
**5. Format JSON Paths**

Use the `format_path` function to make JSON paths more readable.

```python
from jsoninja.utils import format_path

formatted_path = format_path("a.b[1]")
print(formatted_path)
```
**Output**   
```
a -> b[1]
```

## **NOTE**

You can add your own seperator to each of the functions by passing value to a named variable `seperator`

**Example**

Suppose if you want to use seperator with `traverse_json` function. 

```python
from jsoninja.core import traverse_json

data = {"a": {"b": [1, 2], "c": 3}}

for path, value in traverse_json(data, seperator=*):
    print(f"Path: {path}, Value: {value}")
```

**Output**
```
Path: a*b[0], Value: 1
Path: a*b[1], Value: 2
Path: a*c, Value: 3 
```
## Contributing

Contributions to JSONavigator are welcome! To contribute: 

- Fork the repository on GitHub.
- Clone your fork locally:
```bash
git clone https://github.com/Nikhil-Singh-2503/JSONavigator.git
```
- Create a new branch for your feature or bugfix:
```bash
git checkout -b feature-name
```
- Make your changes and write tests if applicable.

- Run the tests to ensure everything works:
```bash
pytest
```
- Commit your changes and push them to your fork:
```bash
git commit -m "Add feature or fix"
git push origin feature-name
```
- Open a pull request on the main repository.

## Running Tests

To run the test suite, use `pytest`:

```bash
  pytest
```
For coverage reports, install `pytest-cov` and run:
```bash
  pytest --cov=JSONavigator
```
## License
This project is licensed under the MIT License.



## Contact

If you have any questions or need support, feel free to reach out:

- Email: nikhilraj7654@gmail.com 

## Acknowledgements

- Inspired by the need to simplify working with nested JSON structures.
- Built with ❤️ using Python.
     
