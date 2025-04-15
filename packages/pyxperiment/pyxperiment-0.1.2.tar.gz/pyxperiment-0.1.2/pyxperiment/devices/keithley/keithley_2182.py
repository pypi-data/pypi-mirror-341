"""
    pyxperiment/devices/keithley/keithley2182.py:
    Support for Keithley 2182/2182A nanovoltmeter support

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

from pyxperiment.instrument import (
    VisaInstrument, ListControl, ValueControl, TimeoutControl
)

class Keithley2182Nanovoltmeter(VisaInstrument):
    """
    Keithley 2182/2182A nanovoltmeter support
    """

    def __init__(self, rm, resource):
        super().__init__(rm, resource)
        self.inst.write_termination = '\n'
        self.inst.read_termination = '\n'
        self.write('*CLS')
        self.idn = self.query_id().split(',')
        self.write(':INIT:CONT OFF')
        self.write(':TRIG:SOUR IMM')
        self.write(':TRIG:COUNT 1')
        self.set_options([
            self.meas_range_ch1,
            self.meas_range_ch2,
            self.nplc,
            self.meas_channel,
            self.value,
            TimeoutControl(self.value)
        ])

    @staticmethod
    def driver_name():
        return 'Keithley 2182/2182A nanovoltmeter'

    def device_name(self):
        return self.idn[0].title() + ' ' + self.idn[1] + ' nanovoltmeter'

    def set_nplc(self, value):
        self.write('SENS:VOLT:NPLC ' + str(value))

    def get_nplc(self):
        value = self.query('SENS:VOLT:NPLC?' )
        return value

    nplc = ValueControl(
        'NPLC', None,
        get_func=lambda instr: instr.get_nplc(),
        set_func=lambda instr,value: instr.set_nplc(value),
        sweepable=False
    )

    range_values = [
        '100', '10', '1', '0.1', '0.01'
        ]

    def set_range(self, value, channel=1):
        if value in self.range_values:
            self.write('SENS:VOLT:CHAN' + str(channel) + ':RANG ' + value)
        else:
            raise ValueError('Invalid range.')

    def get_range(self, channel=1):
        value = self.query('SENS:VOLT:CHAN' + str(channel) + ':RANG?')
        for range_value in self.range_values:
            if Decimal(range_value) == Decimal(value):
                return range_value
        raise ValueError('Unkwown range ' + value)

    meas_range_ch1 = ListControl(
        'Range CH1, V',
        range_values,
        get_func=lambda instr: instr.get_range(1),
        set_func=lambda instr,value: instr.set_range(value, 1),
        #enabled=lambda instr: not instr.autorange.get_value(),
    )

    meas_range_ch2 = ListControl(
        'Range CH2, V',
        range_values,
        get_func=lambda instr: instr.get_range(2),
        set_func=lambda instr,value: instr.set_range(value, 2),
        #enabled=lambda instr: not instr.autorange.get_value(),
    )

    meas_channel = ListControl(
        'Active channel', ['1', '2'],
        get_func=lambda instr: instr.query('SENS:CHAN?'),
        set_func=lambda instr, value: instr.write('SENS:CHAN ' + str(value)),
    )

    def to_remote(self):
        self.write(':INIT:CONT OFF')

    value = ValueControl(
        'Value', 'V',
        get_func=lambda instr: instr.query(':READ?')
    )
