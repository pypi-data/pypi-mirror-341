"""
    frames/range_panels.py: This module declares the frames for experiment
    range selection

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

from decimal import Decimal
from abc import abstractmethod
from typing import TypeVar, Generic

import wx

from pyxperiment.settings.group_settings import DeviceSetting, DevicePropertySettings
from pyxperiment.settings.view_settings import ViewSettings
from pyxperiment.core.utils import str_to_range
from pyxperiment.instrument import ValueControl, RampControl
from .basic_panels import CaptionTextPanel
from .plots.simple_plot import SimpleAxisPanel

ValueType = TypeVar("ValueType", bound=ValueControl)
class SweepPanel(wx.Panel, Generic[ValueType]):
    """
    A base class for all sweep panels
    """

    def __init__(self, parent, control: ValueType) -> None:
        wx.Panel.__init__(self, parent)
        self.control = control

        self.edit_delay = CaptionTextPanel(self, 'Delay, ms', size=(120, -1))
        self.edit_delay.edit.SetFont(ViewSettings().RANGE_EDIT_FONT)

    def can_backsweep(self) -> bool:
        """
        Return if the device can sweep in opposide direction
        """
        return not self.control.get_instrument().driver_name() == 'Time'

    def reload(self) -> None:
        """
        Resets the panel
        """

    def new_device_settings(self) -> DeviceSetting:
        """
        Populate new DeviceSetting struct with current device
        """
        device_settings = DeviceSetting()
        instr = self.control.get_instrument()
        device_settings.name = instr.device_name()
        device_settings.address = instr.location
        device_settings.driverName = instr.driver_name()
        device_settings.serial = instr.device_id()
        return device_settings

    def find_sweep_settings(self, settings):
        """
        Find the corresponding sweep settings from device or control
        """
        device_settings = settings.find_device_settings(
            self.control.get_instrument().location,
            self.control.get_instrument().driver_name()
            )
        if device_settings is None:
            return None
        if not isinstance(self.control, ValueControl):
            return device_settings
        return next(filter(
            lambda x: x.name == self.control.name,
            device_settings.properties.get_children()), None
            )

    def save_sweep_settings(self, settings, sweep_range, delay, return_delay):
        """
        Save the sweep settings to respective device or control
        """
        device_settings = settings.find_device_settings(
            self.control.get_instrument().location,
            self.control.get_instrument().driver_name())
        if device_settings is None:
            device_settings = self.new_device_settings()
            settings.add_child(device_settings)
        if not isinstance(self.control, ValueControl):
            device_settings.sweep.range = sweep_range
            device_settings.sweep.delay = delay
            device_settings.sweep.returnDelay = return_delay
            return
        device_property = next(filter(
            lambda x: x.name == self.control.name,
            device_settings.properties.get_children()), None)# type: ignore TODO
        if device_property is None:
            device_property = DevicePropertySettings()
            device_property.name = self.control.name
            device_settings.properties.add_child(device_property)# type: ignore TODO
        device_property.sweep.range = sweep_range
        device_property.sweep.delay = delay
        device_property.sweep.returnDelay = return_delay

    @abstractmethod
    def save_settings(self, settings):
        """
        Save the control settings from the panel.
        """

    @abstractmethod
    def get_range(self) -> str:
        """
        Get the selected range.
        """

    def get_delay(self) -> int:
        """
        Get the target delay between points.
        """
        return int(self.edit_delay.GetValue())

class TimeSweepPanel(SweepPanel[ValueControl]):
    """
    A special class for time sweep panel
    """

    def __init__(self, parent, device, settings):
        SweepPanel.__init__(self, parent, device)

        self.edit_numpoints = CaptionTextPanel(self, 'Num points', size=(240, -1))
        self.edit_numpoints.edit.SetFont(ViewSettings().RANGE_EDIT_FONT)

        device_settings = self.find_sweep_settings(settings)
        if device_settings is None:
            device_settings = self.new_device_settings()
            device_settings.sweep.range = '100'
            device_settings.sweep.delay = '250'
            device_settings.sweep.returnDelay = '0.1'

        self.edit_numpoints.SetValue(device_settings.sweep.range)
        self.edit_delay.SetValue(device_settings.sweep.delay)

        self._vbox = wx.BoxSizer(wx.VERTICAL)
        self._vbox.Add(self.edit_numpoints, flag=wx.ALIGN_CENTRE_HORIZONTAL)
        self._vbox.Add(self.edit_delay, border=5, flag=wx.ALL | wx.ALIGN_CENTRE_HORIZONTAL)
        self.SetSizer(self._vbox)
        self._vbox.Fit(self)

    def save_settings(self, settings):
        self.save_sweep_settings(
            settings, self.edit_numpoints.GetValue(), self.edit_delay.GetValue(), '0.1'
        )

    def get_range(self) -> str:
        delay = Decimal(int(self.edit_delay.GetValue())) / 1000
        numpoints = int(self.edit_numpoints.GetValue())
        return '0:' + str(delay) + ':' + str(delay * (numpoints - 1))

class FieldSweepPanel(SweepPanel[RampControl]):
    """
    A special class for the device with automated sweep (Field, Temperature)
    """

    def __init__(self, parent, control: RampControl, settings):
        super().__init__(parent, control)
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        self.edit_value = CaptionTextPanel(
            self, 'Value', size=(240, -1), show_mod=True, style=wx.TE_PROCESS_ENTER)
        self.edit_value.edit.SetFont(ViewSettings().RANGE_EDIT_FONT)
        self.edit_value.edit.SetEditable(False)
        self.vbox.Add(self.edit_value, flag=wx.ALIGN_CENTRE_HORIZONTAL)

        self.edit_target = CaptionTextPanel(self, 'Target Value', size=(240, -1))
        self.edit_target.edit.SetFont(ViewSettings().RANGE_EDIT_FONT)
        self.vbox.Add(self.edit_target, flag=wx.ALIGN_CENTRE_HORIZONTAL)

        self.vbox.Add(self.edit_delay, border=5, flag=wx.ALL | wx.ALIGN_CENTRE_HORIZONTAL)

        device_settings = self.find_sweep_settings(settings)
        if device_settings is None:
            device_settings = self.new_device_settings()
            device_settings.sweep.range = self.control.get_target_value()
            device_settings.sweep.delay = '250'
            device_settings.sweep.returnDelay = '0.1'

        self.edit_target.SetValue(device_settings.sweep.range)
        self.edit_delay.SetValue(device_settings.sweep.delay)

        self.SetSizer(self.vbox)
        self.vbox.Fit(self)
        self.reload()

    def save_settings(self, settings):
        self.save_sweep_settings(
            settings, self.edit_target.GetValue(), self.edit_delay.GetValue(), '0.1'
        )

    def reload(self):
        self.edit_value.SetValue(self.control.get_target_value())
        self.control.get_instrument().to_local()

    def get_range(self):
        return [self.edit_value.GetValue(), self.edit_target.GetValue()]

class DeviceSweepPanel(SweepPanel[ValueControl]):
    """
    A basic control of writable device (Motion through a set of points).
    """

    def __init__(self, parent, device, settings, show_compiled=True):
        super().__init__(parent, device)
        self.show_compiled = show_compiled
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.edit_value = CaptionTextPanel(self, 'Value', size=(240, -1), show_mod=True, style=wx.TE_PROCESS_ENTER)
        self.edit_value.edit.SetFont(ViewSettings().RANGE_EDIT_FONT)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnEditValue, self.edit_value.edit)
        self.vbox.Add(self.edit_value, flag=wx.ALIGN_CENTRE_HORIZONTAL)

        self.edit_range = CaptionTextPanel(self, 'Range', size=(240, -1))
        self.edit_range.edit.SetFont(ViewSettings().RANGE_EDIT_FONT)
        self.Bind(wx.EVT_TEXT, self.OnEditRange, self.edit_range.edit)
        self.vbox.Add(self.edit_range, flag=wx.ALIGN_CENTRE_HORIZONTAL)

        if self.show_compiled:
            self.edit_range_compiled = CaptionTextPanel(self, 'Compiled range', size=(240, 60), style=wx.TE_MULTILINE)
            self.vbox.Add(self.edit_range_compiled, proportion=1, flag=wx.GROW)
            self.edit_range_compiled.edit.SetEditable(False)
            self.axis_range = SimpleAxisPanel(self)
            self.vbox.Add(self.axis_range, proportion=2, flag=wx.GROW)

        self.vbox.Add(self.edit_delay, border=5, flag=wx.ALL | wx.ALIGN_CENTRE_HORIZONTAL)

        device_settings = self.find_sweep_settings(settings)
        if device_settings is None:
            device_settings = self.new_device_settings()
            device_settings.sweep.range = self.control.get_value()
            device_settings.sweep.delay = '250'
            device_settings.sweep.returnDelay = '0.1'

        self.range = []
        self.edit_range.SetValue(device_settings.sweep.range)
        self.edit_delay.SetValue(device_settings.sweep.delay)

        self.SetSizer(self.vbox)
        self.vbox.Fit(self)
        self.reload()

    def save_settings(self, settings):
        self.save_sweep_settings(
            settings, self.edit_range.GetValue(), self.edit_delay.GetValue(), '0.1'
        )

    def reload(self):
        self.edit_value.SetValue(str(Decimal(self.control.get_value())))
        self.control.get_instrument().to_local()

    def OnEditValue(self, event):
        del event
        if self.edit_value.IsModified():
            self.control.set_value(self.edit_value.GetValue())
        self.edit_value.SetValue(str(Decimal(self.control.get_value())))

    def OnEditRange(self, event):
        del event
        if self.show_compiled:
            self.edit_range_compiled.edit.Value = ''
        self.range = []
        try:
            self.range = str_to_range(self.edit_range.edit.Value)
            if self.show_compiled:
                self.axis_range.plot(range(len(self.range)), [float(el) for el in self.range])
                self.edit_range_compiled.edit.Value = ', '.join([str(el) for el in self.range])
        except:
            pass

    def get_range(self) -> str:
        return str(self.edit_range.edit.Value)

    def validate(self) -> bool:
        # TODO: move to experiment
        if not self.control.check_values(self.range):
            dlg = wx.MessageDialog(
                None, 'The values range contains points, which are unable to be set by selected device.',
                'Wrong dataset', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            return False
        return True
