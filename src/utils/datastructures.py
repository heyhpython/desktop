"""
@author: yuhao.he
@contact: <hawl.yuhao.he@gmail.com>
@version: 0.0.1
@file: datastructures.py
@time: 2021/10/29 10:41
"""
import re
from typing import Union


class CaseFreeKey:
    """驼峰与下划线命名方式互转"""
    regex = re.compile(r'[a-zA-Z\d]+')

    def __init__(self, value: str):
        self.origin = value
        self._value = self.get_value(value)

    def __eq__(self, other) -> bool:
        return self._value == str(other)

    def __hash__(self):
        return hash(self._value)

    def __str__(self):
        return self._value

    @classmethod
    def get_value(cls, s) -> str:
        matched = cls.regex.findall(s)
        value = ''
        for sub in matched:
            value += sub.upper()
        return value

    def __repr__(self):
        return f'CaseFreeKey("{self.origin}")'


class CaseFreeDict:
    """
    忽略大小写的dict
    """

    def __init__(self, defaults: dict = None, **kwargs):
        self._data = {}
        self.dict = {}
        if defaults:
            defaults.update(kwargs)
        else:
            defaults = kwargs
        for k, v in defaults.items():
            self.__setitem__(k, v)

    def __setitem__(self, key: Union[str, CaseFreeKey], value):
        key = CaseFreeKey(str(key))
        self._data[key] = value

    def __getitem__(self, key: Union[str, CaseFreeKey]):
        key = CaseFreeKey(str(key))
        return self._data[key]

    def get(self, key: Union[str, CaseFreeKey], default=None):
        key = CaseFreeKey(str(key))
        try:
            v = self.__getitem__(key)
        except KeyError:
            v = default
        return v

    def __repr__(self):
        return str(self._data)
