"""
    pyxperiment/devices/lsci/lsci218.py:
    Support for Lake Shore Model 218 temperature monitor

    This file is part of the PyXperiment project.

    Copyright (c) 2022 PyXperiment Developers

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

from pyxperiment.instrument import (
    VisaInstrument, ValueControl
)

class LakeShore218TempMonitor(VisaInstrument):
    """Lake Shore Model 218 temperature monitor support"""

    def __init__(self, rm, resource):
        super().__init__(rm, resource)
        self.set_options(
            self.temperature +
            self.sensor_units
        )

    @staticmethod
    def driver_name():
        return 'Lake Shore Model 218 temperature monitor'

    def device_name(self):
        value = self.query_id().translate({ord(c): None for c in ['\r', '\n']}).split(',')
        return value[0] + ' ' + value[1] + ' temperature monitor'

    def query_id(self):
        return self.query('QIDN?')

    def get_temperature(self, channel):
        """
        Get sensor reading in kelvin
        """
        return self.query('KRDG? ' + channel)

    def get_sensor_units(self, channel):
        """
        Get sensor reading in sensor units
        """
        return self.query('SRDG? ' + channel)

    temperature = [
        ValueControl(
            'Temperature CH ' + ch, 'K', lambda instr, ch=ch: instr.get_temperature(ch)
            ) for ch in map(str,range(1,3))
        ]
    sensor_units = [
        ValueControl(
            'Sensor units CH ' + ch, 'Ohm', lambda instr, ch=ch: instr.get_sensor_units(ch)
            ) for ch in map(str,range(1,3))
        ]
