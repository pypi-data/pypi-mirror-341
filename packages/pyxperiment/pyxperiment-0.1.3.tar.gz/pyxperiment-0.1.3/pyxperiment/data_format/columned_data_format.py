"""
    pyxperiment/data_format/columned_data_format.py:
    Implements the data storaging for columned scans

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

import datetime
import itertools
from .text_data_format import TextDataWriter

class ColumnedDataWriter(TextDataWriter):
    """
    Implements the data storaging for columned scans
    """

    def after_sweep(self, num, data_storage):
        if num == 1:
            self.save_internal(data_storage)
            self.update_filename()

    def save_file(self, timecol, xcol, data):
        file_name = self.get_filename()
        with open(file_name, "w") as text_file:
            for i in range(len(xcol)):
                if i >= len(timecol):
                    print('NaN', end=' ', file=text_file)
                elif isinstance(timecol[i], datetime.datetime):
                    print(datetime.datetime.isoformat(timecol[i]), end=' ', file=text_file)
                else:
                    print(str(int(timecol[i]*1000)), end=' ', file=text_file)
                print(str(xcol[i]), end=' ', file=text_file)
                if i < len(timecol):
                    print(*[str(data_line[i]) for data_line in data], file=text_file)
                else:
                    print(*['NaN' for data_line in data], file=text_file)

    def save_internal(self, data_storage):
        """
        Save the measured data to file
        """
        wr_data = list(
            itertools.chain.from_iterable(
                itertools.repeat(x, data_storage.get_repeat_num())
                for x in data_storage.get_sweepables()[1].values
                ))
        curves = data_storage.get_data()
        rd_data = []
        for i in range(len(curves[0].read_data()[0])):
            rd_data.append(list((curve.read_data()[0][i] if i < len(curve.read_data()[0]) else 'NaN') for curve in curves))
        time_data = [curve.time_markers()[0] for curve in curves]
        self.save_file(time_data, wr_data, rd_data)

    def get_format_name(self):
        """Get the human readable format name"""
        return 'Text file with curves as rows'
