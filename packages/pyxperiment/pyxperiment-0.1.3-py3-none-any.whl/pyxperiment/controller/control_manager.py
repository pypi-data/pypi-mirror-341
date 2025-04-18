"""
    pyxperiment/controller/control_manager.py:
    The control classes implementing data acquisition and storage from
    different controls

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
import traceback
import logging
from typing import Generic, TypeVar

from pyxperiment.core.utils import str_to_range
from pyxperiment.instrument import (
    Instrument, ValueControl, RampControl
)

ControlType = TypeVar('ControlType', bound=ValueControl)
class ControlManager(Generic[ControlType], metaclass=ABCMeta):
    """
    Control manager performs automated operations on an instrument control.
    """

    def __init__(self, control: ControlType):
        self._control = control
        self._index = 0
        self._values = []
        self.curr_value = None

    @property
    def value(self):
        """
        Retrieve the last control value
        """
        return self.curr_value

    @property
    def index(self) -> int:
        """
        Get the number of performed operations
        """
        return self._index

    @property
    def values(self):
        """
        Retrieve the full list of control values
        """
        return self._values

    def reset(self) -> None:
        """
        Reset this manager to the initial state
        """

    @abstractmethod
    def update(self) -> None:
        """
        Perform the operation on the control
        """

    def get_control(self) -> ControlType:
        """
        Return the control, being managed
        """
        return self._control

    def get_instrument(self) -> Instrument:
        """
        Return the instrument, the managed control refers to
        """
        return self._control.get_instrument()

    def description(self):
        """
        Get a human readable representation of this management operation
        """
        return self._control.description()

class ScanManager(ControlManager[ValueControl]):
    """
    Manages a scan (motion through a set of fixed values) for an instrument control.
    """

    def __init__(self, control: ValueControl, values, delay):
        super().__init__(control)
        self.range_str = values
        if isinstance(values, str):
            self._values = str_to_range(values)
        else:
            self._values = values
        # Check that the control can actually set all the values
        if not self._control.check_values(self._values):
            raise Exception(
                'The values list contains points, that can not be accepted by the control.'
                )
        self.delay = delay
        self.curr_value = self._control.get_value()
        self._current = 0

    def reset(self):
        self._current = 0
        self._index = 0
        self._control.set_value(self._values[self._current])

    def revert(self):
        """
        Flip the scan to do it in reverse direction
        """
        self._values = self._values[::-1]# do not modify the original list
        self.reset()

    def forward(self):
        """
        Proceed to next value
        """
        self._index += 1
        if self._current+1 < len(self._values):
            self._current += 1
            self._control.set_value(self._values[self._current])
            return True
        return False

    def backward(self):
        """
        Return to the previous value
        """
        if self._current-1 >= 0:
            self._current -= 1
            self._control.set_value(self._values[self._current])
            return True
        return False

    def update(self):
        self.curr_value = self._control.get_value()

    def is_point_set(self):
        """
        Check if the control has finished setting the point
        """
        if isinstance(self._control, RampControl):
            # The control state has to be checked
            return self._control.is_finished()
        return True

    def description(self):
        ret = super().description()
        ret.append(('Range', str(self.range_str)))
        ret.append(('Number of points', str(len(self.values))))
        ret.append(('Delay', str(self.delay)))
        return ret

class RampManager(ControlManager[RampControl]):
    """
    RampManager is used to peform measurement on a control that can only be affected
    indirectly. A typical example of such is a temperature reading or magnetic field sweep.
    In this case, a condition can be set for measurement termination. Bidirectional measurements
    are possible.
    """

    def __init__(self, control: RampControl, start_value, target_value, delay):
        super().__init__(control)
        self.start_value = start_value
        self.target_value = target_value
        self._values = [start_value, target_value]
        self.delay = delay
        self.curr_value = self._control.get_value()
        self._current = 0

    def reset(self):
        self._current = 0
        self._index = 0
        self._values = [self.target_value]

    def revert(self):
        """
        Flip the observation to do it until start_value is reached
        """
        self.start_value, self.target_value = self.target_value, self.start_value
        self.reset()

    def forward(self):
        """
        Proceed to the target_value
        """
        self._index += 1
        if self._current == 0:
            self._current += 1
            self._control.set_value(self.target_value)
            return True
        if self._current == 2:
            return False
        if self._control.is_finished():
            self._current = 2
        return True

    def backward(self):
        """
        Proceed to the start_value
        """
        if self._current == 2:
            self.curr_value = self._control.get_value()
            self._control.set_value(self.start_value)
            self._current = 0
            return True
        if self._control.is_finished():
            return False
        self.curr_value = self._control.get_value()
        return True

    def update(self):
        self.curr_value = self._control.get_value()
        self._values.insert(len(self._values)-1, self.curr_value)

    def is_point_set(self):
        """
        Check if the target is reached.
        """
        return self._control.is_finished()

    def stop_ramp(self):
        """
        Stop current ramp.
        """
        self._control.stop_ramp()

    def description(self):
        ret = super().description()
        ret.append(('Start', str(self.start_value)))
        ret.append(('Target', str(self.target_value)))
        ret.append(('Delay', str(self.delay)))
        return ret

class ReadableManager(ControlManager):
    """
    Used to manage reading of a control value.
    """

    def __init__(self, control : ValueControl):
        super().__init__(control)
        self.reset()
        self.curr_value = ''
        self._channels_num = self._control.channels_num

    def reset(self):
        self._values = []
        self._channels_num = self._control.channels_num

    def update(self) -> None:
        try:
            self._values.append(self._control.get_value())
        except Exception as ex:
            logging.exception("Error while reading the control: %s", ex)
            traceback.print_exc()
            self.get_instrument().reset()
            self._values.append(self._control.get_value())
        self.curr_value = self._values[-1]

    def num_channels(self) -> int:
        """
        Return the number of values, each read of this control results in. This is
        expected to remain constant during the experiment.
        """
        return self._channels_num

class AsyncReadableManager(ReadableManager):
    """
    Manages asyncronous read operations on control, i.e the ones that block the interface when
    waiting for the result.
    """

    def init_update(self):
        """
        init_update is called to initiate the control acquisition, without blocking
        """
        try:
            self._control.init_get_value()
        except Exception as ex:
            logging.exception("Error while initing reading of control: %s", ex)
            traceback.print_exc()
            self.get_instrument().reset()
            self._control.init_get_value()

    def update(self):
        """
        update blocks until the actual data is acquired
        """
        try:
            self._values.append(self._control.end_get_value())
        except Exception as ex:
            logging.exception("Error while ending reading of control: %s", ex)
            traceback.print_exc()
            self.get_instrument().reset()
            # Have to redo the operation in a blocking manner
            self._values.append(self._control.get_value())
        self.curr_value = self._values[-1]

class DoubleScanManager(ControlManager):
    """
    Manages two scan controls simultaneously
    """

    def __init__(self, device1, device2, values1, values2, delay):
        super().__init__(device1)
        self.range_str = values1 + ',' + values2
        self._values = str_to_range(values1) if isinstance(values1, str) else values1
        self._device_two = device2
        self._values_two = str_to_range(values2) if isinstance(values2, str) else values2
        self.delay = delay
        self.curr_value = self._control.get_value()
        self._current = 0

    def reset(self):
        self._current = 0
        self._index = 0
        self._control.set_value(self._values[self._current])
        self._device_two.set_value(self._values_two[self._current])

    def revert(self):
        """
        Flip the scan to do it in reverse direction
        """
        self._values.reverse()
        self._values_two.reverse()
        self.reset()

    def forward(self):
        """
        Proceed to next value
        """
        self._index += 1
        if self._current+1 < len(self._values):
            self._current += 1
            self._control.set_value(self._values[self._current])
            self._device_two.set_value(self._values_two[self._current])
            return True
        return False

    def backward(self):
        """
        Return to the previous value
        """
        if self._current-1 >= 0:
            self._current -= 1
            self._control.set_value(self._values[self._current])
            self._device_two.set_value(self._values_two[self._current])
            return True
        return False

    def update(self):
        self.curr_value = self._control.get_value()

    def is_point_set(self):
        """
        Check if both controls finished setting the point
        """
        if callable(getattr(self._control, 'finished', None)):
            # The control state has to be checked
            if not self._control.finished():
                return False
        if callable(getattr(self._device_two, 'finished', None)):
            # The control state has to be checked
            if not self._device_two.finished():
                return False
        return True
