import pytest
from jsoninja.core import traverse_json, get_value_at_path, find_all_paths_for_element

def test_traverse_json():
    data = {"a": {"b": [1, 2], "c": 3}}
    expected = [
        ("a.b[0]", 1),
        ("a.b[1]", 2),
        ("a.c", 3)
    ]
    assert list(traverse_json(data)) == expected

def test_get_value_at_path():
    data = {"a": {"b": [1, 2], "c": 3}}
    assert get_value_at_path(data, "a.b[1]") == 2
    assert get_value_at_path(data, "a.c") == 3

def test_find_all_paths_for_element():
    data = {"a": {"b": [1, 2], "c": 3}, "d": {"b": 2}}
    assert find_all_paths_for_element(data, 2) == ["a.b[1]", "d.b"]