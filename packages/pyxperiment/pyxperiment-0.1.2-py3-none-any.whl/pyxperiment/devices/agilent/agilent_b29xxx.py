"""
    pyxperiment/devices/agilent/agilentB2901A.py: Support for Keysight B2901A SMU

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

from decimal import Decimal

from pyxperiment.instrument import (
    VisaInstrument, ListControl, ValueControl, BooleanControl, TimeoutControl
)

class AgilentB29xxxSMU(VisaInstrument):
    """
    Support for Keysight B29xxx SMUs
    """

    def __init__(self, rm, resource):
        super().__init__(rm, resource)
        self.write('*CLS')
        self.idn = self.query_id().split(',')
        self.write(':OUTP:ON:AUTO OFF')

        self.set_options([
            self.output,
            self.function,
            ValueControl('Voltage', 'V', self.get_sour_volt, self.set_sour_volt),
            ValueControl('Current', 'A', self.get_sour_curr, self.set_sour_curr),
            self.volt_range_auto,
            self.volt_range,
            self.curr_range_auto,
            self.curr_range,
            ValueControl('Voltage limit', 'V', self.get_volt_limit, self.set_volt_limit),
            ValueControl('Current limit', 'A', self.get_curr_limit, self.set_curr_limit),
            self.nplc_auto,
            self.nplc,
            self.meas_volt_range_auto,
            self.meas_volt_range,
            self.measured_volt,
            TimeoutControl(self.measured_volt),
            self.measured_curr,
            TimeoutControl(self.measured_curr),
        ])

    @staticmethod
    def driver_name():
        return 'Keysight B29xxx source/measure unit'

    def query(self, data):
        return super().query(data).translate({ord(c): None for c in ['\r', '\n']})

    def device_name(self):
        return self.idn[0] + ' ' + self.idn[1] + ' SMU'

    def device_id(self):
        return self.idn[2]

    def get_value_ch(self, channel):
        """
        Get setting value for a specified channel
        """
        func = self.get_function(channel).lower()
        if func == self.VOLT_NAME:
            return self.get_sour_volt(channel)
        if func == self.CURR_NAME:
            return self.get_sour_curr(channel)
        raise ValueError('Invalid function: ' + func)

    def set_value_ch(self, value, channel):
        """
        Set value for a specified channel
        """
        func = self.get_function(channel).lower()
        if func == self.VOLT_NAME:
            self.set_sour_volt(value, channel)
        elif func == self.CURR_NAME:
            self.set_sour_curr(value, channel)
        else:
            raise ValueError('Invalid function: ' + func)

    def get_phys_q(self, channel):
        func = self.get_function(channel).lower()
        if func == self.VOLT_NAME:
            return 'V'
        if func == self.CURR_NAME:
            return 'A'
        raise ValueError('Invalid function: ' + func)

    channel1 = ValueControl(
        'Channel 1', lambda instr, ch='': instr.get_phys_q(ch),
        lambda instr, ch='': instr.get_value_ch(ch),
        lambda instr, value, ch='': instr.set_value_ch(value, ch),
        )

    channel2 = ValueControl(
        'Channel 2', lambda instr, ch=2: instr.get_phys_q(ch),
        lambda instr, ch=2: instr.get_value_ch(ch),
        lambda instr, value, ch=2: instr.set_value_ch(value, ch),
        )

    output = BooleanControl(
        'Output on',
        get_func=lambda instr: instr.query(':OUTP?'),
        set_func=lambda instr, value: instr.write(f':OUTP {value}'),
        true_str='ON',
        false_str='OFF'
    )

    VOLT_NAME = 'volt'
    CURR_NAME = 'curr'

    function_values = {
        VOLT_NAME:'VOLT',
        CURR_NAME:'CURR',
        }

    def get_function(self, channel=''):
        return self.query(f':SOUR{channel}:FUNC:MODE?')

    def set_function(self, value, channel=''):
        self.write(f':SOUR{channel}:FUNC:MODE {value}')

    function = ListControl(
        'Function', function_values,
        get_func=get_function,
        set_func=set_function
        )

    def get_sour_volt(self, channel=''):
        return self.query(f':SOUR{channel}:VOLT?')

    def set_sour_volt(self, value, channel=''):
        self.write(f':SOUR{channel}:VOLT {value}')

    def get_sour_curr(self, channel=''):
        return self.query(f':SOUR{channel}:CURR?')

    def set_sour_curr(self, value, channel=''):
        self.write(f':SOUR{channel}:CURR {value}')

    def get_volt_limit(self):
        return self.query(':SENS:VOLT:PROT?')

    def set_volt_limit(self, value):
        self.write(':SENS:VOLT:PROT ' + str(value))

    def get_curr_limit(self):
        return self.query(':SENS:CURR:PROT?')

    def set_curr_limit(self, value):
        self.write(':SENS:CURR:PROT ' + str(value))

    nplc_auto = BooleanControl(
        'NPLC auto',
        get_func=lambda instr: instr.query(':SENS:VOLT:NPLC:AUTO?'),
        set_func=lambda instr, value: instr.write(':SENS:VOLT:NPLC:AUTO '+value)
    )

    nplc = ValueControl(
        'NPLC', None,
        get_func=lambda instr: instr.query(':SENS:VOLT:NPLC?'),
        set_func=lambda instr, value: instr.write(':SENS:VOLT:NPLC ' + value),
        enabled=lambda instr: not instr.nplc_auto.get_value(),
        sweepable=False
    )

    meas_volt_range_auto = BooleanControl(
        'Auto voltage range',
        get_func=lambda instr: instr.query(':SENS:VOLT:RANG:AUTO?'),
        set_func=lambda instr, value: instr.write(':SENS:VOLT:RANG:AUTO '+value)
    )

    meas_volt_range_values = ['200', '20', '2', '0.2']

    def _set_meas_volt_range(self, value):
        if value in self.meas_volt_range_values:
            self.write(':SENS:VOLT:RANG '+value)
        else:
            raise ValueError('Invalid range.')

    def _get_meas_volt_range(self):
        value = self.query(':SENS:VOLT:RANG?')
        for range_value in self.meas_volt_range_values:
            if Decimal(range_value) == Decimal(value):
                return range_value
        raise ValueError('Unkwown range ' + value)

    meas_volt_range = ListControl(
        'Voltage range, V',
        meas_volt_range_values,
        get_func=_get_meas_volt_range,
        set_func=_set_meas_volt_range,
        enabled=lambda instr: not instr.meas_volt_range_auto.get_value()
    )

    measured_volt = ValueControl(
        'Measured voltage', 'V',
        get_func=lambda instr: instr.query(':MEAS:VOLT?'),
    )

    measured_curr = ValueControl(
        'Measured current', 'A',
        get_func=lambda instr: instr.query(':MEAS:CURR?'),
    )

    volt_range_auto = BooleanControl(
        'Source voltage range auto',
        get_func=lambda instr: instr.query(':SOUR:VOLT:RANG:AUTO?'),
        set_func=lambda instr, value: instr.write(':SOUR:VOLT:RANG:AUTO '+value),
        true_str='ON',
        false_str='OFF'
    )

    curr_range_auto = BooleanControl(
        'Source current range auto',
        get_func=lambda instr: instr.query(':SOUR:CURR:RANG:AUTO?'),
        set_func=lambda instr, value: instr.write(':SOUR:CURR:RANG:AUTO '+value),
        true_str='ON',
        false_str='OFF'
    )

    volt_range_values = [
        '200',
        '20',
        '2',
        '0.2'
        ]

    curr_range_values = [
        '3',
        '1.5',
        '1',
        '1E-1',
        '1E-2',
        '1E-3',
        '1E-4',
        '1E-5',
        '1E-6',
        '1E-7'
        ]

    def _set_volt_range(self, value):
        if value in self.volt_range_values:
            self.write(':SOUR:VOLT:RANG ' + value)
        else:
            raise ValueError('Invalid range.')

    def _get_volt_range(self):
        value = self.query(':SOUR:VOLT:RANG?')
        for range_value in self.volt_range_values:
            if Decimal(range_value) == Decimal(value):
                return range_value
        raise ValueError('Unkwown range ' + value)

    volt_range = ListControl(
        'Source voltage range, V',
        volt_range_values,
        get_func=_get_volt_range,
        set_func=_set_volt_range,
        enabled=lambda instr: not instr.volt_range_auto.get_value()
    )

    def _set_curr_range(self, value):
        if value in self.curr_range_values:
            self.write(':SOUR:CURR:RANG ' + value)
        else:
            raise ValueError('Invalid range.')

    def _get_curr_range(self):
        value = self.query(':SOUR:CURR:RANG?')
        for range_value in self.curr_range_values:
            if Decimal(range_value) == Decimal(value):
                return range_value
        raise ValueError('Unkwown range ' + value)

    curr_range = ListControl(
        'Source current range, A',
        curr_range_values,
        get_func=_get_curr_range,
        set_func=_set_curr_range,
        enabled=lambda instr: not instr.curr_range_auto.get_value()
    )

    def to_local(self):
        """
        Enable local controls after sweep is over
        """
        self.gpib_to_local()
