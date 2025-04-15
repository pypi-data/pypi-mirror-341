"""
    pyxperiment/devices/testdevice.py: Dummy device for test purposes

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

import random
import time
from decimal import Decimal

from pyxperiment.core.utils import str_to_range
from pyxperiment.instrument import (
    Instrument, ValueControl, ActionControl, SweepControl, StaticRangeValidator
)

class TestDevice(Instrument):
    """
    Test device is used to simulate the data to test graphs and functions of pyxperiment.
    """

    def __init__(self, rm, resource):
        super().__init__('')
        del rm
        self.last_value = 0
        self.up_value = Decimal('0')
        self._rand_channels = 1
        self.set_options([
            self.channels, self.do_reset
        ])
        self.resource = resource if resource else 'Test address'

    def _reset(self):
        self.last_value = 0
        self.up_value = Decimal('0')

    def get_channels_num(self):
        return str(self._rand_channels)

    def set_channels_num(self, value):
        self._rand_channels = int(value)

    @staticmethod
    def driver_name():
        return 'Test'

    def device_name(self):
        return 'Test device'

    @property
    def location(self):
        return self.resource

    def get_value(self):
        return str(self.last_value)

    def get_value2(self):
        value = str(self.up_value)
        self.up_value += Decimal('0.1')
        #time.sleep(0.01)
        return str(value)

    def set_value(self, value):
        self.last_value = value

    def get_random(self):
        #time.sleep(0.1)
        if self._rand_channels == 1:
            return f"{(random.triangular(-10, 10)):.3f}"
        return [f"{(random.triangular(-10, 10)):.3f}" for i in range(self._rand_channels)]

    channels = ValueControl(
        'Random channels', None,
        get_func=get_channels_num,
        set_func=set_channels_num,
        validator=StaticRangeValidator(1, 8, 1),
        sweepable=False
        )

    value = ValueControl(
        'Sweepable', 'V', get_value, set_value,
        validator=StaticRangeValidator('-10', '10', '0.01')
        )
    value2 = ValueControl(
        'Measurable Up', 'V', get_value2
        )
    rand = ValueControl(
        'Measurable Random', 'V', get_random, None, lambda self: int(self.get_channels_num())
        )

    sweep = SweepControl(
        'Test sweep', ('Frequency', 'Power'), ('Hz','dB'),
        get_func=lambda instr:
            (
                list(map(str, str_to_range('1000:2:2000'))),
                [f"{(random.triangular(-10, 10)):.3f}" for i in range(501)]
                )
    )

    do_reset = ActionControl(
        'Reset', _reset
    )

    test_list_values = {
        '6 dB/oct':'1',
        '12 dB/oct':'2',
        '18 dB/oct':'3',
        '24 dB/oct':'4',
        '30 dB/oct':'5',
        '36 dB/oct':'6',
        '42 dB/oct':'7',
        '48 dB/oct':'8'
    }
