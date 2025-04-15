"""
    pyxperiment/devices/ni/nidaq.py:
    Support for 

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

import numpy as np
import logging
try:
    import nidaqmx
    from nidaqmx.constants import TerminalConfiguration, VoltageUnits, AcquisitionType, READ_ALL_AVAILABLE
    from nidaqmx import task as daqtask
except ImportError:
    logging.debug('zhinst failed to import', exc_info=True)
from pyxperiment.instrument import (
    Instrument, ValueControl, StaticRangeValidator
)

class NiDAQmx(Instrument):
    """
    NI DAQmx device
    """

    def __init__(self, rm, resource):
        super().__init__('')
        self.resource = resource

    @staticmethod
    def driver_name():
        return 'NI DAQmx device'

    def device_name(self):
        #value = self.query_id().translate({ord(c): None for c in ['\r', '\n']}).split(',')
        return 'NIDAC'
    
    @property
    def location(self):
        """
        Get device VISA address
        """
        with self._lock:
            return self.resource

    def ai_read(self, num):
        """
        Read the analog input for specified number of samples and return an average
        """
        with self._lock:
            with nidaqmx.Task() as task:
                task.ai_channels.add_ai_voltage_chan(self.resource + f"/ai{num}",
                    min_val=-10.0, max_val=10.0,
                    terminal_config=TerminalConfiguration.DIFF,
                    units=VoltageUnits.VOLTS
                    )
                n_samples = 200
                task.timing.cfg_samp_clk_timing(20000.0, sample_mode=AcquisitionType.FINITE, samps_per_chan=n_samples)
                data = task.read(n_samples)# type: ignore
                mean = np.mean(np.array(data))
                return str(mean)

    def ao_write(self, num, value):
        with self._lock:
            with nidaqmx.Task() as task:
                task.ao_channels.add_ao_voltage_chan(self.resource + f"/ao{num}",
                    min_val=-10.0, max_val=10.0,
                    units=VoltageUnits.VOLTS
                    )
                task.write(float(value))

    def ao_read(self, num):
        with self._lock:
            with nidaqmx.Task() as task:
                task.ai_channels.add_ai_voltage_chan(self.resource + f"/_ao{num}_vs_aognd",
                    min_val=-10.0, max_val=10.0, terminal_config=TerminalConfiguration.DIFF,
                    units=VoltageUnits.VOLTS
                    )
                return str(task.read())

    analog_out = [ValueControl(
        f'Analog Out {i}', 'V',
        get_func=lambda instr, num=i: instr.ao_read(num),
        set_func=lambda instr, x, num=i: instr.ao_write(num, x),
        validator=StaticRangeValidator(-10, 10)
    ) for i in range(2)]

    analog_in = [ValueControl(
        f'Analog In {i}', 'V',
        get_func=lambda instr, num=i: instr.ai_read(num)
    ) for i in range(4)]

    # def measure_iv(self, ramp_rate, v_out_list, v_in_max):
    #     with nidaqmx.Task() as task:
    #         out_ch = task.ao_channels.add_ao_voltage_chan(f"{self.resource}/ao0",
    #             min_val=-10.0, max_val=10.0, units=VoltageUnits.VOLTS
    #             )
    #         task.timing.cfg_samp_clk_timing(ramp_rate, '/Dev1/ai/SampleClock', sample_mode=AcquisitionType.CONTINUOUS)
    #         task.ao_channels.
    #         task.rege
    #         task.write(float(value))
