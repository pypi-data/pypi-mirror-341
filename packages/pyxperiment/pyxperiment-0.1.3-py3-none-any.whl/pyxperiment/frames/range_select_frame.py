"""
    pyxperiment/frames/range_select_frame.py:
    The frame for experiment range selection

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

import threading
import time
from typing import Sequence

import wx

from pyxperiment.core import PyXperimentApp
from pyxperiment.core import Experiment
from pyxperiment.data_format.text_data_format import TextDataWriter
from pyxperiment.data_format.columned_data_format import ColumnedDataWriter
from pyxperiment.settings.core_settings import CoreSettings
from pyxperiment.settings.view_settings import ViewSettings
from pyxperiment.instrument import InstrumentControl, SweepControl, RampControl

from .basic_panels import CaptionTextPanel, CaptionDropBox
from .range_panels import SweepPanel, TimeSweepPanel, FieldSweepPanel, DeviceSweepPanel

class RangeSelectFrame(wx.Frame):
    """
    This dialog is used to select the range for writable controls of on experiment.
    """

    def __get_device_panel(self, control: InstrumentControl, device_settings) -> SweepPanel:
        """
        Selects the correct panel depending on the InstrumentControl type.
        """
        if control.get_instrument().device_name() == 'Time':
            panel = TimeSweepPanel(self.panel, control, device_settings)
        elif self.xdevices.index(control) == 0 and isinstance(control, RampControl):
            panel = FieldSweepPanel(self.panel, control, device_settings)
        else:
            panel = DeviceSweepPanel(self.panel, control, device_settings)
        return panel

    STR_MODE_DEFAULT = 'Default (n-D scan)'
    STR_MODE_SIMULTANEOUS = 'Simultaneous scan'
    STR_MODE_SEQUENTIAL = 'Sequential scan'

    def __init__(
        self, parent, data_writer,
        ydevices: Sequence[InstrumentControl], xdevices: Sequence[InstrumentControl]
        ):
        super().__init__(parent, wx.ID_ANY, 'Select range')
        self.parent = parent
        self.panel = wx.Panel(self)

        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.data_writer = data_writer
        self.xdevices = xdevices
        self.ydevices = ydevices
        self.range = []

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.hbox_devices = wx.BoxSizer(wx.HORIZONTAL)

        device_settings = CoreSettings.get_device_settings()

        # For each x
        self.device_panels = [
            self.__get_device_panel(xdevice, device_settings) for xdevice in xdevices
            ]
        for panel in self.device_panels:
            self.hbox_devices.Add(panel, proportion=1, border=5, flag=wx.ALL|wx.GROW)
        self.vbox.Add(self.hbox_devices, proportion=1, border=5, flag=wx.ALL|wx.GROW)

        # One for all
        self.edit_iterations = CaptionTextPanel(self.panel, 'Iterations', size=(120, -1))
        self.edit_iterations.edit.SetFont(ViewSettings().EDIT_FONT)

        self.edit_iterations_delay = CaptionTextPanel(self.panel, 'Delay between iterations, s', size=(120, -1))
        self.edit_iterations_delay.edit.SetFont(ViewSettings().EDIT_FONT)

        self.checkbox_backsweep = wx.CheckBox(self.panel, label='Sweep both directions')
        self.checkbox_fastascolumns = wx.CheckBox(self.panel, label='Fast device as columns')
        self.combobox_sweep_mode = CaptionDropBox(
            self.panel,
            'Sweep mode',
            [self.STR_MODE_DEFAULT, self.STR_MODE_SIMULTANEOUS, self.STR_MODE_SEQUENTIAL]
            )
        self.combobox_sweep_mode.combo.SetSelection(0)
        self.checkbox_cumulative = wx.CheckBox(self.panel, label='View all curves')

        self.hbox_iterations = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox_iterations.Add(self.edit_iterations, proportion=1, border=5, flag=wx.ALL|wx.GROW)
        self.hbox_iterations.Add(self.edit_iterations_delay, proportion=1, border=5, flag=wx.ALL|wx.GROW)
        self.hbox_iterations.Add(self.checkbox_backsweep, border=5, flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL)

        self.vbox.Add(self.hbox_iterations, flag=wx.ALL|wx.ALIGN_CENTRE_HORIZONTAL)

        self.hbox_extras = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox_extras.Add(self.combobox_sweep_mode, proportion=1, border=5, flag=wx.ALL|wx.GROW)
        self.hbox_extras.Add(self.checkbox_fastascolumns, proportion=1, border=5, flag=wx.ALL|wx.GROW)
        self.hbox_extras.Add(self.checkbox_cumulative, proportion=1, border=5, flag=wx.ALL|wx.GROW)

        self.vbox.Add(self.hbox_extras, flag=wx.ALL|wx.ALIGN_CENTRE_HORIZONTAL)

        self.edit_filename = CaptionTextPanel(self.panel, 'File name', size=(350, -1))
        self.edit_filename.edit.SetFont(ViewSettings().SMALL_FONT)
        self.vbox.Add(self.edit_filename, border=5, flag=wx.ALL|wx.GROW)

        self.__load_settings()

        self.btn_start = wx.Button(self.panel, label='Start', size=(100, 35))
        self.btn_start.SetFont(ViewSettings().BUTTON_FONT)
        self.Bind(wx.EVT_BUTTON, self.on_start, self.btn_start)
        self.btn_cancel = wx.Button(self.panel, label='Cancel', size=(100, 35))
        self.btn_cancel.SetFont(ViewSettings().BUTTON_FONT)
        self.Bind(wx.EVT_BUTTON, self.on_close, self.btn_cancel)

        self.hbox_buttons = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox_buttons.Add(self.btn_start, border=5, flag=wx.ALL)
        self.hbox_buttons.Add(self.btn_cancel, border=5, flag=wx.ALL)

        self.vbox.Add(self.hbox_buttons, flag=wx.ALIGN_CENTER_HORIZONTAL)
        self.panel.SetSizer(self.vbox)
        self.vbox.Fit(self)

        self.parent.Disable()
        self.Center()
        self.SetFocus()
        self.__reload()

    def __reload(self):
        self.data_writer.update_filename()
        self.edit_filename.SetValue(self.data_writer.get_filename())
        for panel in self.device_panels:
            panel.reload()

    def __load_settings(self):
        """
        Load the most recent experiment settings from the configuration file.
        """
        sweep_settings = CoreSettings.get_sweep_settings()
        self.edit_iterations.SetValue(sweep_settings.iterations)
        self.edit_iterations_delay.SetValue(sweep_settings.iterationsDelay)
        if self.validate_backsweep():
            self.checkbox_backsweep.SetValue(sweep_settings.backsweep)
        else:
            self.checkbox_backsweep.SetValue(False)
            self.checkbox_backsweep.Disable()
        if self.validate_simultaneous() or self.validate_sequential():
            self.combobox_sweep_mode.SetValue(sweep_settings.sweepMode)
        else:
            self.combobox_sweep_mode.combo.SetSelection(0)
            self.combobox_sweep_mode.Disable()
        if self.validate_fastascolumns():
            self.checkbox_fastascolumns.SetValue(sweep_settings.fastAsColumns)
        else:
            self.checkbox_fastascolumns.SetValue(False)
            self.checkbox_fastascolumns.Disable()
        self.checkbox_cumulative.SetValue(sweep_settings.cumulativeView)

    def save_settings(self):
        """
        Save the experiment settings into configuration file.
        """
        device_settings = CoreSettings.get_device_settings()
        for panel in self.device_panels:
            panel.save_settings(device_settings)
        CoreSettings.set_device_settings(device_settings)

        sweep_settings = CoreSettings.get_sweep_settings()
        sweep_settings.iterations = self.edit_iterations.GetValue()
        sweep_settings.iterationsDelay = self.edit_iterations_delay.GetValue()
        if self.validate_backsweep():
            sweep_settings.backsweep = self.checkbox_backsweep.IsChecked()
        if self.validate_simultaneous() or self.validate_sequential():
            sweep_settings.sweepMode = self.combobox_sweep_mode.GetValue()
        if self.validate_fastascolumns():
            sweep_settings.fastAsColumns = self.checkbox_fastascolumns.IsChecked()
        sweep_settings.cumulativeView = self.checkbox_cumulative.IsChecked()
        CoreSettings.set_sweep_settings(sweep_settings)

    def validate_fastascolumns(self) -> bool:
        """
        Check if "Fast as columns" option is possible to activate.
        """
        return (
            len(self.ydevices) == 1 and
            len(self.device_panels) > 1 and
            not any(isinstance(device, SweepControl) for device in self.ydevices)
            )

    def validate_backsweep(self) -> bool:
        """
        Check if backsweep option can be activated.
        """
        return self.device_panels[0].can_backsweep()

    def validate_simultaneous(self) -> bool:
        """
        Check, if a simultaneous mode can be run with current settings:
        only two devices, both regular sweep.
        """
        if len(self.device_panels) != 2:
            return False
        if (
                not isinstance(self.device_panels[0], DeviceSweepPanel) or
                not isinstance(self.device_panels[1], DeviceSweepPanel)
            ):
            return False
        return True

    def validate_sequential(self) -> bool:
        """
        Check, if a simultaneous mode can be run with current settings:
        at least two devices
        """
        if len(self.device_panels) < 2:
            return False
        return True

    def sequential_task(self, experiments) -> None:
        """
        This task is used to sequentually run experiments of several writable parameters.
        """
        for i in range(int(self.edit_iterations.GetValue())):
            for experiment in experiments:
                experiment.data_writer.update_filename()
                experiment.data_context.rearm()
                experiment.data_context.start()
                while not experiment.data_context.finished:
                    time.sleep(0.1)

    def run_sequential_mode(self) -> None:
        """
        Runs the sequential mode experiment.
        """
        experiments = []
        for panel in self.device_panels:
            experiment = Experiment(PyXperimentApp(), self.data_writer)
            experiment.add_readables(self.ydevices)
            if isinstance(panel, FieldSweepPanel):
                experiment.add_observable(panel.control, panel.get_range(), int(panel.edit_delay.edit.Value))
            else:
                experiment.add_writable(panel.control, panel.get_range(), int(panel.edit_delay.edit.Value))
            experiment.set_curves_num(
                1,
                float(self.edit_iterations_delay.GetValue()),
                False
            )
            experiments.append(experiment)
        
        for experiment in experiments:
            experiment.run(False, self, False)
        thread = threading.Thread(target=self.sequential_task, args=(experiments,))
        thread.start()

    def on_start(self, event):
        """
        Called when the Start button is pushed.
        """
        del event
        if self.combobox_sweep_mode.GetValue() == self.STR_MODE_SIMULTANEOUS:
            if not self.validate_simultaneous():
                dlg = wx.MessageDialog(
                    self, 'Simultaneous sweep only possible with two normal x devices.',
                    'Wrong set of devices', wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                return
            if len(self.device_panels[0].get_range()) != len(self.device_panels[1].get_range()):
                dlg = wx.MessageDialog(
                    self, 'Simultaneous sweep needs equal length for x devices.',
                    'Wrong x values', wx.OK | wx.ICON_INFORMATION
                    )
                dlg.ShowModal()
                return
        if self.combobox_sweep_mode.GetValue() == self.STR_MODE_SEQUENTIAL:
            if not self.validate_sequential():
                dlg = wx.MessageDialog(
                    self, 'Sequential only possible with at least two x devices.',
                    'Wrong set of devices', wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                return

        if self.checkbox_backsweep.IsChecked():
            if not self.validate_backsweep():
                dlg = wx.MessageDialog(
                    self, 'It is not possible to sweep both directions in time scans.',
                    'No backsweep for time scans', wx.OK | wx.ICON_INFORMATION
                    )
                dlg.ShowModal()
                return
            if self.combobox_sweep_mode.GetValue() == self.STR_MODE_SEQUENTIAL:
                dlg = wx.MessageDialog(
                    self, 'It is not possible to sweep both directions in sequential scans.',
                    'No backsweep for sequential scans', wx.OK | wx.ICON_INFORMATION
                    )
                dlg.ShowModal()
                return

        if self.checkbox_fastascolumns.IsChecked():
            if not self.validate_fastascolumns():
                dlg = wx.MessageDialog(
                    self, 'Saving Y data in columns is only possible with a single Y device.',
                    'Too many Y devices', wx.OK | wx.ICON_INFORMATION
                    )
                dlg.ShowModal()
                return
            if self.combobox_sweep_mode.GetValue() != self.STR_MODE_DEFAULT:
                dlg = wx.MessageDialog(
                    self, 'Only default mode can be combined with saving Y data in columns.',
                    'Wrong settings', wx.OK | wx.ICON_INFORMATION
                    )
                dlg.ShowModal()
                return

        # TODO: check if modified
        if self.checkbox_fastascolumns.IsChecked():
            self.data_writer = ColumnedDataWriter(self.data_writer.name_exp)
        else:
            self.data_writer = TextDataWriter(self.data_writer.name_exp)

        if self.combobox_sweep_mode.GetValue() == self.STR_MODE_SEQUENTIAL:
            self.run_sequential_mode()
            return
        experiment = Experiment(PyXperimentApp(), self.data_writer)
        try:
            experiment.add_readables(self.ydevices)
            if self.combobox_sweep_mode.GetValue() == self.STR_MODE_SIMULTANEOUS:
                experiment.add_double_writable(
                    self.device_panels[0].control, self.device_panels[1].control,
                    self.device_panels[0].get_range(), self.device_panels[1].get_range(),
                    int(self.device_panels[0].edit_delay.edit.Value)
                    )
            elif self.combobox_sweep_mode.GetValue() == self.STR_MODE_DEFAULT:
                for panel in self.device_panels:
                    if isinstance(panel, FieldSweepPanel):
                        experiment.add_observable(
                            panel.control, panel.get_range(), int(panel.edit_delay.edit.Value)
                            )
                    else:
                        experiment.add_writable(
                            panel.control, panel.get_range(), int(panel.edit_delay.edit.Value)
                            )
        except Exception as ex:
            dlg = wx.MessageDialog(
                None, str(ex),
                'Wrong dataset', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            return

        experiment.set_curves_num(
            int(self.edit_iterations.GetValue()),
            float(self.edit_iterations_delay.GetValue()),
            self.checkbox_backsweep.IsChecked()
            )

        experiment.set_cumulative_view(self.checkbox_cumulative.IsChecked())
        self.save_settings()
        experiment.run(False, self)

    def Enable(self):
        """
        Reenables the controls after experiment has finished.
        """
        self.__reload()
        wx.Frame.Enable(self)

    def on_close(self, event) -> None:
        """
        Called when the window is closed.
        """
        del event
        self.save_settings()
        self.Destroy()
        self.parent.Enable()
        self.parent.SetFocus()
