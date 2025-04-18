"""
    examples/simple_measurement.py:
    The example demonstrates how a simple measurement with a small intermediate
    routine can be implemented in pyxperiment. Replace test instruments with the
    real ones to apply to real experimental environment.

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
from pyxperiment import PyXperimentApp, Experiment
from pyxperiment.core.utils import str_to_range
from pyxperiment.data_format.text_data_format import TextDataWriter

from pyxperiment.devices.testdevice import TestDevice

# Application startup
app = PyXperimentApp()

# Instrument connections
# bias_voltage = app.resource_manager.open_instrument(Agilent34xxxDMM, 'GPIB0::1::INSTR')
bias_voltage = app.resource_manager.open_instrument(TestDevice, 'TEST1').rand
# bias_current = app.resource_manager.open_instrument(Yokogawa7651, 'GPIB0::2::INSTR')
bias_current = app.resource_manager.open_instrument(TestDevice, 'TEST2').value
# gate_voltage = app.resource_manager.open_instrument(Yokogawa7651, 'GPIB0::3::INSTR')
gate_voltage = app.resource_manager.open_instrument(TestDevice, 'TEST3').value

experiment = Experiment(app, TextDataWriter('C:\\test\\test*.dat'))
# Add y instruments
experiment.add_readables([bias_voltage])
# Add x range and timeout
experiment.add_writable(bias_current, '1:-0.1:-1', 100)
# Set iterations number, delay between itarations and sweep type
experiment.set_curves_num(2, 1.0, True)
# the array to be used for manual values setting
gate_rearm_range = str_to_range('-3:0.2:4')

# repeat the whole process 10 times
for i in range(10):
    # run the main measurement
    experiment.run(True)
    # perform intermediate routine
    for value in gate_rearm_range:
        gate_voltage.set_value(value)
        time.sleep(0.1)
    # delay after the routine
    time.sleep(3.0)
