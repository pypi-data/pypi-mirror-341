"""
    pyxperiment/devices/ami430.py: Support for AMI 430 magnet power supply programmer

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

import wx

from pyxperiment.instrument import (
    VisaInstrument, ValueControl, BooleanControl, RampControl, StaticRangeValidator
)
from pyxperiment.frames.device_config import DeviceConfig
from pyxperiment.frames.basic_panels import CaptionTextPanel

class AMI430Supply(VisaInstrument):
    """
    AMI 430 magnet power supply programmer support
    """

    def __init__(self, rm, resource):
        super().__init__(rm, resource)
        self.inst.read_termination = '\r\n'
        read_str = self.read()
        read_str = self.read()
        del read_str

    @staticmethod
    def driver_name():
        return 'AMI 430 magnet power supply programmer'

    def device_name(self):
        value = self.query_id().translate({ord(c): None for c in ['\r', '\n']}).split(',')
        return value[0] + ' ' + value[1] + ' power source'

    pswitch = BooleanControl(
        'Persistent switch heater',
        get_func=lambda instr: instr.query('PSwitch?'),
        set_func=lambda instr, value: instr.write('PSwitch ' + value)
    )

    def get_coil_const(self):
        return self.query("COIL?")

    volt_limit = ValueControl(
        'Voltage limit', 'V',
        get_func=lambda instr: instr.query('VOLT:LIM?'),
        set_func=lambda instr, value: instr.write('CONF:VOLT:LIM ' + str(value)),
        sweepable=False
    )

    target_field = ValueControl(
        'Target field', 'T',
        get_func=lambda instr: instr.query('FIELD:TARG?'),
        set_func=lambda instr, value: instr.write('CONF:FIELD:TARG ' + str(value)),
        sweepable=False
    )

    field = ValueControl(
        'Magnet field', 'T',
        get_func=lambda instr: instr.query('FIELD:MAG?')
    )

    current = ValueControl(
        'Magnet current', 'A',
        get_func=lambda instr: instr.query('CURR:MAG?')
    )

    voltage = ValueControl(
        'Magnet voltage', 'V',
        get_func=lambda instr: instr.query('VOLT:SUPP?')
    )

    def get_ramp_seg_field(self, num):
        return self.query('RAMP:RATE:FIELD:'+str(num)+'?').split(',')

    def get_ramp_seg_curr(self, num):
        return self.query('RAMP:RATE:CURR:'+str(num)+'?').split(',')

    def set_ramp_seg_curr(self, num, ramp, end):
        self.write('CONF:RAMP:RATE:CURR '+str(num)+','+ramp+','+end)

    def start_ramp(self):
        self.write('RAMP')

    def pause_ramp(self):
        self.write('PAUSE')

    def zero_ramp(self):
        self.write('ZERO')

    state_values = [
        'RAMPING',
        'HOLDING',
        'PAUSED',
        'MANUAL UP',
        'MANUAL DOWN',
        'ZEROING',
        'QUENCH!!!',
        'AT ZERO',
        'HEATING SWITCH',
        'COOLING SWITCH'
    ]

    def get_state(self):
        value = self.query('STATE?')
        return self.state_values[int(value)-1]

    def get_config_class(self):
        return AMI430SupplyConfig

    def set_value(self, value):
        self.target_field.set_value(str(value))
        self.start_ramp()

    def get_value(self):
        return self.field.get_value()

    def _is_finished(self):
        return self.get_state() != self.state_values[0]

    ramp_field = RampControl(
        'Ramp field', 'T',
        get_actual_value=field._fget,
        set_target_value=set_value,
        get_target_value=target_field._fget,
        stop_ramp=pause_ramp,
        is_finished=_is_finished,
        validator=StaticRangeValidator('-9', '9')
    )

class AMI430SupplyConfig(DeviceConfig):

    def __init__(self, parent, device: AMI430Supply):
        DeviceConfig.__init__(self, parent, device, 300)

    def _create_controls(self):
        self.controls = []
        self.columns = 3

        self.target_field = CaptionTextPanel(self.panel, label='Target field', show_mod=True)
        self.controls.append(self.target_field)
        self.voltage_limit = CaptionTextPanel(self.panel, label='Voltage limit', show_mod=True)
        self.controls.append(self.voltage_limit)
        self.coilconst = CaptionTextPanel(self.panel, label='Coil constant')
        self.coilconst.SetEnabled(False)
        self.controls.append(self.coilconst)

        self.field = CaptionTextPanel(self.panel, label='Magnet field')
        self.field.SetEnabled(False)
        self.controls.append(self.field)
        self.volt = CaptionTextPanel(self.panel, label='Magnet voltage')
        self.volt.SetEnabled(False)
        self.controls.append(self.volt)
        self.curr = CaptionTextPanel(self.panel, label='Magnet current')
        self.curr.SetEnabled(False)
        self.controls.append(self.curr)

        self.ramp_segments = 3
        self.ramp_limit = []
        self.ramp_rate = []
        for i in range(self.ramp_segments):
            segment_limit = CaptionTextPanel(self.panel, label='Segment limit', show_mod=True)
            self.controls.append(segment_limit)
            self.ramp_limit.append(segment_limit)
            segment_rate = CaptionTextPanel(self.panel, label='Segment rate', show_mod=True)
            self.controls.append(segment_rate)
            self.ramp_rate.append(segment_rate)

        self.btn_ramp = wx.Button(self.panel, label='Ramp')
        self.Bind(wx.EVT_BUTTON, self.on_btn_ramp, self.btn_ramp)
        self.controls.append(self.btn_ramp)
        self.btn_pause = wx.Button(self.panel, label='Pause')
        self.Bind(wx.EVT_BUTTON, self.on_btn_pause, self.btn_pause)
        self.controls.append(self.btn_pause)
        self.btn_zero = wx.Button(self.panel, label='Zero')
        self.Bind(wx.EVT_BUTTON, self.on_btn_zero, self.btn_zero)
        self.controls.append(self.btn_zero)

        self.pswitch = wx.CheckBox(self.panel, label='Persistent switch heater')
        self.controls.append(self.pswitch)

        self.state = CaptionTextPanel(self.panel, label='State')
        self.state.SetEnabled(False)
        self.controls.append(self.state)

    def on_btn_ramp(self, event):
        self.device.start_ramp()

    def on_btn_pause(self, event):
        self.device.pause_ramp()

    def on_btn_zero(self, event):
        self.device.zero_ramp()

    def read(self):
        self.target_field.SetValue(self.device.get_target_field())
        self.voltage_limit.SetValue(self.device.get_volt_limit())

        self.coilconst.SetValue(self.device.get_coil_const())

        for i in range(1, self.ramp_segments+1):
            seg_field = self.device.get_ramp_seg_field(i)
            seg_curr = self.device.get_ramp_seg_curr(i)
            self.ramp_rate[i-1].SetValue(seg_curr[0])
            self.ramp_limit[i-1].SetValue(seg_field[1])

        self.pswitch.SetValue(self.device.get_pswitch())

    def write(self):
        if self.target_field.IsModified():
            self.device.set_field_target(self.target_field.GetValue())
        if self.pswitch.Value != self.device.get_pswitch():
            self.device.set_pswitch(self.pswitch.Value)
        if self.voltage_limit.IsModified():
            self.device.set_volt_limit(self.voltage_limit.GetValue())
        # Пока только скорость разветки
        for i in range(0, self.ramp_segments):
            if self.ramp_rate[i].IsModified():
                seg_curr = self.device.get_ramp_seg_curr(i+1)
                self.device.set_ramp_seg_curr(i+1, self.ramp_rate[i].GetValue(), seg_curr[1])

    def on_reload_timer(self, event):
        self.field.SetValue(self.device.field.get_value())
        self.volt.SetValue(self.device.voltage.get_value())
        self.curr.SetValue(self.device.current.get_value())
        self.state.SetValue(self.device.get_state())
