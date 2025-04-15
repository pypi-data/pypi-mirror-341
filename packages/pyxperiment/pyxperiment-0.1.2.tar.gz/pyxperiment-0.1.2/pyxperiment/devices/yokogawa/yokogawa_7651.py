"""
    pyxperiment/devices/yokogawa/yokogawa7651.py:
    Support for Yokogawa 7651 programmable DC source

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

import re
from decimal import Decimal
import wx

from pyxperiment.instrument import (
    VisaInstrument, ListControl, BooleanControl, ValueControl, DynamicRangeValidator
)
from pyxperiment.frames.device_config import DeviceConfig, ControlField
from pyxperiment.frames.basic_panels import (
    CaptionTextPanel, CaptionDropBox, ModifiedCheckBox
)

class Yokogawa7651(VisaInstrument):
    """
    Support for Yokogawa 7651 programmable DC source
    """

    def __init__(self, rm, resource):
        super().__init__(rm, resource)
        self.clear_buf(4)
        self.inst.write('DL0', '\n')
        self.inst.write('H1', '\n')
        self.set_options([
            ListControl(
                'Function', self.function_values.keys(), self.get_function, self.set_function),
            ListControl(
                'Range', [], self.get_range, self.set_range),
            ValueControl(
                'Voltage limit', 'V', self.get_volt_limit, self.set_volt_limit),
            ValueControl(
                'Current limit', 'mA', self.get_curr_limit, self.set_curr_limit),
            self.value,
            self.output
        ])

    def __read_status(self):
        self.write('OS')
        return [self.read().translate({ord(c): None for c in ['\r', '\n']}) for i in range(5)]

    @staticmethod
    def driver_name():
        return 'Yokogawa 7651/GS200 programmable DC source'

    def device_name(self):
        status = self.__read_status()
        return 'Yokogawa ' + status[0] + ' DC source'

    def get_value(self):
        value = self.query('OD').translate({ord(c): None for c in ['\r', '\n']})
        if value[0] == 'E' and len(value) >= 4:
            return 'Inf'
        if value[0] == 'N' and len(value) > 4:
            return value[4:]
        raise ValueError('Invalid output data: ' + value)

    def set_value(self, value, apply=True):
        self.write('S' + str(value) + ('E' if apply else ''))

    output = BooleanControl(
        'Output on',
        get_func=lambda instr: (int(instr.query('OC')[5:]) & 1 << 4) >> 4,
        set_func=lambda instr, val: instr.write('O' + val)
        )

    function_values = {
        'volt':'F1',
        'curr':'F5',
        }

    def get_function(self):
        status = self.__read_status()
        function = status[1][:2]
        if function == 'F1':
            return 'volt'
        elif function == 'F5':
            return 'curr'
        else:
            raise ValueError('Invalid function: ' + function)

    def set_function(self, value):
        try:
            cmd = self.function_values[value]
        except KeyError as exc:
            raise ValueError('Invalid function: ' + value, exc) from exc
        self.write(cmd)

    volt_range_values = {
        '10 mV':('R2', (Decimal('-0.012'), Decimal('0.012'), Decimal('0.0000001'))),
        '100 mV':('R3', (Decimal('-0.12'), Decimal('0.12'), Decimal('0.000001'))),
        '1 V':('R4', (Decimal('-1.2'), Decimal('1.2'), Decimal('0.00001'))),
        '10 V':('R5', (Decimal('-12'), Decimal('12'), Decimal('0.0001'))),
        '30 V':('R6', (Decimal('-32'), Decimal('32'), Decimal('0.001'))),
        }# type: dict[str, tuple[str, tuple[Decimal, Decimal, Decimal]]]

    curr_range_values = {
        '1 mA':('R4', (Decimal('-0.0012'), Decimal('0.0012'), Decimal('0.00000001'))),
        '10 mA':('R5', (Decimal('-0.012'), Decimal('0.012'), Decimal('0.0000001'))),
        '100 mA':('R6', (Decimal('-0.12'), Decimal('0.12'), Decimal('0.000001'))),
        }# type: dict[str, tuple[str, tuple[Decimal, Decimal, Decimal]]]

    def get_range(self):
        """
        Get the current range.
        """
        status = self.__read_status()
        function = status[1][:2]
        value = status[1][2:4]
        if function == 'F1':
            ranges = self.volt_range_values
        elif function == 'F5':
            ranges = self.curr_range_values
        else:
            raise ValueError('Invalid function: ' + function)
        for val in ranges.items():
            if val[1][0] == value:
                return val
        raise ValueError('Invalid range: ' + value)

    def set_range(self, value):
        try:
            cmd = self.volt_range_values[value]
        except KeyError as exc:
            raise ValueError('Invalid range: ' + value, exc) from exc
        self.write(cmd[0])

    def get_volt_limit(self):
        status = self.__read_status()
        match = re.match("LV([0-9]+)LA([0-9]+)", status[3])
        return match.group(1)# type: ignore

    def set_volt_limit(self, value):
        self.write('LV' + str(value))

    def get_curr_limit(self):
        status = self.__read_status()
        match = re.match("LV([0-9]+)LA([0-9]+)", status[3])
        return match.group(2)# type: ignore

    def set_curr_limit(self, value):
        self.write('LA' + str(value))

    def apply_settings(self):
        """Apply the changed settings"""
        self.write('E')

    def to_local(self):
        self.gpib_to_local()

    function_to_phys_q = {
        'curr': 'A',
        'volt': 'V'
    }

    value = ValueControl(
        'Value', lambda instr: Yokogawa7651.function_to_phys_q[instr.get_function()],
        get_func=get_value, set_func=set_value,
        validator=DynamicRangeValidator(lambda instr: instr.get_range()[1][1])
        )

    def get_config_class(self):
        return Yokogawa7651Config

class Yokogawa7651Config(DeviceConfig):

    def __range_value(self, func):
        def range_value(item):
            return func(item)[1]
        return range_value

    def _create_controls(self):
        self.function = CaptionDropBox(self.panel, 'Function', Yokogawa7651.function_values.keys())
        self.control_views.append(ControlField(self.function, None))
        self.range = CaptionDropBox(self.panel, 'Range', [])
        self.control_views.append(ControlField(self.range, None))
        self.voltage_limit = CaptionTextPanel(self.panel, 'Voltage limit, V', show_mod=True)
        self.control_views.append(ControlField(self.voltage_limit, None))
        self.current_limit = CaptionTextPanel(self.panel, 'Current limit, mA', show_mod=True)
        self.control_views.append(ControlField(self.current_limit, None))
        self.value = CaptionTextPanel(self.panel, 'Value', show_mod=True)
        self.control_views.append(ControlField(self.value, None))
        self.output = ModifiedCheckBox(self.panel, label='Output on')
        self.control_views.append(ControlField(self.output, None))
    
    def read(self):
        self.function.SetValue(self.device.get_function())
        self.function.SetEnabled(False)
        if self.function.GetValue() == 'volt':
            self.range.SetItems(sorted(
                Yokogawa7651.volt_range_values,
                key=self.__range_value(Yokogawa7651.volt_range_values.__getitem__)
                ))
        elif self.function.GetValue() == 'curr':
            self.range.SetItems(sorted(
                Yokogawa7651.curr_range_values,
                key=self.__range_value(Yokogawa7651.curr_range_values.__getitem__)
                ))
        self.range.SetValue(self.device.get_range())
        self.voltage_limit.SetValue(self.device.get_volt_limit())
        self.current_limit.SetValue(self.device.get_curr_limit())
        self.value.SetValue(str(Decimal(self.device.get_value())))
        self.output.SetValue(self.device.output.get_value())

    def write(self):
        if self.output.IsModified() and self.output.GetValue() != self.device.output.get_value():
            dlg = wx.MessageDialog(
                self,
                'Warning! you are trying to modify a' +
                'critical parameter (output on/off, output function). ' +
                'Such modification is potentially dangerous to the connected load. ' +
                'Please check twice before proceeding.',
                'Modification of a critical parameter',
                wx.YES_NO | wx.ICON_WARNING
                )
            if dlg.ShowModal() != wx.ID_YES:
                return
            self.device.output.set_value(self.output.GetValue())
        if self.range.IsModified():
            self.device.set_range(self.range.GetValue())
        if self.value.IsModified():
            self.device.set_value(self.value.GetValue(), False)
        self.device.apply_settings()
        if self.voltage_limit.IsModified():
            self.device.set_volt_limit(self.voltage_limit.GetValue())
        if self.current_limit.IsModified():
            self.device.set_curr_limit(self.current_limit.GetValue())
