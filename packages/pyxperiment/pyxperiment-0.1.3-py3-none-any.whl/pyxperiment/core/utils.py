"""
    pyxperiment/core/utils.py: Contains useful utilitary methods

    This file is part of the PyXperiment project.

    Copyright (c) 2023 PyXperiment Developers

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
"""

from decimal import Decimal

class Singleton(type):
    """
    metaclass to specify that only one instance of this class exists
    """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

# pylint: disable=C0103
class classandinstancemethod(classmethod):
    """
    To define a method that can be called both for class and for instance
    """
    def __get__(self, instance, type_):
        descr_get = super().__get__ if instance is None else self.__func__.__get__
        return descr_get(instance, type_)

def str_to_range(range_str: str, limit: int=100000) -> list[Decimal]:
    """
    Converts the range string to python array
    """
    ranges = range_str.split(' ')
    result = []
    for curr_range in ranges:
        parts = curr_range.split(':')
        if len(parts) == 1 and parts[0] != '':
            result.append(Decimal(parts[0]))
        elif len(parts) == 3 and parts[2] != '':
            start = Decimal(parts[0])
            step = Decimal(parts[1])
            end = Decimal(parts[2])
            numpoints = int((end - start) / step) + 1
            if numpoints > limit:
                raise Exception('Too many points for a valid sweep')
            result += [start + (i) * step for i in range(numpoints)]
    return result

# pylint: disable=C0103
class bidict(dict):
    """
    A simple bidirectional dictionary, composed of two
    ordinary dictionaries
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inverse = {}
        for key, value in self.items():
            self.inverse.setdefault(value, []).append(key)

    def __setitem__(self, key, value):
        if key in self:
            self.inverse[self[key]].remove(key)
        super().__setitem__(key, value)
        self.inverse.setdefault(value, []).append(key)

    def __delitem__(self, key):
        self.inverse.setdefault(self[key], []).remove(key)
        if self[key] in self.inverse and not self.inverse[self[key]]:
            del self.inverse[self[key]]
        super().__delitem__(key)
