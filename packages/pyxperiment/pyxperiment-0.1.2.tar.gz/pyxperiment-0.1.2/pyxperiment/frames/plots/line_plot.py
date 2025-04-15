"""
    pyxperiment/frames/plots/line_plot.py: The module defining line plot panel
    for data representation

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

from enum import Enum
from math import isnan
from typing import cast, Optional
import itertools

import wx
import numpy as np
import pylab

from matplotlib.figure import Figure
from matplotlib.ticker import ScalarFormatter
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx

from pyxperiment.data_storage import DataAccessor
from pyxperiment.instrument import SweepControl, ValueControl

class NavigationToolbar(NavigationToolbar2Wx):
    """
    A custom NavigationToolbar replacement to fix the rubberband glitches
    """

    def __init__(self, canvas):
        NavigationToolbar2Wx.__init__(self, canvas)
        self.last_rubberband = None

    def _init_toolbar(self):
        pass

    def draw_rubberband(self, event, x0, y0, x1, y1):
        self.last_rubberband = (x0, y0, x1, y1)
        NavigationToolbar2Wx.draw_rubberband(self, event, x0, y0, x1, y1)

    def remove_rubberband(self):
        self.last_rubberband = None
        NavigationToolbar2Wx.remove_rubberband(self)

    def redraw_rubberband(self):
        if self.last_rubberband != None:
            NavigationToolbar2Wx.draw_rubberband(self, None, *self.last_rubberband)# type: ignore

    def is_nav_at_home(self):
        return self._nav_stack() is None or self._nav_stack[0] == self._nav_stack[-1]# type: ignore

class DataViewMode(Enum):
    SIMPLE = 1
    CUMULATIVE = 2

class MyScalarFormatter(ScalarFormatter):
    """
    Minor tweaks to display the exponent along the value
    """

    def __init__(self):
        super().__init__(False, True, None)
        self.set_powerlimits((-3, 4))

    def get_offset(self):
        return ''

    def _set_format(self, *arg):
        super()._set_format(*arg)# type: ignore
        offset = super().get_offset().lstrip('$')
        if offset:
            self.format = self.format.rstrip('$') + offset

class DataViewAxis(wx.Panel):
    """
    The Panel, showing a line plot of a single physical quantity
    """

    # 14 standard colors for the plots
    PLOT_COLORS = [
        (1, 1, 0), (1, 0, 0), (0, 1, 0),
        (0, 0, 1), (0, 1, 1), (1, 0, 1),
        (1, 1, 1),
        (0.5, 0.5, 0), (0.5, 0, 0), (0, 0.5, 0),
        (0, 0, 0.5), (0, 0.5, 0.5), (0.5, 0, 0.5),
        (0.5, 0.5, 0.5),
        ]

    def __init__(self, parent, data_provider: DataAccessor, mode=DataViewMode.SIMPLE):
        super().__init__(parent, wx.ID_ANY, size=(500,400))

        self.data_provider = data_provider
        self.mode = mode

        # Will effectively set the minimal figure size
        self.fig = Figure((1, 1), dpi=100, facecolor='lightgray')
        self.canvas = FigCanvas(self, -1, self.fig)
        self.toolbar = NavigationToolbar(self.canvas)
        self.toolbar.RemoveTool(self.toolbar.wx_ids['Subplots'])

        self.axes = self.fig.add_subplot(111)
        if callable(getattr(self.axes, 'set_facecolor', None)):
            self.axes.set_facecolor('black')
        else:
            self.axes.set_axis_bgcolor('black')# type: ignore
        self.axes.grid(True, color='gray')

        pylab.setp(self.axes.get_xticklabels(), fontsize=9)
        pylab.setp(self.axes.get_yticklabels(), fontsize=9)
        self.axes.get_xaxis().set_major_formatter(MyScalarFormatter())
        self.axes.get_yaxis().set_major_formatter(MyScalarFormatter())

        self.cb_autox = wx.CheckBox(
            self, -1, "Auto scale X", style=wx.ALIGN_RIGHT)
        self.Bind(wx.EVT_CHECKBOX, self._on_cb_xlab, self.cb_autox)
        self.cb_autox.SetValue(False)

        self.sweepable = self.data_provider.get_sweepables()[0]
        self.measurable = self.data_provider.get_measurables()[0]
        self.axes.set_title(
            'Reading from: ' + self.measurable.get_instrument().device_name() +
            ' at ' + self.measurable.get_instrument().location,
            size=10
            )

        self._set_axes_labels()

        if self.measurable.num_channels() > len(self.PLOT_COLORS):
            self.PLOT_COLORS = [self.PLOT_COLORS[1]] * self.measurable.num_channels()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer_controls = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_controls.Add(self.toolbar, 0, wx.ALIGN_LEFT)
        self.sizer_controls.Add(self.cb_autox, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.sizer.Add(self.canvas, 1, flag=wx.ALL | wx.GROW)
        self.sizer.Add(self.sizer_controls, 0, flag=wx.ALIGN_LEFT | wx.TOP)
        self.SetSizer(self.sizer)
        self.sizer.Fit(self)
        self.Bind(wx.EVT_SIZE, self._on_resize, self)

        # Create initial curves
        self.plot_curves = [
            self.axes.plot(
                [], linewidth=1, color=self.PLOT_COLORS[i], scalex=False, scaley=False
                )[0]
            for i in range(self.measurable.num_channels())
            ]
        self.current_curve = 0
        self.ylimits = np.zeros(2)*np.nan
        if isinstance(self.measurable.get_control(), SweepControl):
            self.cb_autox.Value = True
            self.cb_autox.Disable()
        self._set_xscale()

    @staticmethod
    def _format_phys_q(phys_q):
        if phys_q is None:
            return ''
        return ' (' + phys_q + ')'

    def _set_axes_labels(self):
        # TODO: create a more general way
        control = self.measurable.get_control()
        # For Sweep devices we take both labels from this control
        if isinstance(control, SweepControl):
            phys_q = cast(tuple[Optional[str],Optional[str]],control.get_phys_q())
            self.axes.set_xlabel(
                control.get_axes_names()[0] + self._format_phys_q(phys_q[0])
                )
            self.axes.set_ylabel(
                control.get_axes_names()[1] + self._format_phys_q(phys_q[1])
                )
            return
        # For Value devices we take the proper name
        if isinstance(control, ValueControl):
            self.axes.set_ylabel(
                control.name + self._format_phys_q(control.get_phys_q())
                )
        control = self.sweepable.get_control()
        if isinstance(control, ValueControl):
            self.axes.set_xlabel(
                control.name + self._format_phys_q(control.get_phys_q())
                )

    def _on_resize(self, event):
        event.Skip()
        size = self.GetSize()
        if size.x > 250 and size.y > 250:
            self.fig.subplots_adjust(
                left=80.0/size.x, right=1-30.0/size.x, top=1-30.0/size.y, bottom=55.0/size.y
                )

    def _set_xscale(self):
        if not isinstance(self.measurable.get_control(), SweepControl):
            xdata = self.sweepable.values
            self.axes.set_xbound(lower=min(xdata), upper=max(xdata))

    def _on_cb_xlab(self, event):
        del event
        if not self.cb_autox.Value:
            self._set_xscale()
        self.draw_plot()

    def _plot_sweep_data(self, sweep):
        # Get the actual data
        if isinstance(self.measurable.get_control(), SweepControl):
            if not sweep.read_data():
                return
            data = sweep.read_data()[-1]
            xdata = data[0]
            ydata = data[1]
        else:
            xdata = sweep.write_data()
            ydata = sweep.read_data()
        # if sweep is not finished yet, cut it
        xdata = np.fromiter(xdata, float, len(ydata))
        # Convert data to floats
        for i, curve in enumerate(self.plot_curves):
            if len(self.plot_curves) > 1:
                ydata_ch = np.fromiter(
                    itertools.islice((float(x[i]) for x in ydata), xdata.size), float, xdata.size
                    )
            else:
                ydata_ch = np.fromiter(
                    itertools.islice((float(x) for x in ydata), xdata.size), float, xdata.size
                    )
            # Update the y axis limits
            if ydata_ch.size > 0:
                self.ylimits[0] = ydata_ch.min() if isnan(self.ylimits[0]) else min(self.ylimits[0], ydata_ch.min()) 
                self.ylimits[1] = ydata_ch.max() if isnan(self.ylimits[1]) else max(self.ylimits[1], ydata_ch.max()) 
            # Update data
            curve.set_xdata(xdata)
            curve.set_ydata(ydata_ch)
        # Update x axis limits if required
        if self.cb_autox.Value and xdata.size:
            self.axes.set_xbound(lower=xdata.min(), upper=xdata.max())

    def draw_plot(self):
        """
        Redraws the plot
        """
        sweeps_ready = self.data_provider.get_length()
        if not sweeps_ready:
            return

        if self.mode == DataViewMode.CUMULATIVE:
            # If new curves appeared
            while sweeps_ready-1 > self.current_curve:
                self._plot_sweep_data(
                    self.data_provider.get_curve(self.current_curve)
                    )
                # Make previous curves faint
                for curve in self.plot_curves:
                    curve.set_color([col / 3 for col in curve.get_color()])# type: ignore
                # Create new curves
                self.plot_curves = [
                    self.axes.plot(
                        [], linewidth=1, color=self.PLOT_COLORS[i], scalex=False, scaley=False
                        )[0]
                    for i in range(self.measurable.num_channels())
                ]
                self.current_curve += 1
        else:
            self.ylimits *= np.nan

        sweep = self.data_provider.get_curve(-1)
        # TODO: check that data actually changed
        self._plot_sweep_data(sweep)

        if np.all(np.isfinite(self.ylimits)):
            margin = (self.ylimits[1] - self.ylimits[0]) / 10
            if margin == 0:
                margin = 0.1
            if self.toolbar.is_nav_at_home():
                self.axes.set_ybound(lower=self.ylimits[0] - margin, upper=self.ylimits[1] + margin)

        self.canvas.draw()
        self.toolbar.redraw_rubberband()
