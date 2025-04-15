"""
    pyxperiment/devices/lsci/lsci370.py:
    Support for Lake Shore Model 370 resistance bridge

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

import time
from decimal import Decimal
from pyxperiment.instrument import (
    VisaInstrument, ListControl, ValueControl, StaticRangeValidator, RampControl,
    MultiControl, InstrumentModule, BooleanControl
)

class LakeShore370ResBridge(VisaInstrument):
    """
    Lake Shore Model 370 resistance bridge support
    """

    def __init__(self, rm, resource):
        super().__init__(rm, resource)
        self.write('*CLS')
        self.sample_heater = self.SampleHeater(self)
        self.analog_heater1 = self.AnalogHeater(self, 1)
        self.analog_heater2 = self.AnalogHeater(self, 2)

    @staticmethod
    def driver_name():
        return 'Lake Shore Model 370 resistance bridge'

    def device_name(self):
        value = self.query_id().translate({ord(c): None for c in ['\r', '\n']}).split(',')
        return value[0] + ' ' + value[1] + ' resistance bridge'

    class SampleHeater(InstrumentModule[VisaInstrument]):
        """
        Represents controls over sample heating
        """
        def __init__(self, instrument: VisaInstrument):
            super().__init__('Sample Heater', instrument)
            self.current_value = None
            self.sample_control_mode = ListControl(
                'Heater mode', ListControl.dict_for_list(self._CONTROL_MODE_VALUES, 1),
                lambda instr=self.instrument: instr.query('CMODE?'),
                lambda value, instr=self.instrument: instr.write('CMODE '+ value),
            )
            self.mode = MultiControl((
                ListControl('Heater input', self._HEATER_INPUT_VALUES),
                BooleanControl('Filter'),
                ValueControl('Delay', 's'),
                ListControl('Heater limit', ListControl.dict_for_list(self._HEATER_RANGE_VALUES)),
                ), self._get_control_setup, self._set_control_setup
                )
            self.pid_params = MultiControl((
                ValueControl('P', None),
                ValueControl('I', None),
                ValueControl('D', None),
                ), self._get_pid_values, self._set_pid_values
                )
            self.ramp_params = MultiControl((
                BooleanControl('Ramp on'),
                ValueControl('Ramp rate', 'K/min'),
                ), self._get_ramp, self._set_ramp
                )
            self.target_temp = ValueControl(
                'Set Temperature', 'K',
                lambda instr=self.instrument: instr.query('SETP?').translate({ord(c): None for c in ['\r', '\n']}),
                lambda value, instr=self.instrument: instr.write(f'SETP {value}'),
                validator=StaticRangeValidator('0', '0.8'),
                sweepable=False
            )
            self.ramp_temperature = RampControl(
                'Ramp Temperature', 'K',
                get_actual_value=lambda instr=self.instrument: instr.temperature[1].get_value(),
                set_target_value=self._set_value,
                get_target_value=lambda instr=self.instrument: instr.target_temp.get_value(),
                stop_ramp=lambda _: None,
                is_finished=self._is_finished,
                validator=self.target_temp.validator
            )

        _CONTROL_MODE_VALUES = [
            'Closed Loop (PID)', 'Zone', 'Open Loop', 'Off',
            ]

        _HEATER_INPUT_VALUES = [
            '1', '2', '3', '4', '5', '6', '7',
            '8', '9', '10', '11', '12', '13', '14', '15', '16'
            ]

        _HEATER_RANGE_VALUES = [
            'off', '31.6 µA', '100 µA', '316 µA',
            '1.00 mA', '3.16 mA', '10.0 mA', '31.6 mA', '100 mA'
            ]

        _sample_heater_range = ListControl(
            'Sample heater range', ListControl.dict_for_list(_HEATER_RANGE_VALUES),
            get_func=lambda instr: instr.query('HTRRNG?'),
            set_func=lambda instr, value: instr.write('HTRRNG '+ value),
        )

        def _get_pid_values(self):
            return map(lambda x: str(Decimal(x)), self.instrument.query('PID?').split(','))

        def _set_pid_values(self, p_value, i_value, d_value):
            self.instrument.write(f'PID {p_value},{i_value},{d_value}')

        def _get_control_setup(self):
            values = self.instrument.query('CSET?').split(',')
            return [values[0],values[1],values[3],values[5]]

        def _set_control_setup(self, input_num, filter_on, delay, limit):
            values = self.instrument.query('CSET?').split(',')
            values[0] = input_num
            values[1] = filter_on
            values[3] = delay
            values[5] = limit
            self.instrument.write('CSET ' + ','.join(values))

        def _get_ramp(self):
            return self.instrument.query('RAMP?').split(',')

        def _set_ramp(self, ramp_on, ramp_rate):
            self.instrument.write('RAMP ' + ramp_on + ',' + ramp_rate)

        def _set_value(self, value):
            self.target_temp.set_value(value)
            self.current_value = value

        def _is_finished(self):
            if self.current_value is not None:
                return abs(
                    (Decimal(self.current_value) - Decimal(self.instrument.query('RDGK? '+str(6)))
                    ) / Decimal(self.current_value)) < Decimal('0.02')
            return True

    class AnalogHeater(InstrumentModule[VisaInstrument]):
        """
        Represents control over analog heater
        """
        def __init__(self, instrument: VisaInstrument, channel: int):
            super().__init__(f'Analog heater {channel}', instrument)
            self.channel = channel
            modes_list = self._HEATER_MODES if self.channel == 2 else self._HEATER_MODES[:-1]
            self.mode = MultiControl((
                BooleanControl('Polarity'),
                ListControl('Heater mode', ListControl.dict_for_list(modes_list)),
                ),
                self._get_analog_mode, self._set_analog_mode,
                )
            if channel == 2:
                self.still_power = MultiControl((
                    ValueControl('Still power', 'mW'),
                    ValueControl('Still voltage', 'V', enabled=lambda _: False),
                    ),
                    self._get_still_power, self._set_still_power
                    )

        _HEATER_MODES = [
            'Off', 'Channel', 'Manual', 'Zone', 'Still'
            ]

        def _get_still_volt(self):
            return str(Decimal(self.instrument.query('STILL?'))/Decimal('10'))

        def _set_still_volt(self, value):
            self.instrument.write('STILL '+str(Decimal(value)*Decimal('10')))

        def _get_analog_mode(self):
            values = self.instrument.query(f'ANALOG? {self.channel}').split(',')
            return values[:2]

        def _set_analog_mode(self, bipolar, mode):
            values = self.instrument.query(f'ANALOG? {self.channel}').split(',')
            values[0] = bipolar
            values[1] = mode
            self.instrument.write(f'ANALOG {self.channel},' + ','.join(values))

        def _get_still_power(self):
            value = self._get_still_volt()
            return [str(pow(Decimal(value)/150, 2)*120*1000), value]

        def _set_still_power(self, power):
            voltage = pow(Decimal(power[0])/1000/120, Decimal('0.5'))*150
            self._set_still_volt(voltage)
            time.sleep(0.05)

    temperature = [
        ValueControl(
            'Temperature CH ' + str(i), 'K',
            get_func=lambda instr, ch=i: instr.query(f'RDGK? {ch}').translate({ord(c): None for c in ['\r', '\n']})
            )
        for i in [2, 6]]

    resistance = [
        ValueControl(
            'Resistance CH ' + str(i), 'Ohm',
            get_func=lambda instr, ch=i: instr.query(f'RDGR? {ch}').translate({ord(c): None for c in ['\r', '\n']})
            )
        for i in [2, 6]]
