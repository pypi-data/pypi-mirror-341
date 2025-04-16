import json
from typing import Any


class Bunch:
    def __init__(self, *args, **kwargs):
        for arg in args:
            if not isinstance(arg, dict):
                kwargs[arg] = None
        self.__dict__.update(kwargs)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __contains__(self, key):
        return key in self.__dict__

    def __str__(self):
        return json.dumps(self.__dict__, indent=4, sort_keys=False)

    def __repr__(self):
        return self.__str__()

    def __delitem__(self, key):
        del self.__dict__[key]

    def contains_value(self, value):
        return value in self.__dict__.values()

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    @staticmethod
    def from_dict(dictionary: dict) -> Any:
        return Bunch(**dictionary)
