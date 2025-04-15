"""
    pyxperiment/devices/attocubeANC300.py: Support for ANC300 piezo controller

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

import re
from pyxperiment.instrument import (
    VisaInstrument, ValueControl, InstrumentModule, ListControl, ActionControl, BooleanControl
)

class AttocubeANC300(VisaInstrument):
    """
    ANC300 piezo controller support
    """

    DEFAULT_PORT = 7230
    PWD = '123456'
    ACTIVE_MODULES = [1, 2, 3]

    def __init__(self, rm, resource):
        super().__init__(rm, resource)
        self.modules = [AttocubeANC300.ANM300Channel(self, i) for i in self.ACTIVE_MODULES]
        self.inst.write_termination = '\r\n'
        self.inst.read_termination = '\r\n'
        with self._lock:
            self.inst.read_raw()
            line = self.inst.read()
            self.inst.write(self.PWD)
            line = self.inst.read()
            while line != 'Authorization success':
                line = self.inst.read()
            self.inst.write('echo off')
            line = self.inst.read()
            while line != 'OK':
                line = self.inst.read()

    def write(self, data):
        with self._lock:
            self.inst.write(data)
            line = self.inst.read()
            while line != 'OK':
                line = self.inst.read()

    def query(self, data):
        with self._lock:
            ret = self.inst.query(data)
            match = re.match('([^ =]+) += +([^ ]+)', ret)
            ret = match.group(2)# type: ignore
            line = self.inst.read()
            while line != 'OK':
                line = self.inst.read()
            return ret

    @staticmethod
    def driver_name():
        return 'ANC300 piezo controller (' + str(AttocubeANC300.DEFAULT_PORT) + ')'

    def device_name(self):
        return 'Attocube ANC300 piezo controller'

    class ANM300Channel(InstrumentModule):
        """
        Represents a single ANM300 channel of ANC300
        """
        def __init__(self, instrument: VisaInstrument, chnum: int):
            super().__init__('Channel ' + str(chnum), instrument)
            self.chnum = chnum
            self._steps = 0

            self.mode = ListControl(
                'Mode', self.modes_dict, self._get_mode, self._set_mode
                )
            self.dc_in = BooleanControl(
                'DC-IN', self._get_dc_in, self._set_dc_in
                )
            self.filter = ListControl(
                'Filter', self.filters_dict, self._get_filter, self._set_filter
                )
            self.step_freq = ValueControl(
                'Step frequency', 'Hz', self._get_step_freq, self._set_step_freq, sweepable=False
                )
            self.step_voltage = ValueControl(
                'Step voltage', 'V', self._get_step_volt, self._set_step_volt, sweepable=False
            )
            self.offset_voltage = ValueControl(
                'Offset voltage', 'V', self._get_offset_volt, self._set_offset_volt
            )
            self.capacitance = ValueControl(
                'Capacitance', 'nF', self._get_capacitance, sweepable=False
            )
            self.output_voltage = ValueControl(
                'Output voltage', 'V', self.get_output
            )
            self.steps = ValueControl(
                'Steps count', None, self.get_steps, self.set_steps, sweepable=False
            )
            self.step_forward = ActionControl(
                'Step forward', self._step_forward
            )
            self.step_backward = ActionControl(
                'Step forward', self._step_backward
            )
            self.stop = ActionControl(
                'Stop', self._stop
            )

        modes_dict = {
            'Ground':'gnd',
            'AC-IN/DC-IN only':'inp',
            'Cap. measurement':'cap',
            'Stepping only':'stp',
            'Offset only':'off',
            'Offset + stepping':'stp+',
            'Offset - stepping':'stp-'
        }

        def _get_mode(self):
            return self.instrument.query('getm ' + str(self.chnum))

        def _set_mode(self, mode):
            self.instrument.write('setm ' + str(self.chnum) + ' ' + mode)

        def _get_dc_in(self):
            data = self.instrument.query('getdci ' + str(self.chnum))
            return data == 'on'

        def _set_dc_in(self, value):
            self.instrument.write('setdci ' + str(self.chnum) + ' ' + ('on' if value else 'off'))

        def _get_step_freq(self):
            data = self.instrument.query('getf ' + str(self.chnum))
            return data

        def _set_step_freq(self, freq):
            self.instrument.write('setf ' + str(self.chnum) + ' ' + str(freq))

        def _get_step_volt(self):
            data = self.instrument.query('getv ' + str(self.chnum))
            return data

        def _set_step_volt(self, volt):
            self.instrument.write('setv ' + str(self.chnum) + ' ' + str(volt))

        def _get_offset_volt(self):
            data = self.instrument.query('geta ' + str(self.chnum))
            return data

        def _set_offset_volt(self, volt):
            self.instrument.write('seta ' + str(self.chnum) + ' ' + str(volt))

        filters_dict = {
            'Off':'off',
            '16 Hz':'16',
            '160 Hz':'160'
        }

        def _get_filter(self):
            return self.instrument.query('getfil ' + str(self.chnum))

        def _set_filter(self, value):
            self.instrument.write('setfil ' + str(self.chnum) + ' ' + value)

        def _get_capacitance(self):
            return self.instrument.query('getc ' + str(self.chnum))

        def get_output(self):
            return self.instrument.query('geto ' + str(self.chnum))

        def get_steps(self):
            return str(self._steps)

        def _step_forward(self, steps=1):
            self.instrument.write('stepu ' + str(self.chnum) + ' ' + str(steps))
            self.instrument.write('stepw ' + str(self.chnum))
            self._steps += int(steps)

        def _step_backward(self, steps=1):
            self.instrument.write('stepd ' + str(self.chnum) + ' ' + str(steps))
            self.instrument.write('stepw ' + str(self.chnum))
            self._steps -= int(steps)

        def _stop(self):
            self.instrument.write('stop ' + str(self.chnum))

        def set_steps(self, value):
            value = int(value)
            current = self._steps
            if value > current:
                self._step_forward(value - current)
            elif value < current:
                self._step_backward(current - value)

    stepping_params = []
    scanning_params = []
    output_params = []
    for i, num in zip(list(range(len(ACTIVE_MODULES))), ACTIVE_MODULES):
        stepping_params.append(ValueControl(
            'Axis ' + str(num) + ' stepping', '',
            lambda instr, mod=i: instr.modules[mod].get_steps(),
            lambda instr, val, mod=i: instr.modules[mod].set_steps(val)))
        scanning_params.append(ValueControl(
            'Axis ' + str(num) + ' scanning', '',
            lambda instr, mod=i: instr.modules[mod].get_offset_volt(),
            lambda instr, val, mod=i: instr.modules[mod].set_offset_volt(val)))
        output_params.append(ValueControl(
            'Axis ' + str(num) + ' output', '',
            lambda instr, mod=i: instr.modules[mod].get_output()))
