"""
    pyxperiment/devices/rohde_schwarz/znb.py:
    Support for Rohde&Schwarz ZNB Network Analyzer

    This file is part of the PyXperiment project.

    Copyright (c) 2021 PyXperiment Developers

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
    VisaInstrument, ValueControl, BooleanControl, SweepControl, StaticRangeValidator
)

class ZNB(VisaInstrument):
    """
    Rohde & Schwarz ZNB vector analyzer support
    """

    def __init__(self, rm, resource):
        super().__init__(rm, resource)
        self.inst.write_termination = '\n'
        self.inst.read_termination = '\n'
        self.write('*CLS')
        self.idn = self.query_id().split(',')
        self.set_options([
            self.power,
            self.output
        ])

    @staticmethod
    def driver_name():
        return 'Rohde & Schwarz ZNB vector analyzer'

    def device_name(self):
        return self.idn[0].title() + ' ' + self.idn[1] + ' power source'

    def device_id(self):
        return self.idn[2] if self.idn[2] != '0' else 'Unknown'

    bandwindth = ValueControl(
        'Bandwidth', 'Hz',
        get_func=lambda instr: instr.query('BAND?'),
        set_func=lambda instr, val: instr.write('BAND ' + str(val)),
        validator=StaticRangeValidator(1, 1e6)
    )

    power = ValueControl(
        'Power', 'dBm',
        get_func=lambda instr: instr.query('SOUR:POW?'),
        set_func=lambda instr, val: instr.write('SOUR:POW ' + str(val)),
        validator=StaticRangeValidator(-100, 0)
    )

    output = BooleanControl(
        'Output on',
        get_func=lambda instr: instr.query('OUTP?'),
        set_func=lambda instr, val: instr.write('OUTP ' + val),
        true_str='ON', false_str='OFF'
    )

    trace = SweepControl(
        'Trace', ('Frequency', 'Power'), ('Hz', 'dBm'),
        get_func=None
    )
