"""
    pyxperiment/controller/data_storage/data_access.py:
    Describes a general interface for data access

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

from abc import ABCMeta, abstractmethod
from typing import Any, Sequence

from pyxperiment.controller import ControlManager, ReadableManager

class SweepAccessor(metaclass=ABCMeta):
    """
    A result of a single sweep
    """

    @abstractmethod
    def read_data(self) -> list[Any]:
        """
        Get all the values from readed devices
        """

    @abstractmethod
    def write_data(self) -> list[Any]:
        """
        Get all the values from writable devices
        """

    @abstractmethod
    def time_markers(self) -> list[Any]:
        """
        Get the time markers for this measurement trace
        """

class DataAccessor(metaclass=ABCMeta):
    """
    Gives access to the measured data for the entire experiment
    """

    @abstractmethod
    def get_curve(self, index: int) -> SweepAccessor:
        """
        Return the dataset for a specified curve.

        Parameters
        ----------
        index: int
            The index of the sweep to fetch (-1 = the last).

        Returns
        -------
        SweepProvider: SweepAccessor
            The fetched sweep object
        """

    @abstractmethod
    def get_data(self) -> list[SweepAccessor]:
        """
        Get all the stored curves.

        Returns
        -------
        list[SweepAccessor]
        """

    @abstractmethod
    def get_length(self) -> int:
        """
        Returns the total number of sweeps present

        Returns
        -------
        int
            The number of sweeps available
        """

    @abstractmethod
    def get_sweepables(self) -> Sequence[ControlManager]:
        """
        Returns all the controls being managed
        """

    @abstractmethod
    def get_measurables(self) -> Sequence[ReadableManager]:
        """
        Returns all the controls being acquired
        """
