import re
def traverse_json(data, parent_key='', separator='.'):
    """
    Recursively traverse a nested JSON structure and yield paths and values.
    :param data: The JSON data (dict or list).
    :param parent_key: The accumulated key path.
    :param separator: The separator to join keys.
    :yield: (path, value) tuples.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            new_key = f"{parent_key}{separator}{key}" if parent_key else key
            yield from traverse_json(value, new_key, separator)
    elif isinstance(data, list):
        for index, value in enumerate(data):
            new_key = f"{parent_key}[{index}]"
            yield from traverse_json(value, new_key, separator)
    else:
        yield parent_key, data


def get_value_at_path(data, path, separator='.'):
    """
    Get the value at a given path in the JSON structure.
    :param data: The JSON data (dict or list).
    :param path: The path to the desired element.
    :param separator: The separator used in the path.
    :return: The value at the given path.
    """
    # Regular expression to match keys (e.g., "a") and indices (e.g., "[1]")
    pattern = re.compile(rf'[^{re.escape(separator)}\[\]]+|\[\d+\]')
    
    # Split the path into components
    components = pattern.findall(path)
    current = data
    
    for component in components:
        if component.startswith('[') and component.endswith(']'):
            # Extract the index from the brackets
            index = int(component[1:-1])
            if isinstance(current, list):
                current = current[index]
            else:
                raise KeyError(f"Index {index} accessed on non-list: {current}")
        else:
            # Access the key in the dictionary
            if isinstance(current, dict):
                current = current[component]
            else:
                raise KeyError(f"Key {component} accessed on non-dictionary: {current}")
    
    return current

def find_all_paths_for_element(data, target, separator='.'):
    """
    Find all paths where the target element exists.
    :param data: The JSON data (dict or list).
    :param target: The target element to search for.
    :param separator: The separator used in paths.
    :return: List of paths where the target element is found.
    """
    paths = []
    for path, value in traverse_json(data, separator=separator):
        if value == target:
            paths.append(path)
    return paths
