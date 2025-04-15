"""
    pyxperiment/devices/lsci/lsci332.py:
    Support for Lake Shore Model 332 resistance bridge

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

from pyxperiment.instrument import (
    VisaInstrument, ListControl, ValueControl, BooleanControl, InstrumentModule,
    MultiControl, StaticRangeValidator
)

class LakeShore332ResBridge(VisaInstrument):
    """
    Lake Shore Model 332 resistance bridge support
    Provides the most simple functionality to read the temperature and
    manually set the heater range/value.
    """

    def __init__(self, rm, resource):
        super().__init__(rm, resource)
        self.write('*CLS')
        self.control_loops = [LakeShore332ResBridge.ControlLoop(self, ch) for ch in (1,2)]

    @staticmethod
    def driver_name():
        return 'Lake Shore Model 332 resistance bridge support'

    def device_name(self):
        value = self.query_id().translate({ord(c): None for c in ['\r', '\n']}).split(',')
        return value[0] + ' ' + value[1] + ' resistance bridge'

    class ControlLoop(InstrumentModule[VisaInstrument]):
        """
        Represents control over sample heating
        """
        def __init__(self, instrument: VisaInstrument, channel: int):
            super().__init__('Sample Heater', instrument)
            assert channel in (1,2)
            self.channel = channel
            self.control_settings = MultiControl((
                ListControl('Input', ['A', 'B']),
                ListControl('Units', ListControl.dict_for_list(self._UNITS, 1)),
                BooleanControl('Powerup enable'),
                ListControl('Current/Power', ListControl.dict_for_list(self._C, 1)),
                )
            )
            self.control_mode = ListControl(
                'Control mode', ListControl.dict_for_list(self._CONTROL_MODES,1),
                self._get_cmode, self._set_cmode
            )
            self.pid_params = MultiControl((
                ValueControl('P', None, validator=StaticRangeValidator('0.1', '1000')),
                ValueControl('I', None, validator=StaticRangeValidator('0.1', '1000')),
                ValueControl('D', None, validator=StaticRangeValidator('0', '200')),
                ), self._get_pid_values, self._set_pid_values
                )
            self.m_out = ValueControl(
                'Manual output', '%', self._get_manual, self._set_manual,
                validator=StaticRangeValidator('0', '100')
            )
            self.setpoint = ValueControl(
                'Setpoint', 'K', self._get_setpoint, self._set_setpoint
            )
            self.output = ValueControl(
                'Output', '%', self._get_output
            )

        _UNITS = ['Kelvin', 'Celsius', 'Sensor units']

        def _get_setpoint(self):
            return self.instrument.query(f'SETP? {self.channel}')

        def _set_setpoint(self, value):
            self.instrument.write(f'SETP {self.channel},{value}')

        def _get_manual(self):
            return self.instrument.query(f'MOUT? {self.channel}')

        def _set_manual(self, value):
            self.instrument.write(f'MOUT {self.channel},{value}')

        def _get_pid_values(self):
            return self.instrument.query(f'PID? {self.channel}').split(',')

        def _set_pid_values(self, p_value, i_value, d_value):
            self.instrument.write(f'PID {self.channel},{p_value},{i_value},{d_value}')

        _CONTROL_MODES = [
            'Manual PID', 'Zone', 'Open Loop', 'AutoTune PID', 'AutoTune PI', 'AutoTune P',
        ]

        def _get_cmode(self):
            return self.instrument.query(f'CMODE? {self.channel}')

        def _set_cmode(self, value):
            self.instrument.write(f'CMODE {self.channel},{value}')

        def _get_output(self):
            return self.instrument.query('HTR?' if self.channel == 1 else 'AOUT?')

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

    _HEATER_RANGES = [
        'Off', 'Low (0.5 W)', 'Medium (5 W)', 'High (50 W)'
    ]
    heater_range = ListControl(
        'Heater range',
        values_list=ListControl.dict_for_list(_HEATER_RANGES),
        get_func=lambda instr: instr.query('RANGE?'),
        set_func=lambda instr, val: instr.write(f'RANGE {val}'),
    )

    temperature_a = ValueControl(
        'Temperature CH A', 'K', lambda instr: instr.get_temperature('A')
        )
    temperature_b = ValueControl(
        'Temperature CH B', 'K', lambda instr: instr.get_temperature('B')
        )
    sensor_units_a = ValueControl(
        'Sensor units CH A', 'Ohm', lambda instr: instr.get_sensor_units('A')
        )
    sensor_units_b = ValueControl(
        'Sensor units CH B', 'Ohm', lambda instr: instr.get_sensor_units('B')
        )
