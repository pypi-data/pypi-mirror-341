"""
    pyxperiment/controller/data_storage.py: The storage for experimental data

    This file is part of the PyXperiment project.

    Copyright (c) 2021 PyXperiment Developers

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

class SweepStorage():
    """
    A result of a single sweep
    """

    def __init__(self, time, writable, readables):
        self._time = time
        self._wrdata = writable.values
        self._rddata = [rdev._values for rdev in readables]

    def read_data(self):
        """
        Get all the values from readed devices
        """
        return self._rddata

    def write_data(self):
        """
        Get all the values from writable devices
        """
        return self._wrdata

    def time_markers(self):
        """
        Get the time markers for this measurements
        """
        return self._time

class DataStorage():
    """
    Stores the measured data for the entire experiment
    """

    def __init__(self, sweepables, measurables, repeat_num):
        self._curves = []
        self._sweepables = sweepables
        self._measurables = measurables
        self._repeat_num = repeat_num

    def add_curve(self, time, writable, readables):
        """
        Aggregates readable and writable data in a single set.
        The data is not copied, but referenced to account for modifications.
        """
        self._curves.append(SweepStorage(time, writable, readables))

    def get_curve(self, index):
        """
        Return the dataset for a specified curve.

        Parameters
        ----------
        index : int
            The index of the sweep to fetch (-1 = the last).

        Returns
        -------
        SweepProvider
            The fetched sweep object
        """
        return self._curves[index]

    def get_repeat_num(self):
        """
        Returns the number of times curves are measured with
        same parameters.

        Returns
        -------
        int
        """
        return self._repeat_num

    def get_data(self):
        """
        Get all the stored curves.

        Returns
        -------
        list of SweepProvider
        """
        return self._curves

    def get_sweepables(self):
        return self._sweepables

    def get_measurables(self):
        return self._measurables
