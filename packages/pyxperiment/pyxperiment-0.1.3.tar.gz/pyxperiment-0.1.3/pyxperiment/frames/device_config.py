"""
    pyxperiment/frames/device_config.py:
    The class defining base functions for device configuration dialogs

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

from abc import abstractmethod, ABCMeta
from typing import Union, Optional, Iterable
import time
import wx

from pyxperiment.instrument import (
    Instrument, InstrumentControl, InstrumentModule,
    ActionControl, ListControl, BooleanControl, ValueControl, StateControl, MultiControl
)
from pyxperiment.settings.view_settings import ViewSettings
from .basic_panels import (
    CaptionTextPanel, CaptionDropBox, ModifiedCheckBox, ActionButton
)

class ControlViewBase(metaclass=ABCMeta):
    """
    Base interface for visual representation on instrument controls.
    """

    @abstractmethod
    def read(self) -> None:
        """
        Update the view by reading the controls from instrument.
        """

    @abstractmethod
    def write(self) -> None:
        """
        Update the instrument by sending all the modified values.
        """

    @property
    @abstractmethod
    def view_component(self) -> wx.Window:
        """
        Return the corresponding view component to add into the dialog box.
        """

# All the possible view components
ViewComponent = Union[CaptionTextPanel, CaptionDropBox, ModifiedCheckBox, ActionButton]
# Only view components, that can be both read and written
ViewComponentRW = Union[CaptionTextPanel, CaptionDropBox, ModifiedCheckBox]

class ControlField(ControlViewBase):
    """
    Control field is used to combine instrument control with its visual representation.
    """
    def __init__(
            self, view_component: ViewComponent, control: Optional[InstrumentControl]
            ) -> None:
        self._view_component = view_component
        self.control = control
        if self.control and self.control.is_readable():
            self._view_component.SetEnabled(False)

    @property
    def view_component(self) -> ViewComponent:
        return self._view_component

    def read(self) -> None:
        assert self.control
        if not isinstance(self._view_component, ActionButton):
            start_time = time.perf_counter()
            value = self.control.get_value()
            end_time = time.perf_counter()
            if not isinstance(value, list):
                self._view_component.SetValue(value)
            else:
                self._view_component.SetValue(', '.join(value))
            if isinstance(self.control, ValueControl) and self.control.read_timeout is not None:
                self.control.read_timeout.value = end_time - start_time
            if self.control.is_writable():
                self._view_component.SetEnabled(self.control.is_enabled())

    def write(self) -> None:
        assert self.control
        if self.control.is_writable() and self._view_component.IsModified():
            value = self._view_component.GetValue()# type: ignore
            if isinstance(self.control, ValueControl) and not self.control.check_value(value):
                raise ValueError(f'Invalid value for {self.control.name}: {value}')
            self.control.set_value(value)

class ControlPanelMeta(type(wx.Panel), type(ControlViewBase)):# type: ignore
    pass

class MultiControlView(wx.Panel, ControlViewBase, metaclass=ControlPanelMeta):
    """
    Sometimes an instrument returns several control values for a single function call. PyXperiment
    can manage those avoiding multiple calls of the underlying function.
    """

    def __init__(self, parent, control: MultiControl, orientation=wx.HORIZONTAL):
        super().__init__(parent)
        self.components = []# type: Iterable[ViewComponentRW]
        self.control = control
        self.sizer = wx.BoxSizer(orientation)
        if self.control.name is not None:
            self.sizer.Add(wx.StaticText(self, label=self.control.name), 0, wx.ALL | wx.ALIGN_CENTER, 10)
        for subcontrol in self.control.controls:
            component = create_component(self, subcontrol)
            self.components.append(component)#type: ignore
            self.sizer.Add(component, 0, wx.ALL | wx.GROW, 5)
        self.SetSizer(self.sizer)
        self.sizer.Fit(self)

    @property
    def view_component(self) -> wx.Panel:
        return self

    def read(self):
        for component, value in zip(self.components, self.control.get_value()):
            component.SetValue(value)

    def write(self):
        if any(map(lambda x: x.IsModified(), self.components)):
            self.control.set_value([x.GetValue() for x in self.components])

class ModuleView(wx.Panel, ControlViewBase, metaclass=ControlPanelMeta):
    """
    Control panel combines several control views into a single panel.
    """

    def __init__(self, parent, module: InstrumentModule, orientation=wx.VERTICAL):
        super().__init__(parent)
        self.module = module
        self.control_views = []# type: Iterable[ControlViewBase]
        self.timer_controls = []# type: Iterable[ControlViewBase]
        self.sizer = wx.BoxSizer(orientation)
        if module.name is not None:
            self.sizer.Add(wx.StaticText(self, label=module.name), 0, wx.ALL | wx.ALIGN_CENTER, 10)
        for control in self.module.get_controls(InstrumentControl):
            # MultiControl processed separately
            if isinstance(control, MultiControl):
                control_view = MultiControlView(self, control)
            else:
                control_view = ControlField(create_component(self, control), control)
            if control.is_readable():
                self.timer_controls.append(control_view)
            self.control_views.append(control_view)
            self.sizer.Add(control_view.view_component, 0, wx.ALL | wx.GROW)

        self.SetSizer(self.sizer)
        self.sizer.Fit(self)

    @property
    def view_component(self) -> wx.Panel:
        return self

    def read(self):
        for control_view in (x for x in self.control_views if not x in self.timer_controls):
            control_view.read()

    def write(self):
        for control_view in (x for x in self.control_views if not x in self.timer_controls):
            control_view.write()

class DeviceConfig(wx.Frame, ControlViewBase, metaclass=ControlPanelMeta):
    """
    Instrument configuration panel shows all the controls of an instrument.
    """
    def __init__(self, parent, instr: Instrument, reload_speed:int=100):
        super().__init__(parent, -1, instr.driver_name() + ' config',
                         style=wx.DEFAULT_FRAME_STYLE & (~(wx.RESIZE_BORDER|wx.MAXIMIZE_BOX)))
        self.device = instr
        self.control_views = []# type: list[ControlViewBase]
        self.timer_controls = []# type: list[ControlViewBase]

        self.panel = wx.Panel(self)
        self.name = wx.StaticText(self.panel, label=self.device.device_name())
        self.name.SetFont(ViewSettings().TITLE_FONT)
        self.location = wx.StaticText(self.panel, label=self.device.location)
        self.location.SetFont(ViewSettings().EDIT_FONT)

        self.btn_save = wx.Button(self.panel, label='Save')
        self.Bind(wx.EVT_BUTTON, self._on_save_button, self.btn_save)
        self.btn_load = wx.Button(self.panel, label='Load')
        self.Bind(wx.EVT_BUTTON, self._on_load_button, self.btn_load)

        self._init_view()
        self.read()

        self.reload_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_reload_timer, self.reload_timer)
        self.reload_timer.Start(reload_speed)
        self.Bind(wx.EVT_CLOSE, self._on_close)

    @property
    def view_component(self):
        return self

    def _init_view(self):
        self.columns = 2
        self._create_controls()

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.name, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 10)
        self.vbox.Add(self.location, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        for i in range(0, len(self.control_views), self.columns):
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            for j in range(self.columns):
                if i+j < len(self.control_views):
                    hbox.Add(self.control_views[i+j].view_component, 1, wx.GROW | wx.ALL, 2)
            self.vbox.Add(hbox, 0, wx.GROW | wx.LEFT | wx.RIGHT, 10)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.btn_save, 0, border=10, flag=wx.ALL)
        hbox.Add(self.btn_load, 0, border=10, flag=wx.ALL)
        self.vbox.Add(hbox, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.panel.SetSizer(self.vbox)
        self.vbox.Fit(self)

    def _on_close(self, _):
        self.reload_timer.Stop()
        self.Destroy()
        self.device.to_local()

    def _on_save_button(self, _):
        self.write()
        self.read()
        self.Refresh()

    def _on_load_button(self, _):
        self.read()
        self.Refresh()

    def _create_controls(self):
        # Create views for all modules
        for module in self.device.get_controls(InstrumentModule):
            self.control_views.append(ModuleView(self.panel, module))
        # Create views for all controls
        for control in self.device.get_options():
            # MultiControl processed separately
            if isinstance(control, MultiControl):
                control_view = MultiControlView(self.panel, control)
            else:
                control_view = ControlField(create_component(self.panel, control), control)
            if control.is_readable():
                self.timer_controls.append(control_view)
            self.control_views.append(control_view)

    def read(self):
        for control in (x for x in self.control_views if not x in self.timer_controls):
            control.read()

    def write(self):
        for control in (x for x in self.control_views if not x in self.timer_controls):
            control.write()

    def on_reload_timer(self, event):
        """
        Periodically called to update controls.
        """
        del event
        for control in self.timer_controls:
            control.read()

def create_component(panel, control: InstrumentControl) -> ViewComponent:
    """
    This method creates a corresponding GUI element for a device control.
    """
    if isinstance(control, ListControl):
        return CaptionDropBox(panel, control.name, control.values_list())
    if isinstance(control, BooleanControl):
        return ModifiedCheckBox(panel, control.name)
    if isinstance(control, ValueControl):
        phys_q = control.get_phys_q()
        return CaptionTextPanel(
            panel, control.name + ('' if phys_q is None else (', ' + phys_q)), show_mod=True
            )
    if isinstance(control, StateControl):
        return CaptionTextPanel(panel, control.name)
    if isinstance(control, ActionControl):
        return ActionButton(panel, control.name, control.set_value)
    raise Exception("Unknown control type: ", str(type(control)))
