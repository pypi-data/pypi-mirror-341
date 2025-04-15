"""
    pyxperiment_controller/validation.py:
    Validators check the conformity to given constraints

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

from abc import ABCMeta, abstractmethod
from decimal import Decimal
from typing import Union, Optional, Sequence, Callable, Any, Tuple

class Validator(metaclass=ABCMeta):
    """
    Used to check the compliance of an element to certain criteria
    """

    @abstractmethod
    def check_value(self, value: Union[str,int,float]) -> bool:
        """
        Validate a single element
        """

    def check_values(self, values: Sequence[Union[str,int,float]]) -> list[bool]:
        """
        Validate the compliance of all values to constraints
        """
        return [self.check_value(x) for x in values]

class EmptyValidator(Validator):
    """
    Positively validates any elements
    """

    @staticmethod
    def check_value(value: Union[str,int,float]):
        del value
        return True

    @staticmethod
    def check_values(values: Sequence[Union[str,int,float]]):
        return [True for x in values]

class StaticRangeValidator(Validator):
    """
    Validates the presence of a decimal value within given decimal range.
    """

    def __init__(self, lower, upper, quant=None):
        self._lower = Decimal(lower)
        self._upper = Decimal(upper)
        self._quant = Decimal(quant) if quant is not None else None

    def check_value(self, value: Union[str,int,float]):
        dec_val = Decimal(value)
        return (
            (self._lower <= dec_val <= self._upper) and
            (self._quant is None or divmod(dec_val, self._quant)[1] == 0)
        )

class DynamicRangeValidator(Validator):
    """
    Validates the presence of a decimal value within given decimal range. The range itself is
    dependent on the instrument status.
    """

    def __init__(self, range_func: Callable[[Any],Tuple[Decimal,Decimal,Optional[Decimal]]]):
        self._range_func = range_func
        self._instr = None# type: Any

    def set_instrument(self, instr):
        self._instr = instr

    def check_value(self, value: Union[str,int,float]):
        lower, upper, quant = self._range_func(self._instr)
        dec_val = Decimal(value)
        return (
            (lower <= dec_val <= upper) and (quant is None or divmod(dec_val, quant)[1] == 0)
        )

    def check_values(self, values: Sequence[Union[str,int,float]]) -> list[bool]:
        lower, upper, quant = self._range_func(self._instr)
        if quant is None:
            return [
                (lower <= dec_val <= upper) for dec_val in map(Decimal, values)
            ]
        return [
            ((lower <= dec_val <= upper) and divmod(dec_val, quant)[1] == 0)
            for dec_val in map(Decimal, values)
        ]
        