"""
    pyxperiment/frames/device_select_panel.py:
    The panel for selecting experimental devices

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

from typing import Tuple, Sequence, Optional, cast

import wx
import pyvisa

from pyxperiment.instrument import Instrument, InstrumentControl, InstrumentFactory
from pyxperiment.core.application import PyXperimentApp
from pyxperiment.settings.view_settings import ViewSettings
from pyxperiment.controller.time_device import TimeDevice
from pyxperiment.settings.group_settings import DeviceSetting

class DeviceSelectPanel(wx.Panel):
    """
    The panel for selecting instrument and control for experiment.
    """

    def __init__(
        self, parent, res_manager: InstrumentFactory, is_readable: bool, name: str=''
        ) -> None:
        super().__init__(parent, wx.ID_ANY)
        self.res_manager = res_manager
        self.is_readable = is_readable
        text_name = wx.StaticText(self, label=name)
        text_name.SetFont(ViewSettings().BUTTON_FONT)

        self.dropbox_device = wx.ComboBox(self, style=wx.CB_READONLY)
        self.dropbox_device.SetFont(ViewSettings().MAIN_FONT)

        self.dropbox_control = wx.ComboBox(self, style=wx.CB_READONLY)
        self.dropbox_control.SetFont(ViewSettings().MAIN_FONT)
        self.dropbox_control.Disable()

        self.dropbox_driver = wx.ComboBox(self, style=wx.CB_READONLY)
        self.dropbox_driver.SetFont(ViewSettings().MAIN_FONT)
        self.dropbox_driver.Disable()
        for driver in self.res_manager.list_drivers():
            self.dropbox_driver.Append(driver.driver_name(), driver)

        self.button_configure = wx.Button(self, -1, 'Configure')
        self.button_configure.SetFont(ViewSettings().BUTTON_FONT)
        self.Bind(wx.EVT_BUTTON, self._on_configure, self.button_configure)

        self._instrument = cast(Instrument, None)
        self.Bind(wx.EVT_COMBOBOX, self._on_device_change, self.dropbox_device)
        self._on_device_change(None)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(text_name, 0, wx.ALIGN_CENTRE)
        self.sizer.Add(self.dropbox_device, 0, wx.ALL | wx.GROW)
        self.sizer.Add(self.dropbox_driver, 0, wx.TOP | wx.BOTTOM | wx.GROW, 20)
        self.sizer.Add(self.dropbox_control, 0, wx.BOTTOM | wx.GROW, 20)
        self.sizer.Add(self.button_configure, 0, wx.ALL | wx.ALIGN_RIGHT)
        self.SetSizer(self.sizer)
        self.sizer.Fit(self)

    def set_devices_list(
            self, devices: Sequence[Optional[Tuple[DeviceSetting,type[Instrument]]]]
            ) -> None:
        """
        Set the devices list avialiable in this panel
        """
        self.dropbox_device.Clear()
        for device in devices:
            if device is None:
                self.dropbox_device.Append(str(None), None)
            elif device[1] == TimeDevice:
                self.dropbox_device.Append(TimeDevice.driver_name(), device)
            else:
                self.dropbox_device.Append(device[0].address, device)
        self.dropbox_device.Select(0)
        self._on_device_change(None)

    def _on_device_change(self, event) -> None:
        """
        Called when a new instrument is selected.
        """
        del event
        try:
            self._instrument = self.get_instrument()
        except (pyvisa.errors.VisaIOError) as err:
            wx.MessageBox(err.description)
            self.dropbox_device.Select(0)
            self._instrument = None
        except OSError as err:
            wx.MessageBox(str(err))
            self.dropbox_device.Select(0)
            self._instrument = None
        self.dropbox_control.Disable()
        self.button_configure.Disable()
        self.dropbox_control.Clear()
        if (self._instrument is None or isinstance(self._instrument, TimeDevice)):
            self.dropbox_driver.Select(-1)
            if self._instrument is None:
                return
        else:
            element = self.dropbox_driver.FindString(self._instrument.driver_name())
            self.dropbox_driver.Select(element)
            self.button_configure.Enable()

        controls = (
            self._instrument.get_readable_controls() if self.is_readable
            else self._instrument.get_writable_controls()
            )
        if controls:
            for prop in controls:
                self.dropbox_control.Append(prop.name, prop)
            self.dropbox_control.Select(0)
            if len(controls) > 1:
                self.dropbox_control.Enable()

    def _on_configure(self, event) -> None:
        """
        Called to open the configuration dialog.
        """
        del event
        if self._instrument is not None:
            PyXperimentApp().show_conf_wnd(self._instrument)

    def get_instrument(self) -> Optional[Instrument]:
        """
        Get the instrument, selected by this panel.
        """
        value = self.dropbox_device.GetSelection()
        if value < 0:
            return None
        instr_data = self.dropbox_device.GetClientData(value)# type: Optional[Tuple[DeviceSetting,type[Instrument]]]
        if instr_data is None:
            return None
        return self.res_manager.open_instrument(instr_data[1], instr_data[0].address)

    def get_control(self) -> Optional[InstrumentControl]:
        """
        Get the control, selected by this panel.
        """
        if self._instrument is None:
            return None
        return self.dropbox_control.GetClientData(self.dropbox_control.GetSelection())
