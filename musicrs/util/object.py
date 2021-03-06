""" Object utility functions. """

import collections
import flatten_json

from copy import deepcopy
from typing import Dict, List
from sqlalchemy import inspect

from musicrs.util.types_check import is_dict, is_iterable, is_string, is_list


def as_dict(obj):
    """
    Convert sqlalchemy object to dictionary
    :param obj: SQL Alchemy object
    :return: dictionary
    """
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


def dict_to_list(dict: Dict, name_key: str = "name", value_key: str = "value"):
    """
    Returns a list of dictionaries with `name` and `value` keys for all
    key-value pair in given dictionary.
    """
    if not is_dict(dict):
        raise AttributeError(
            "Argument must be a dictionary, invalid argument received '{}'.".format(
                dict
            )
        )

    list = []

    for key, val in dict.items():
        list.append({name_key: key, value_key: val})

    return list


def list_to_dict(list: List, name_key: str = "name", value_key: str = "value"):
    """
    Returns a key-value pair dictionary with given list of dictionary having
    `name` and `value` keys or custom keys.
    """
    if not is_list(list):
        raise AttributeError(
            "Argument must be a list, invalid argument received '{}'.".format(list)
        )

    dict = {}

    for item in list:
        dict[item[name_key]] = item[value_key]

    return dict


def merge(dict1, dict2):
    """
    Merge two dictionaries recursively and
    return the merged dict. (Immutable)
    """
    result = deepcopy(dict1)

    for key, value in dict2.items():
        if is_dict(value):
            result[key] = merge(result.get(key, {}), value)
        else:
            result[key] = deepcopy(dict2[key])

    return result


def with_only(src, attrs):
    """
    Return a new copy of source dictionary
    containing only the attributes provided.
    """
    if not is_dict(src):
        raise AttributeError(
            "First argument must be a dictionary, invalid argument received '{}'.".format(
                src
            )
        )
    elif not is_list(attrs):
        raise AttributeError(
            "Second argument must be a list, invalid argument received '{}'.".format(
                attrs
            )
        )

    result = {}

    for key, value in src.items():
        if key in attrs:
            result[key] = value

    return result


def without_attr(src, attrs, deep=True):
    """
    Return a new copy of source dictionary
    removing the attributes provided.
    """
    result = {}

    for key, value in src.items():
        if deep and is_dict(value):
            value = without_attr(value, attrs, deep)
        elif deep and is_iterable(value) and not is_string(value):
            value = list(map(lambda x: without_attr(x, attrs, deep), value))

        if key not in attrs:
            result[key] = value

    return result


def map_dict(dict, callback, recursive=False):
    """
    Returns a new dictionary after applying a callback function over each item in given dictionary.
    :param dict Dictionary of items to iterate the callback functions over.
    :type dict
    :param callback Function that is called with each value passed as an argument.
    :type function
    :param recursive Boolean value that determines whether or not to apply callback function recursively.
    :type bool
    """
    new_dict = {}

    for key, value in dict.items():
        if recursive and is_dict(value):
            new_dict[key] = map_dict(value, callback, recursive=recursive)
        else:
            new_dict[key] = callback(key, value)

    return new_dict


def linearize(dict, separator="."):
    """
    Returns a flattened/linearized dictionary from provided nested dictionary.
    """
    return flatten_json.flatten(dict, separator)


def delinearize(dict, separator="."):
    """
    Returns a nested dictionary from provided flattened/linearized dictionary.
    """
    return flatten_json.unflatten_list(dict, separator)
