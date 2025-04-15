"""
    pyxperiment/devices/tektronix4323.py: Support for Tektronix PWS4323

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
    VisaInstrument, BooleanControl, ValueControl
)

class TektronixPWS4323(VisaInstrument):

    def __init__(self, rm, resource):
        super().__init__(rm, resource)
        self.idn = self.query_id().split(',')
        self.set_options([
            self.current,
            self.voltage,
            self.output
        ])

    output = BooleanControl(
        'Output on',
        get_func=lambda instr: instr.query('OUTP?'),
        set_func=lambda instr, value: instr.write('OUTP ' + value),
        true_str='ON',
        false_str='OFF'
    )

    current = ValueControl(
        'Current', 'A',
        get_func=lambda instr: instr.query('CURR?'),
        set_func=lambda instr, value: instr.write('CURR ' + str(value))
    )

    voltage = ValueControl(
        'Voltage', 'V',
        get_func=lambda instr: instr.query('VOLT?'),
        set_func=lambda instr, value: instr.write('VOLT ' + str(value))
    )

    @staticmethod
    def driver_name():
        return 'TektronixPWS4323'

    def device_name(self):
        return self.idn[0].title() + ' ' + self.idn[1] + ' DC'
