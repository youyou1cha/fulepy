#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __getattr__

from collections import abc

class FrozenJson:
    '''
    只读接口，使用属性表示法访问JSON类对象
    '''

    def __new__(cls, *args, **kwargs):
        if isinstance(args,abc.Mapping):
            return super().__new__(cls)
        elif isinstance(args,abc.MutableSequence):
            return [cls(item) for item in args]
        else:
            return args

    def __init__(self,mapping):
        self.__data = dict(mapping)
        for key, value in mapping.items():
            if iskeyword(key):
                key += '_'
            self.__data[key] = value

    def __getattr__(self, name):
        if hasattr(self.__data,name):
            return getattr(self.__data,name)
        else:
            return FrozenJson.build(self.__data[name])

    @classmethod
    def build(cls,obj):
        if isinstance(obj,abc.Mapping):
            return cls(obj)
        elif isinstance(obj,abc.MutableSequence):
            return [cls.build(item) for item in obj]
        else:
            return obj