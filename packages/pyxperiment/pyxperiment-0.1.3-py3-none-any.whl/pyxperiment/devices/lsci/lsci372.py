"""
    devices/lsci/lsci372.py: Support for Lake Shore Model 372 resistance bridge

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
import time

from pyxperiment.instrument import (
    VisaInstrument, InstrumentModule, RampControl, ListControl, ValueControl, MultiControl,
    StaticRangeValidator, BooleanControl
)

class LakeShore372ResBridge(VisaInstrument):
    """
    Lake Shore Model 372 resistance bridge support
    """

    def __init__(self, rm, resource):
        super().__init__(rm, resource)
        self.write('*CLS')
        self.sample_heater = self.Heater(self, 0)
        self.analog_heater1 = self.Heater(self, 1)
        self.analog_heater2 = self.Heater(self, 2)
        self.target_temp = ValueControl(
            'Set Temperature', 'K',
            self.get_target_temp, self.set_target_temp,
            sweepable=False
        )
        self.current_temp = ValueControl(
            'Actual temperature', 'K', self._get_value
        )

    @staticmethod
    def driver_name():
        return 'Lake Shore Model 372 resistance bridge'

    def device_name(self):
        value = self.query_id().translate({ord(c): None for c in ['\r', '\n']}).split(',')
        return value[0] + ' ' + value[1] + ' resistance bridge'

    class Heater(InstrumentModule[VisaInstrument]):
        """
        Represents control over heaters
        """

        HEATER_MODE_VALUES = [
            'Off', 'Monitor Out', 'Open Loop (Manual)', 'Zone',
            'Still', 'Closed Loop (PID)', 'Warm up'
            ]

        SHEATER_RANGES = [
            'off', '31.6 µA', '100 µA', '316 µA',
            '1.00 mA', '3.16 mA', '10.0 mA', '31.6 mA', '100 mA'
            ]
        AHEATER_RANGES = [
            'off', 'on'
        ]

        HEATER_INPUT_VALUES = [
            '0', 'A', '1', '2', '3', '4', '5', '6', '7',
            '8', '9', '10', '11', '12', '13', '14', '15', '16'
        ]

        CHANNEL_MODES = (
            [0, 2, 3, 5], [0, 2, 3, 5, 6], [0, 1, 2, 4]
        )

        def __init__(self, instrument: VisaInstrument, channel: int):
            super().__init__(
                'Sample Heater' if channel == 0 else 'Analog heater ' + str(channel), instrument
                )
            self.channel = channel
            self.current_value = None
            modes_list = self.CHANNEL_MODES[self.channel]
            self.mode = MultiControl((
                ListControl(
                    'Heater mode',
                    dict(zip([self.HEATER_MODE_VALUES[i] for i in modes_list],map(str,modes_list)))
                    ),
                ListControl('Heater input', self.HEATER_INPUT_VALUES),
                BooleanControl('Powerup enable'),
                BooleanControl('Polarity'),
                BooleanControl('Filter'),
                ValueControl('Delay', 's')
                ),
                self._get_heater_mode, self._set_heater_mode,
                )
            ranges = self.SHEATER_RANGES if self.channel == 0 else self.AHEATER_RANGES
            self.range = ListControl(
                'Range', ListControl.dict_for_list(ranges),
                self._get_range, self._set_range
                )
            if self.channel in (1,2):
                self.pid_params = MultiControl((
                    ValueControl('P', None),
                    ValueControl('I', None),
                    ValueControl('D', None),
                    ), self._get_pid_values, self._set_pid_values,
                )
            if self.channel == 2:
                self.still_power = MultiControl((
                    ValueControl('Still power', 'mW'),
                    ValueControl('Still voltage', 'V', enabled=lambda _: False),
                    ),
                    self._get_still_power, self._set_still_power,
                    )

        def _get_still_power(self):
            value = self._get_analog_volt()
            return [str(pow(Decimal(value)/150, 2)*120*1000), value]

        def _set_still_power(self, power):
            voltage = pow(Decimal(power[0])/1000/120, Decimal('0.5'))*150
            self._set_still_voltage(voltage)
            time.sleep(0.05)
            self._set_analog_volt(voltage)
            time.sleep(0.05)

        def _get_heater_mode(self):
            return self.instrument.query('OUTMODE?' + str(self.channel)).split(',')

        def _set_heater_mode(self, mode, input_num, pup_enable, polarity, filter_on, delay):
            self.instrument.write(
                'OUTMODE ' + str(self.channel) + ',' + mode + ',' + input_num + ',' +
                pup_enable + ',' + polarity + ',' + filter_on + ',' + str(delay)
                )

        def _set_still_voltage(self, value):
            self.instrument.write('STILL' + str(Decimal(value)*Decimal('10')))# percent of 10.0V

        def _get_analog_volt(self):
            value = self.instrument.query('ANALOG? ' + str(self.channel))
            return str(Decimal(value.split(',')[6])/Decimal('10'))# percent of 10.0V

        def _set_analog_volt(self, value):
            self.instrument.write('ANALOG 2,0,4,0,2,+1.0E+00,+0.0E-03,' + str(Decimal(value)*Decimal('10')))# percent of 10.0V

        def _get_pid_values(self):
            return map(
                lambda x: str(Decimal(x)), self.instrument.query('PID?'+str(self.channel)).split(',')
                )

        def _set_pid_values(self, p_value, i_value, d_value):
            self.instrument.write(
                'PID '+str(self.channel)+','+str(p_value)+','+str(i_value)+','+str(d_value)
                )

        def _get_range(self):
            return self.instrument.query('RANGE?' + str(self.channel))

        def _set_range(self, value):
            self.instrument.write('RANGE ' + str(self.channel) + ',' + value)

    def get_target_temp(self):
        return self.query('SETP?')

    def set_target_temp(self, value):
        self.write('SETP'+str(value))

    def _get_value(self):
        return self.query('KRDG?6')

    def _set_value(self, value):
        if Decimal(value) < Decimal(self._get_value()):
            self.analog_heater2.range.set_value(True)
        else:
            self.analog_heater2.range.set_value(False)
        time.sleep(0.05)
        self.set_target_temp(value)
        self.sample_heater.current_value = value

    def _is_finished(self):
        if self.sample_heater.current_value is not None:
            return abs(
                (Decimal(self.sample_heater.current_value) - Decimal(self._get_value())) /
                Decimal(self.sample_heater.current_value)
                ) < Decimal('0.02')
        return True

    ramp_temperature = RampControl(
        'Ramp Temperature', 'K',
        get_actual_value=_get_value,
        set_target_value=_set_value,
        get_target_value=get_target_temp,
        stop_ramp=lambda _: None,
        is_finished=_is_finished,
        validator=StaticRangeValidator('0.0', '0.8')
    )
