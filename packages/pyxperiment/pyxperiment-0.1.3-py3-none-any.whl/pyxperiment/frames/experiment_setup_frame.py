"""
    pyxperiment/frames/experiment_setup_frame.py: The frame for experiment setup

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

import os
from typing import cast

import wx

from pyxperiment.instrument import InstrumentControl, InstrumentFactory
from pyxperiment.settings.core_settings import CoreSettings
from pyxperiment.settings.group_settings import DeviceSetting
from pyxperiment.settings.view_settings import ViewSettings
from pyxperiment.controller.time_device import TimeDevice
from pyxperiment.data_format.text_data_format import TextDataWriter

from .device_library_frame import DeviceLibraryFrame
from .device_select_panel import DeviceSelectPanel
from .range_select_frame import RangeSelectFrame
from .app_settings_frame import AppSettingsFrame

class ExperimentSetupFrame(wx.Frame):
    """
    Experiment setup window
    """

    def __init__(self, res_manager: InstrumentFactory, num_readers: int, num_writers: int):
        wx.Frame.__init__(self, None, -1, 'Experiment setup')
        self.panel = wx.Panel(self)
        self.res_manager = res_manager

        self.reader_panels = [
            DeviceSelectPanel(
                self.panel, self.res_manager, True, name="Y-device " + str(reader+1) + ":"
                ) for reader in range(num_readers)
        ]

        self.writer_panels = [
            DeviceSelectPanel(
                self.panel, self.res_manager, False, name="X-device:" if writer == 0
                else "X-device slow:"
                ) for writer in range(num_writers)
        ]

        self.update_devices()

        text_label = wx.StaticText(self.panel, label='Device selection')
        text_label.SetFont(ViewSettings().HEADER_FONT)

        text_path = wx.StaticText(self.panel, label='Path to save data files:')
        text_path.SetFont(ViewSettings().BUTTON_FONT)
        self.edit_path = wx.TextCtrl(
            self.panel, -1, size=(35, -1), value=str(CoreSettings.get_last_path())
            )
        self.edit_path.SetFont(ViewSettings().MAIN_FONT)
        self.button_select_path = wx.Button(self.panel, label='Select')
        self.button_select_path.SetFont(ViewSettings().MAIN_FONT)
        self.Bind(wx.EVT_BUTTON, self.on_select_path, self.button_select_path)

        self.btn_start = wx.Button(self.panel, label='Start', size=(-1, 35))
        self.btn_start.SetFont(ViewSettings().BUTTON_FONT)
        self.Bind(wx.EVT_BUTTON, self.on_start_button, self.btn_start)
        self.btn_exit = wx.Button(self.panel, label='Exit', size=(-1, 35))
        self.btn_exit.SetFont(ViewSettings().BUTTON_FONT)
        self.Bind(wx.EVT_BUTTON, self.on_close, self.btn_exit)
        self.btn_library = wx.Button(self.panel, label='Devices', size=(-1, 35))
        self.btn_library.SetFont(ViewSettings().BUTTON_FONT)
        self.Bind(wx.EVT_BUTTON, self.on_library_button, self.btn_library)
        self.btn_settings = wx.Button(self.panel, label='Settings', size=(-1, 35))
        self.btn_settings.SetFont(ViewSettings().BUTTON_FONT)
        self.Bind(wx.EVT_BUTTON, self.on_settings_button, self.btn_settings)

        self._box_readers = wx.BoxSizer(wx.HORIZONTAL)
        self._box_readers.AddSpacer(20)
        for panel in self.reader_panels:
            self._box_readers.Add(panel, 1, flag=wx.GROW)
            self._box_readers.AddSpacer(20)

        self._box_writers = wx.BoxSizer(wx.HORIZONTAL)
        self._box_writers.AddSpacer(20)
        for panel in self.writer_panels:
            self._box_writers.Add(panel, 1, flag=wx.GROW)
            self._box_writers.AddSpacer(20)

        self._box_buttons = wx.BoxSizer(wx.HORIZONTAL)
        self._box_buttons.Add(self.btn_start, 1, border=20, flag=wx.GROW|wx.LEFT|wx.RIGHT)
        self._box_buttons.Add(self.btn_exit, 1, border=20, flag=wx.GROW|wx.LEFT|wx.RIGHT)
        self._box_buttons.Add(self.btn_library, 1, border=20, flag=wx.GROW|wx.LEFT|wx.RIGHT)
        self._box_buttons.Add(self.btn_settings, 1, border=20, flag=wx.GROW|wx.LEFT|wx.RIGHT)

        self._box_path = wx.BoxSizer(wx.HORIZONTAL)
        self._box_path.AddSpacer(20)
        self._box_path.Add(self.edit_path, 1)
        self._box_path.AddSpacer(20)
        self._box_path.Add(self.button_select_path, 0)
        self._box_path.AddSpacer(20)

        self._vbox = wx.BoxSizer(wx.VERTICAL)
        self._vbox.AddSpacer(10)
        self._vbox.Add(text_label, 0, flag=wx.ALIGN_CENTRE_HORIZONTAL)
        self._vbox.AddSpacer(20)
        self._vbox.Add(self._box_readers, 1, flag=wx.GROW)
        self._vbox.AddSpacer(50)
        self._vbox.Add(self._box_writers, 1, flag=wx.GROW)
        self._vbox.AddSpacer(50)
        self._vbox.Add(text_path, 0, flag=wx.ALIGN_CENTRE_HORIZONTAL)
        self._vbox.Add(self._box_path, 0, flag=wx.TOP | wx.GROW)
        self._vbox.AddSpacer(10)
        self._vbox.Add(self._box_buttons, 0, flag=wx.TOP | wx.GROW)
        self._vbox.AddSpacer(10)

        self.panel.SetSizer(self._vbox)
        self._vbox.Fit(self)
        self.Center()
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def update_devices(self) -> None:
        """
        Update the devices list in all the controls.
        """
        saved_resources = list(filter(
            lambda x: x.driverName != 'Time',
            CoreSettings.get_device_settings().get_children()
        ))
        drivers = self.res_manager.list_drivers()
        drivers = {driver.driver_name() : driver for driver in drivers}
        # Find the instruments without a valid name
        bad_instruments = set(filter(lambda x: not x.driverName in drivers.keys(), saved_resources))
        for instr in bad_instruments:
            wx.MessageDialog(
                self,
                'The instrument driver: ' + instr.driverName + ' cannot be found. ' +
                'Please update the device library.',
                'Invalid instrument driver',
                wx.OK | wx.ICON_WARNING
                ).ShowModal()
        saved_resources = [
            (setting, drivers[setting.driverName])
            for setting in saved_resources if not setting in bad_instruments
            ]
        readable_devices = list(filter(lambda x: x[1].is_readable(), saved_resources))
        writable_devices = list(filter(lambda x: x[1].is_writable(), saved_resources))
        for ind, panel in enumerate(self.reader_panels):
            panel.set_devices_list(
                ([None] if ind > 0 else []) + readable_devices
            )
        for ind, panel in enumerate(self.writer_panels):
            panel.set_devices_list(
                ([None] if ind > 0 else [(DeviceSetting(), TimeDevice)]) + writable_devices
            )

    def on_select_path(self, event) -> None:
        """
        Opens a dialog to select the path for the data files.
        """
        del event
        dlg = wx.FileDialog(self, "Select path for data files...", os.getcwd(), "", "*.dat",
                            wx.FD_SAVE)
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            self.edit_path.Value = dlg.GetPath()
            CoreSettings.set_last_path(self.edit_path.Value)
        dlg.Destroy()

    def on_start_button(self, event) -> None:
        """
        Starts the experiment.
        """
        del event
        writer = TextDataWriter(self.edit_path.Value)
        CoreSettings.set_last_path(self.edit_path.Value)
        select_range = RangeSelectFrame(
            self, writer,
            cast(list[InstrumentControl], list(filter(
                lambda x: x is not None, map(DeviceSelectPanel.get_control, self.reader_panels)
                ))),
            cast(list[InstrumentControl], list(filter(
                lambda x: x is not None, map(DeviceSelectPanel.get_control, self.writer_panels)
                )))
            )
        select_range.Show()

    def on_library_button(self, event) -> None:
        """
        Opens the instrument library dialog.
        """
        del event
        library_frame = DeviceLibraryFrame(self, self.res_manager)
        library_frame.Show()

    def on_settings_button(self, event) -> None:
        """
        Opens the application settings dialog.
        """
        del event
        settings_frame = AppSettingsFrame(self)
        settings_frame.Show()

    def on_experiment_closed(self, event) -> None:
        """
        Is called when experiment has finished.
        """
        del event
        self.Enable()

    def on_close(self, event) -> None:
        """
        Called when the window is closed.
        """
        del event
        self.Destroy()
