"""
    pyxperiment/core/application.py: This module defines the base entity for any
    PyXperiment application

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

import logging
import sys
import wx
import matplotlib

try:
    from pyxperiment.instrument import Instrument, InstrumentFactory
    from pyxperiment.frames.device_config import DeviceConfig
    from pyxperiment.settings.core_settings import CoreSettings
except Exception as ex:# pylint: disable=broad-except
    logging.exception("Exception when imporing modules:")
    raise

class PyXperimentApp():
    """
    The PyXperiment application basebone
    """

    _is_running = False
    _instr_conf_dict = {}# type: dict[Instrument,DeviceConfig]

    def __init__(self) -> None:
        if not hasattr(PyXperimentApp, '_wx_app'):
            # Configure logging and global exception handling
            logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO,
                                handlers=[
                                    logging.FileHandler('logfile.log'), logging.StreamHandler()
                                    ]
                                    )
            sys.excepthook = self.log_excepthook
            # Configure matplotlib to use wxpython
            matplotlib.use('WXAgg')
            if wx.GetApp() is not None:
                PyXperimentApp._wx_app = wx.GetApp()
            else:
                PyXperimentApp._wx_app = wx.App()
            PyXperimentApp._frame = None
            PyXperimentApp._settings = CoreSettings
            # Create resource manager
            PyXperimentApp._resource_manager = InstrumentFactory(
                PyXperimentApp._settings.get_resource_manager()
                )

    @staticmethod
    def log_excepthook(exc_type, exc_value, exc_traceback) -> None:
        """
        Logs the unhandled exception to log file
        """
        if not issubclass(exc_type, KeyboardInterrupt):
            logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
        sys.__excepthook__(exc_type, exc_value, exc_traceback)

    @property
    def frame(self):
        """
        Get the application main frame
        """
        return PyXperimentApp._frame

    @frame.setter
    def frame(self, value) -> None:
        """
        Set the application main frame
        """
        PyXperimentApp._frame = value

    def start(self) -> None:
        """
        Start the application main loop
        """
        if not PyXperimentApp._is_running:
            if self.frame:
                self.frame.Show()
            PyXperimentApp._is_running = True
            PyXperimentApp._wx_app.MainLoop()
            self.frame = None
            PyXperimentApp._is_running = False

    @property
    def resource_manager(self) -> InstrumentFactory:
        """
        Get the global resource manager
        """
        return PyXperimentApp._resource_manager

    @property
    def settings(self):
        """
        Get the global application settings
        """
        return PyXperimentApp._settings

    def show_conf_wnd(self, instr: Instrument) -> None:
        """
        Show the configuration dialog for a specified instrument. PyXperiment ensures, that only
        one such dialog is open for a specified instrument.
        """
        # check if a window is already open
        if instr in PyXperimentApp._instr_conf_dict:
            wnd = PyXperimentApp._instr_conf_dict[instr]
            if wnd:
                return
        # no active window, need to open
        if hasattr(instr, 'get_config_class') and callable(instr.get_config_class):# type: ignore
            config = instr.get_config_class()# type: ignore
            conf_wnd = config(self.frame, instr)# type: ignore
        else:
            conf_wnd = DeviceConfig(self.frame, instr)
        conf_wnd.Show()
        PyXperimentApp._instr_conf_dict[instr] = conf_wnd
