"""
    pyxperiment/devices/agilent/agilent_dsox12xx.py:
    Support for Keysight DSOX12xx Oscilloscopes

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

from pyxperiment.instrument import (
    VisaInstrument, ListControl, ValueControl, BooleanControl
)

class KeysightDSOX12xxScope(VisaInstrument):
    """
    Support for Keysight DSOX12xx Oscilloscopes.
    Tested with DSOX1204G.
    """

    @staticmethod
    def driver_name():
        return 'Keysight DSOX12xx Oscilloscope'

    def __init__(self, rm, resource):
        super().__init__(rm, resource)
        self.inst.write_termination = '\n'
        self.inst.read_termination = '\n'
        self.idn = self.query_id().split(',')
        self.set_options([
            self.function,
            self.impedance,
            self.output,
            self.offset
        ])

    def device_name(self):
        return self.idn[0] + ' ' + self.idn[1] + ' Oscilloscope'

    def device_id(self):
        return self.idn[2]

    function = ListControl(
        'Function',
        dict(zip(
            ['Sine', 'Square', 'Ramp', 'Pulse', 'Noise', 'DC'],
            ['SIN', 'SQU', 'RAMP', 'PULS', 'NOIS', 'DC']
            )),
        get_func=lambda instr: instr.query('WGEN:FUNC?'),
        set_func=lambda instr, val: instr.write('WGEN:FUNC ' + val)
    )

    impedance = ListControl(
        'Impedance', dict(zip(['1 MOhm', '50 Ohm'], ['ONEM', 'FIFT'])),
        get_func=lambda instr: instr.query('WGEN:OUTP:LOAD?'),
        set_func=lambda instr, val: instr.write('WGEN:OUTP:LOAD ' + val)
    )

    output = BooleanControl(
        'Output',
        get_func=lambda instr: instr.query('WGEN:OUTP?'),
        set_func=lambda instr, val: instr.write('WGEN:OUTP ' + val)
    )

    offset = ValueControl(
        'Offset', 'V',
        get_func=lambda instr: instr.query('WGEN:VOLT:OFFS?'),
        set_func=lambda instr, val: instr.write('WGEN:VOLT:OFFS ' + str(val))
    )
    