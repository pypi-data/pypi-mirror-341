"""
    pyxperiment/controller/instrument_module.py:
    Instrument module is a part of an instrument, which combines related
    controls. May correspond to physical module.

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

from typing import TypeVar, Generic
from .instrument import Instrument

InstrType = TypeVar('InstrType', bound=Instrument)
class InstrumentModule(Instrument, Generic[InstrType]):
    """
    Instrument module is a part of an instrument, combining the related controls,
    often representing an actual physical 'module'.
    """

    def __init__(self, name: str, instrument: InstrType) -> None:
        super().__init__(name)
        self.instrument = instrument

    @property
    def location(self) -> str:
        return self.instrument.location

    @staticmethod
    def driver_name() -> str:
        return ""

    def device_name(self) -> str:
        return self.instrument.device_name()
