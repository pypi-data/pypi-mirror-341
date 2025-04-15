"""
    pyxperiment/settings/view_settings.py:
    This module declares programm setting groups, accessible elsewhere via
    core_settings module

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

import wx

from pyxperiment.core.utils import Singleton

class ViewSettings(metaclass=Singleton):
    """
    Describes the view setting for the application
    """
    def __init__(self) -> None:
        #print(wx.ScreenDC().GetPPI())
        self.HEADER_FONT = wx.Font(wx.FontInfo(18).Bold())
        self.TITLE_FONT = wx.Font(wx.FontInfo(16).Bold())
        self.MAIN_FONT = wx.Font(wx.FontInfo(12))
        self.BUTTON_FONT = wx.Font(wx.FontInfo(12).Bold())
        self.RANGE_EDIT_FONT = wx.Font(wx.FontInfo(12).Bold())
        self.SMALL_FONT = wx.Font(wx.FontInfo(10).Bold())
        self.EDIT_FONT = wx.Font(wx.FontInfo(12).Bold())
