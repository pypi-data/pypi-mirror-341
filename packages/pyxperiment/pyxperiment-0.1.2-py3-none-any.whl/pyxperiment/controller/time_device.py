"""
    pyxperiment/controller/time_device.py:
    Module defines special instrument class, used for time sweeps

    This file is part of the PyXperiment project.

    Copyright (c) 2019 PyXperiment Developers

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

from pyxperiment.instrument import Instrument, ValueControl

class TimeDevice(Instrument):
    """
    Special instrument class, used for time sweeps
    """

    def __init__(self, rm=None, resource=None):
        super().__init__('')
        self.value = '0'

    @staticmethod
    def driver_name():
        return 'Time'

    def device_name(self):
        return 'Time'

    @property
    def location(self):
        return ''

    def description(self):
        ret = []
        ret.insert(0, ('Name', 'Time sweep'))
        return ret

    def _set_value(self, value):
        self.value = value

    def _get_value(self):
        return self.value

    time = ValueControl('Time', 's', _get_value, _set_value)
