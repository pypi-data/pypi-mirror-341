"""OmniScript Helpers functions
"""
# Copyright (c) LiveAction, Inc. 2022. All rights reserved.
# Copyright (c) Savvius, Inc. 2013-2019. All rights reserved.
# Copyright (c) WildPackets, Inc. 2013-2014. All rights reserved.

from json import JSONEncoder
import six


_tag_results = 'results'


def create_object_list(props: dict, cls: str) -> list:
    if isinstance(props, list):
        return [cls(p) for p in props]
    return None


def is_almost_success(props: dict) -> bool:
    # Start Capture sometimes returns: {'returns': []}
    if isinstance(props, dict) and (_tag_results in props):
        return isinstance(props[_tag_results], list)
    return False


def is_success(props: dict) -> bool:
    return (isinstance(props, dict) and (_tag_results in props)
            and isinstance(props[_tag_results], list)
            and (len(props[_tag_results]) > 0) and (props[_tag_results][0] == 0))


def load_native_props_from_dict(obj: object, props: dict, prop_dict: dict):
    """Set attributes from a dictionary."""
    if isinstance(props, dict):
        for k, v in props.items():
            a = prop_dict.get(k)
            if a is not None and hasattr(obj, a):
                # Test for bool before int. bool is an instance of int.
                if isinstance(getattr(obj, a), bool):
                    setattr(obj, a, v)
                elif isinstance(getattr(obj, a), int):
                    setattr(obj, a, int(v) if v else 0)
                elif isinstance(getattr(obj, a), six.string_types):
                    setattr(obj, a, v if v else '')


def load_native_props_from_list(obj: object, props: dict, prop_list: dict):
    """Set attributes from a dictionary."""
    if isinstance(props, dict):
        for k, v in props.items():
            if k is not None and hasattr(obj, k):
                # Test for bool before int. bool is an instance of int.
                if isinstance(getattr(obj, k), bool):
                    setattr(obj, k, v)
                elif isinstance(getattr(obj, k), int):
                    setattr(obj, k, int(v) if v else 0)
                elif isinstance(getattr(obj, k), six.string_types):
                    setattr(obj, k, v if v else '')


def load_props_from_dict(obj: object, props: dict, prop_dict: dict) -> list:
    """Set attributes from a dictionary."""
    notfound = []
    if isinstance(props, dict):
        for k, v in props.items():
            a = prop_dict.get(k)
            if a is not None and hasattr(obj, a):
                # Test for bool before int. bool is an instance of int.
                if isinstance(getattr(obj, a), bool):
                    setattr(obj, a, v)
                elif isinstance(getattr(obj, a), int):
                    setattr(obj, a, int(v) if v else 0)
                elif isinstance(getattr(obj, a), six.string_types):
                    setattr(obj, a, v if v else '')
                elif isinstance(getattr(obj, a), list):
                    setattr(obj, a, v)
                elif isinstance(getattr(obj, a), dict):
                    setattr(obj, a, v)
                else:
                    notfound.append(a)
    return notfound


def repr_array(a: list) -> str:
    """Returns a repr representation of the array."""
    return ', '.join(repr(v) for v in a) if a else ''


def str_array(a: list) -> str:
    """Returns a str representation of the array."""
    return ', '.join(str(v) for v in a) if a else ''


class OmniScriptEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
