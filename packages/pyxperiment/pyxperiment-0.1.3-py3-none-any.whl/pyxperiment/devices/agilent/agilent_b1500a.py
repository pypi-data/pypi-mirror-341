"""
    pyxperiment/devices/agilent/agilentB1500A.py: Support for Agilent B1500A Device Analyzer

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

from typing import Union
import wx

from pyxperiment.instrument import (
    VisaInstrument, InstrumentModule, ListControl, ValueControl, BooleanControl
)

from pyxperiment.frames.device_config import (
    DeviceConfig, ModuleView, ControlField, MultiControlView
)
from pyxperiment.frames.basic_panels import (
    CaptionTextPanel
)

class AgilentB1500AAnalyzer(VisaInstrument):
    """
    Support for Agilent B1500A Device Analyzer
    """

    def __init__(self, rm, resource):
        super().__init__(rm, resource)
        self.write('FMT 2')
        self.idn = self.query_id().split(',')
        self.set_options([
            self.adc_zero
        ])
        self.modules = [
            AgilentB1500AAnalyzer.AgilentB151xSMU(self, i) for i in self.ACTIVE_MODULES
            ]

    @staticmethod
    def driver_name():
        return 'Agilent B1500A device analyzer'

    def device_name(self):
        return self.idn[0] + ' ' + self.idn[1] + ' device analyzer'

    def get_adc_zero(self):
        values = self.query('*LRN? 56').split(';')
        return values[3][2:]

    adc_zero = BooleanControl(
        'ADC zero',
        get_func=get_adc_zero,
        set_func=lambda instr, val: instr.write('AZ ' + val)
        )

    ACTIVE_MODULES = ['101', '201']

    class AgilentB151xSMU(InstrumentModule):
        """
        A single SMU module
        """

        def __init__(self, instrument, channel):
            super().__init__('Module ' + str(channel), instrument)
            channel = int(channel)
            self.channel = channel if channel > 100 else channel*100 + 1
            self.set_options([
                BooleanControl(
                    'Channel on',
                    get_func=self.get_output,
                    set_func=self.set_output,
                    true_str='NX', false_str='L'
                    ),
                ListControl('ADC type',
                    dict(zip(self.adc_values, map(str,range(len(self.adc_values))))),
                    self.get_adc_type,
                    self.set_adc_type
                    ),
                BooleanControl(
                    'Series resistor',
                    get_func=self.get_series_resistor,
                    set_func=self.set_series_resistor
                    ),
                BooleanControl(
                    'Filter', self.get_filter, self.set_filter),
                ValueControl('Measured current', 'A', self.get_measure_current()),
                ValueControl('Measured voltage', 'V', self.get_measure_voltage())
            ])

        @staticmethod
        def driver_name():
            return AgilentB1500AAnalyzer.driver_name()

        def write(self, data):
            self.instrument.write(data)# type: ignore

        def query(self, data):
            return self.instrument.query(data)# type: ignore

        def set_output(self, state):
            """
            Set's the output state for specified SMU channel
            """
            self.write(('C' + state + ' ') + str(self.channel))

        def get_output(self):
            """
            Get the output state for specified channel
            """
            values = [int(x) for x in self.query('*LRN? 0')[2:].split(',')]
            values = [x if x > 100 else x*100+1 for x in values]
            if self.channel in values:
                return 1
            return 0

        def set_voltage(self, value):
            """
            Set's the output voltage for specified SMU channel
            """
            self.write('DV ' + str(self.channel) + ',0,' + str(value))

        def get_voltage(self):
            return self.get_voltage_full()[0]

        def set_voltage_full(self, volt, curr_comp, curr_range):
            self.write(
                'DV ' +
                str(self.channel) + ',0,' + str(volt) + ',' +
                str(curr_comp) + ',0,' + str(curr_range)
                )

        def get_voltage_full(self):
            value = self.query('*LRN? ' + str(self.channel/100)).split(',')
            if len(value) > 1:
                return [value[2], value[3], value[5]]
            return [0, 0, 0]

        def set_current(self, value):
            """
            Set's the output current for specified SMU channel
            """
            self.write('DI ' + str(self.channel) + ',0,' + str(value))

        def set_series_resistor(self, value):
            self.write('SSR '  + str(self.channel) + ',' + value)

        def get_series_resistor(self):
            values = self.query('*LRN? ' + str(53)).split(';')
            for value in values:
                value = value[3:].split(',')
                channel = int(value[0])
                if channel < 100:
                    channel = channel*100 + 1
                if channel == self.channel:
                    return value[1]
            return 0

        def set_filter(self, value):
            self.write('FL ' +  value + ',' + str(self.channel))

        def get_filter(self):
            values = self.query('*LRN? ' + str(30)).split(';')
            if len(values) == 1:
                return values[0] 
            for value in values:
                value = value[4:].split(',')
                channel = int(value[0])
                if channel < 100:
                    channel = channel*100 + 1
                if channel == self.channel:
                    return value[1]
            return 0

        adc_values = ['High speed', 'High resolution']

        def set_adc_type(self, value):
            self.write(
                'AAD ' + str(self.channel) +
                (',1' if value == self.adc_values[1] else ',0')
                )

        def get_adc_type(self):
            values = self.query('*LRN? ' + str(55)).split(';')
            for value in values:
                value = value[4:].split(',')
                channel = int(value[0])
                if channel < 100:
                    channel = channel*100 + 1
                if channel == self.channel:
                    return value[1]
            return 0

        def get_measure_current(self):
            return self.query('TI ' + str(self.channel))

        def get_measure_voltage(self):
            return self.query('TV ' + str(self.channel))

    voltage_options = [
        ValueControl(
            'Out Voltage CH' + str(num), 'V',
            lambda x, mod=i: x.modules[mod].get_voltage(),
            lambda x, val, mod=i: x.modules[mod].set_voltage(val)
            )
        for i, num in zip(list(range(len(ACTIVE_MODULES))), ACTIVE_MODULES)
    ]

    current_options = [
        ValueControl(
            'Current CH' + str(num), 'A',
            lambda x, mod=i: x.modules[mod].get_measure_current()
            )
        for i, num in zip(list(range(len(ACTIVE_MODULES))), ACTIVE_MODULES)
    ]

    def get_config_class(self):
        return AgilentB1500AAnalyzerConfig

class AgilentB1500AAnalyzerConfig(DeviceConfig):

    class AgilentB151xSMUPanel(ModuleView):
        """
        A panel for single B151x SMU
        """
        def __init__(self, parent, device, channel):
            super().__init__(parent, 'Channel: ' + str(channel), wx.VERTICAL)
            self.channel_num = int(channel)//100
            self.device = device.modules[self.channel_num-1]
            controls = []
            for option in self.device.get_options():
                control = option_to_control(self, option)
                controls.append(control)
            output_panel = MultiControlView(
                self, None, lambda dev=device: dev.get_voltage_full(),
                lambda x, dev=device: dev.set_voltage_full(*x), wx.VERTICAL)
            output_panel.set_controls([
                CaptionTextPanel(output_panel, 'Voltage, V'),
                CaptionTextPanel(output_panel, 'Current compiance, A'),
                CaptionTextPanel(output_panel, 'Current Range'),
            ])
            controls.append(
                output_panel
            )
            self.set_controls(controls)

    def _create_controls(self):
        self.controls = [
            self.AgilentB151xSMUPanel(self.panel, self.device, i)
            for i in self.device.ACTIVE_MODULES
            ]# type: list[Union[ModuleView,ControlField]]
        for option in self.device.get_options():
            control = option_to_control(self.panel, option)
            self.controls.append(control)
        self.controls_fields = self.controls
        self.columns = len(self.device.ACTIVE_MODULES)
