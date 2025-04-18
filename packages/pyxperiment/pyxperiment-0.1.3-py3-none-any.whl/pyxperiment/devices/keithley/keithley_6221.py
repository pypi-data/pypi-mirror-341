"""
    pyxperiment/devices/keithley/keithley_6221.py:
    Support for Keithley 6221 pulse source support

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
import numpy as np

from pyxperiment.instrument import (
    VisaInstrument, BooleanControl, ValueControl, SweepControl
)

class Keithley6221ACDC(VisaInstrument):
    """
    Keithley 6221 pulse source support
    """
    def __init__(self, rm, resource):
        super().__init__(rm, resource)
        self.inst.write_termination = '\n'
        self.inst.read_termination = '\n'
        self.idn = self.query_id().split(',')
        self.write('*RST')
        self.write('SOUR:PDEL:LOW 0')
        self.write('SOUR:PDEL:HIGH ' + str(1e-9))
        self.write('SOUR:PDEL:INT ' + str(5))
        self.write('SOUR:PDEL:SWE ON')
        self.write('SOUR:PDEL:COUN ' + str(4))
        self.write('SOUR:SWE:SPAC LIN')
        self.write('SOUR:SWE:RANG BEST')
        self.write('SOUR:CURR:STAR ' + str(0e-9))
        self.write('SOUR:CURR:STOP ' + str(10e-9))
        self.write('SOUR:CURR:STEP ' + str(1e-9))
        self.write('SOUR:DEL 1')
        self.set_options([
        self.pulse_width,
        self.current_start,
        self.current_stop,
        self.current_step,
        self.current_time,
        self.output_earth
        ])
        pw = float(self.query('SOUR:PDEL:WIDT?'))
        self.write('SOUR:PDEL:SDEL ' + str(pw / 2))

    current_start = ValueControl(
        'Start Current', 'A',
        get_func=lambda instr: instr.query('SOUR:CURR:STAR?'),
        set_func=lambda instr, value: instr.write('SOUR:CURR:STAR ' + str(value)),
        sweepable=False
    )

    current_stop = ValueControl(
        'Stop Current', 'A',
        get_func=lambda instr: instr.query('SOUR:CURR:STOP?'),
        set_func=lambda instr, value: instr.write('SOUR:CURR:STOP ' + str(value)),
        sweepable=False
    )

    current_step = ValueControl(
        'Step Current', 'A',
        get_func=lambda instr: instr.query('SOUR:CURR:STEP?'),
        set_func=lambda instr, value: instr.write('SOUR:CURR:STEP ' + str(value)),
        sweepable=False
    )

    pulse_width = ValueControl(
        'pulse width', 's',
        get_func=lambda instr: instr.query('SOUR:PDEL:WIDT?'),
        set_func=lambda instr, value: instr.write('SOUR:PDEL:WIDT ' + str(value)),
        sweepable=False
    )

    current_time = ValueControl(
        'Time between points', 's',
        get_func=lambda instr: instr.query('SOUR:DEL?'),
        set_func=lambda instr, value: instr.write('SOUR:DEL ' + str(value)),
        sweepable=False
    )

    output_earth = BooleanControl(
        'Earth',
        get_func=lambda instr: instr.query('OUTP:LTE?'),
        set_func=lambda instr, value: instr.write('OUTP:LTE ' + value),
        true_str='ON',
        false_str='OFF'
    )


    @staticmethod
    def driver_name():
        return 'Keithley6221ACsource'

    def device_name(self):
        value = self.query_id().translate({ord(c): None for c in ['\r', '\n']}).split(',')
        return value[0] + value[1]

    @property
    def channels_num(self):
        return 1

    def get_trace(self):
        start_current = float(self.query('SOUR:CURR:STAR?'))
        step_current = float(self.query('SOUR:CURR:STEP?'))
        stop_current= float(self.query('SOUR:CURR:STOP?'))
        time_interval_current = float(self.query('SOUR:DEL?'))
        self.write('TRAC:CLE')
        self.write('TRAC:POIN 500')
        self.write('SOUR:PDEL:ARM')
        self.write('INIT:IMM')
        time.sleep((stop_current-start_current)/step_current*time_interval_current+5)
        self.write('SOUR:SWE:ABOR')
        data = self.query('TRAC:DATA?')
        """x = data.split(',')[1::2]"""
        timedata_list = data.split(',')[1::2]
        y = data.split(',')[::2]
        """x = data.split(',')[1::2]"""
        timedata = np.array(timedata_list, dtype=float)
        x_array = start_current + timedata / time_interval_current * step_current
        x = [str(value) for value in x_array]
        return x, y

    sweep = SweepControl(
        'Keithley sweep', ('Current', 'Voltage'), ('A', 'V'),
        get_func=get_trace
    )
