"""
    pyxperiment/data_format/text_data_format.py:
    Implements the data stroraging into plain text files

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

import os
import re
import datetime
import itertools

from pyxperiment.instrument.instrument_control import SweepControl
from pyxperiment.data_storage import DataStorage

class TextDataWriter():
    """
    A class for formatted data output into text files
    """

    def __init__(self, name_exp: str) -> None:
        self.name_exp = name_exp
        self.dirname = os.path.dirname(name_exp)
        self.base_name = os.path.basename(name_exp)
        self.regexp = self.base_name.replace('*', '([0-9]+)').replace('.', r'\.')
        if not os.path.exists(self.dirname):
            os.makedirs(self.dirname)
        self.update_filename()

    @staticmethod
    def get_format_name() -> str:
        """
        Get the human readable format name
        """
        return 'Text file for each curve'

    def update_filename(self) -> None:
        """
        Recheck next avialiable file number
        """
        max_file_num = 0
        for file in os.listdir(self.dirname):
            match = re.match(self.regexp, file)
            if match is not None:
                max_file_num = max(max_file_num, int(match.group(1)))
        self.file_num = max_file_num + 1

    def get_filename(self) -> str:
        """Get the current filename"""
        return os.path.join(self.dirname, self.base_name.replace('*', str(self.file_num)))

    def print_device_info(self, info, file) -> None:
        """
        Saves experiment info for a single device
        """
        device_name = next(filter(lambda x: x[0] == 'Name', info))
        print('Device: ' + device_name[1], end='\n', file=file)
        for field in filter(lambda x: x[0] != 'Name', info):
            print('\t' + field[0] + ': ' + field[1], end='\n', file=file)

    def save_info_file(self, yinfo, xinfo, sweep_info) -> None:
        """
        Saves experiment info file
        """
        file_name = self.get_filename().replace('.dat', '.info')
        with open(file_name, "w", encoding='utf-8') as text_file:
            print('Y devices: ', end='\n', file=text_file)
            for device_info in yinfo:
                self.print_device_info(device_info, text_file)
            print('X devices: ', end='\n', file=text_file)
            for device_info in xinfo:
                self.print_device_info(device_info, text_file)
            for field in sweep_info:
                print(field[0] + ': ' + str(field[1]), end='\n', file=text_file)

    def save_sweep(self, index: int, channel: int, num_channels: int, data):
        """
        Saves a sweep device data in a separate file
        """
        file_name = self.get_filename().replace(
            '.dat', '_' + str(index) + '_' + str(channel) + '.dat'
            )
        with open(file_name, "w", encoding='utf-8') as text_file:
            # Check if all the x lines are the same
            same_x = all(sample[0] == data[0][0] for sample in data)
            # Only need to save x line once
            if same_x:
                print(*data[0][0], file=text_file)
            # Need to save each x line
            for data_sample in data:
                if not same_x:
                    print(*data_sample[0], file=text_file)
                if num_channels == 1:
                    print(*data_sample[1], file=text_file)
                else:
                    print(*data_sample[1][channel], file=text_file)

    def after_sweep(self, num: int, data_storage: DataStorage):
        """This method shall be called after each sweep"""
        if num == 0:
            self.save_internal(data_storage)
            self.update_filename()

    def save_internal(self, data_storage: DataStorage):
        """
        Save the measured data to file
        """
        # Save the main file
        sweep = data_storage.get_curve(-1)
        timecol = sweep.time_markers()
        # Get indexes of the normal controls
        rd_ind =  [
            index for index, element in enumerate(data_storage.get_measurables())
            if not isinstance(element.get_control(), SweepControl)
            ]
        input_data = list(sweep.read_data()[i] for i in rd_ind)
        # Save all the regular controls
        with open(self.get_filename(), "w", encoding='utf-8') as text_file:
            for i, xval in enumerate(sweep.write_data()):
                # Print the time column
                if i >= len(timecol):
                    print('NaN', end=' ', file=text_file)
                elif isinstance(timecol[i], datetime.datetime):
                    print(datetime.datetime.isoformat(timecol[i]), end=' ', file=text_file)
                else:
                    print(str(int(timecol[i]*1000)), end=' ', file=text_file)
                # Print x column
                print(str(xval), end=' ', file=text_file)
                # Print y columns
                if i >= len(timecol):
                    data_line = [
                        'NaN' for i in range(sum(elem.num_channels() for elem in data_storage.get_measurables()))
                        ]
                else:
                    data_line = [
                        (elem[i] if isinstance(elem[i], list) else [elem[i]]) for elem in input_data
                        ]
                    data_line = itertools.chain(*data_line)
                print(*data_line, sep=' ', file=text_file)
        # Get indexes of the sweep controls
        rd_ind =  [
            index for index, element in enumerate(data_storage.get_measurables())
            if isinstance(element.get_control(), SweepControl)
            ]
        # Save all the sweep controls
        for ind,data in zip(rd_ind, (sweep.read_data()[i] for i in rd_ind)):
            num_channels = data_storage.get_measurables()[ind].num_channels()
            for channel in range(num_channels):
                self.save_sweep(ind, channel, num_channels, data)
