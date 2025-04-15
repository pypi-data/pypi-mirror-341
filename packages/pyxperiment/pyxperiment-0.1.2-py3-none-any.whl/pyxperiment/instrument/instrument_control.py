"""
    pyxperiment/controller/instrument_controls.py:
    The base classes for controls - device specific data entities

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

from __future__ import annotations
from abc import ABCMeta, abstractmethod
from copy import copy
from typing import TYPE_CHECKING, Callable, Optional, Union, Tuple, Sequence, Iterable, Any, cast

from pyxperiment.core.utils import bidict

from .validation import Validator, EmptyValidator, DynamicRangeValidator
if TYPE_CHECKING:
    from .instrument import Instrument

class InstrumentControl(metaclass=ABCMeta):
    """
    Instrument control represents a knob or a gauge of an instrument, that controls
    a certain parameter. Controls can range from simple flip switch to a parameter sweep.
    """

    def __init__(
        self, name: str,
        get_func: Union[Callable[[Instrument],Any], Callable[[],Any], None]=None,
        set_func: Union[Callable[[Instrument,Any],None], Callable[[Any],None], None]=None,
        enabled: Optional[Callable[[Instrument],bool]]=None
        ) -> None:
        self._name = name
        self._fget = cast(Callable[[],Any], get_func)
        self._fset = cast(Callable[[Any],None], set_func)
        self._enabled = enabled
        if TYPE_CHECKING:
            self._instrument = cast(Instrument, None)
        else:
            self._instrument = None

    @property
    def name(self) -> str:
        """
        The name of the control
        """
        return self._name

    def get_instrument(self) -> Instrument:
        """
        Retrieve the instrument this control is part of
        """
        return self._instrument

    @abstractmethod
    def get_value(self) -> Any:
        """
        Retrieve the control value
        """

    @abstractmethod
    def set_value(self, value: Any) -> None:
        """
        Set the control value
        """

    def is_enabled(self) -> bool:
        """
        Is the control modification allowed
        """
        if self._enabled is None:
            return True
        return self._enabled(self._instrument)

    def is_readable(self) -> bool:
        """
        Readable control can be only read
        """
        return self._fset is None

    def is_writable(self) -> bool:
        """
        Writable control can be set
        """
        return self._fset is not None

    def with_instance(self, instrument: Instrument):
        """
        Used to instantiate controls when a specific instrument object is created
        """
        #pylint: disable=W0212
        ret = copy(self)
        ret._instrument = instrument
        if self._fset is not None:
            ret._fset = self._fset.__get__(instrument, instrument.__class__)
        if self._fget is not None:
            ret._fget = self._fget.__get__(instrument, instrument.__class__)
        return ret

    def description(self) -> list[tuple[str,str]]:
        """
        Get the description tuple array
        """
        ret = self._instrument.description()
        ret.append(('Property', self._name))
        return ret

class ListControl(InstrumentControl):
    """
    List control has only a certain set of values, which may also
    have a separate human-readable interpretation.
    """

    def __init__(
            self, name: str,
            values_list: Union[Iterable,dict,bidict],
            get_func=None, set_func=None, enabled=None
            ) -> None:
        super().__init__(name, get_func, set_func, enabled)
        # Convert dict to bidict to have faster backward conversion
        if isinstance(values_list, dict) and not isinstance(values_list, bidict):
            values_list = bidict(values_list)
        self._values_list = values_list

    def values_list(self):
        """
        Return the list of the valid values
        """
        return self._values_list

    def get_value(self):
        """
        Get the value, converted to the readable form
        """
        value = self._fget()
        if isinstance(self._values_list, bidict):
            if not value in self._values_list.inverse:
                raise ValueError('Invalid value for ' + self.name + ': ' + value)
            return self._values_list.inverse[value]
        # No conversion is required
        return value

    def set_value(self, value):
        """
        Set the value, accepts argument in readable form
        """
        if not value in self._values_list:
            raise ValueError('Invalid value for ' + self.name + ': ' + value)
        if isinstance(self._values_list, bidict):
            self._fset(self._values_list[value])
        else:# No conversion is required
            self._fset(value)

    @staticmethod
    def dict_for_list(values: Sequence[str], offset: int = 0) -> dict[str,str]:
        """
        Get the dictionary for ListControl for list of items
        """
        if offset == 0:
            return dict(zip(values,map(str,range(len(values)))))
        return dict(zip(values,map(str,range(offset, len(values)+offset))))

class BooleanControl(InstrumentControl):
    """
    Control, that takes two values:
    true or false, and does data conversion internally
    """

    def __init__(
            self, name: str,
            get_func: Union[
                Callable[[Any],Union[str,int]], Callable[[],Union[str,int]], None
                ]=None,
            set_func: Union[
                Callable[[Any,str],None], Callable[[str],None], None
                ]=None,
            enabled: Optional[Callable[[Any],bool]]=None,
            true_str: str='1', false_str: str='0'
        ):
        super().__init__(name, get_func, set_func, enabled)
        self.true_str = true_str
        self.false_str = false_str

    def get_value(self) -> bool:
        value = self._fget()
        int_value = int(value)
        if int_value == 1:
            return True
        if int_value == 0:
            return False
        raise ValueError('Bad value for ' + self.name + ': "' + str(value) + '"')

    def set_value(self, value: bool) -> None:
        self._fset(self.true_str if value else self.false_str)

class ValueControl(InstrumentControl):
    """
    Control, that repesents a numerical value of physical quantity. Such controls are
    typically used during measurements.
    """

    def __init__(
            self, name: str,
            phys_q: Union[Callable[[Any],Optional[str]], Callable[[],Optional[str]], str, None],
            get_func: Union[
                Callable[[Any],Union[str,list[str]]], Callable[[],Union[str,list[str]]], None
                ]=None,
            set_func: Union[Callable[[Any,Any],None], Callable[[Any],None], None]=None,
            channels: Union[Callable[[Any],int], Callable[[],int], int]=1,
            validator: Validator=EmptyValidator(),
            enabled: Optional[Callable[[Any],bool]]=None,
            sweepable: bool=True
        ):
        """
        Create new value control.

        Parameters
        ----------
        name : str
            The name of this control.

        phys_q : callable or str
            Physical quantity. Can be None.

        get_func : callable
            A function or lambda in the instrument class.
            Should accept no arguments and return a value or list.

        set_func : callable or None

        channels : callable or int
            The vector length for each data point.

        enabled : callable or None
            If the control is currently enabled. None means always enabled.

        sweepable : bool, default True
            Determines if this control can be used for a sweep or only in device menu.
        """
        super().__init__(name, get_func, set_func, enabled)
        self._phys_q = cast(Union[Callable[[],Optional[str]], str, None], phys_q)
        self.validator = validator
        self._channels = cast(Callable[[],int], channels)
        self._sweepable = sweepable
        self.read_timeout = cast(TimeoutControl, None)

    def get_phys_q(self) -> Optional[str]:
        """
        Get the physical quantity, associated with control.

        Returns
        -------
        phys_q : The physical quantity.
        """
        if callable(self._phys_q):
            return self._phys_q()
        return self._phys_q

    def get_value(self):
        """
        Measure and return the value of control.

        Returns
        -------
        value : The measured value.
        """
        return self._fget()

    def set_value(self, value):
        self._fset(value)

    def with_instance(self, instrument):
        #pylint: disable=W0212
        ret = super().with_instance(instrument)
        if callable(self._channels):
            ret._channels = self._channels.__get__(instrument, instrument.__class__)
        if callable(self._phys_q):
            ret._phys_q = self._phys_q.__get__(instrument, instrument.__class__)
        if isinstance(ret.validator, DynamicRangeValidator):
            ret.validator = copy(ret.validator)
            ret.validator.set_instrument(instrument)
        return ret

    def is_sweepable(self) -> bool:
        """
        Get if this device can be controled as a measurement X
        """
        return self._sweepable

    def check_value(self, value):
        """
        Check the ability to set a single value
        """
        return self.validator.check_value(value)

    def check_values(self, values):
        """
        Check the ability to set all the values present in collection
        """
        return self.validator.check_values(values)

    @property
    def channels_num(self) -> int:
        """
        Return the length of the output data vector
        """
        if callable(self._channels):
            return self._channels()
        return self._channels

class RampControl(ValueControl):
    """
    RampControl works as an ordinary ValueControl, but often takes long time to ramp to the set
    point. Notable examples include magnetic field and temperature. RampControl has its own internal
    sweep generator. The state of this generator can be checked by calling is_finished method. It
    always has both get and set methods and only one channel.
    """

    def __init__(
            self, name: str,
            phys_q: Union[Callable[[Any],Optional[str]], Callable[[],Optional[str]], str, None],
            get_actual_value: Union[Callable[[Any],str], Callable[[],str]],
            set_target_value: Union[Callable[[Any,Any],None], Callable[[Any],None]],
            get_target_value: Union[Callable[[Any],str], Callable[[],str]],
            stop_ramp: Union[Callable[[Any],None], Callable[[],None]],
            is_finished: Union[Callable[[Any],bool], Callable[[],bool]],
            validator: Validator=EmptyValidator(),
            enabled: Optional[Callable[[Any],bool]]=None,
            sweepable: bool=True
        ):
        """
        Create a new RampControl

        Parameters
        ----------
        name : str
            The name of this control.

        phys_q : callable or str
            Physical quantity. Can be None.

        get_func : callable
            A function or lambda in the instrument class.
            Should accept no arguments and return a value or list.

        set_func : callable or None

        enabled : callable or None
            If the control is currently enabled. None means always enabled.
        """
        super().__init__(
            name, phys_q, get_actual_value, set_target_value, 1, validator, enabled, sweepable
            )
        self._is_finished = cast(Callable[[],bool], is_finished)
        self._get_target_value = cast(Callable[[],str], get_target_value)
        self._stop_ramp = cast(Callable[[],None], stop_ramp)

    def with_instance(self, instrument):
        #pylint: disable=W0212
        ret = super().with_instance(instrument)
        ret._is_finished = self._is_finished.__get__(instrument, instrument.__class__)
        ret._get_target_value = self._get_target_value.__get__(instrument, instrument.__class__)
        self._stop_ramp = self._stop_ramp.__get__(instrument, instrument.__class__)
        return ret

    def is_finished(self) -> bool:
        """
        Return whether the control has reached its target value.
        """
        return self._is_finished()

    def get_target_value(self) -> str:
        """
        Get the actual target value.
        """
        return self._get_target_value()

    def stop_ramp(self) -> None:
        """
        Stop the ongoing ramp.
        """
        self._stop_ramp()

class SweepControl(ValueControl):
    """
    Sweep control represent an internal capability of making a sweep measurement of one parameter
    versus the other. Each acquisition results in a dataset.
    """

    def __init__(
            self, name: str,
            axes_names: Tuple[str,str],
            phys_q: Tuple[str,str],
            get_func,
            channels: Union[Callable[[Any],int], Callable[[],int], int]=1,
            enabled: Optional[Callable[[Any],bool]]=None
            ) -> None:
        """
        Create a new sweep control.

        Parameters
        ----------
        name : str
            The name of this control.

        axes_names: Tuple (str, str)
            Names for the parameters

        phys_q : Tuple (str, str)
            Physical quantity (Tuple of strings for x and y). Any can be None.

        get_func : callable
            A function or lambda in the instrument class.
            Should accept no arguments and return a list.

        channels : callable or int
            The vector length for each data point.

        enabled : callable or None
            If the control is currently enabled. None means always enabled.
        """
        super().__init__(name, phys_q, get_func, None, channels, enabled=enabled)# type:ignore
        self._axes_names = axes_names

    def get_axes_names(self):
        return self._axes_names

class StateControl(InstrumentControl):
    """
    Instrument control, that can only be read, and represents
    a status string
    """

    def __init__(self, name, get_func, enabled=None) -> None:
        super().__init__(name, get_func, None, enabled)

    def get_value(self):
        return self._fget()

    def set_value(self, value) -> None:
        del value
        raise NotImplementedError('set_value is not valid for StateControl')

class ActionControl(InstrumentControl):
    """
    Instrument control, that can only be set (activated), and
    represents a certain action/state transition
    """

    def __init__(self, name, set_func, enabled=None):
        super().__init__(name, None, set_func, enabled)

    def get_value(self):
        raise NotImplementedError('get_value not valid for ActionControl')

    def set_value(self, value=None):
        self._fset()# type: ignore # TODO: make action control use an argument

class MultiControl(InstrumentControl):
    """
    MultiControl combines several controls that have their values retrieved simultaneaously.
    """

    def __init__(
            self,
            controls: Iterable[InstrumentControl],
            get_func: Union[
                Callable[[Any],Iterable[Any]], Callable[[],Iterable[Any]], None
                ]=None,
            set_func: Union[
                Callable[...,None], Callable[...,None], None
                ]=None,
            enabled: Optional[Callable[[Any],bool]]=None
        ):
        super().__init__('', get_func, set_func, enabled)
        self.controls = controls
        self.temp_values = []
        for ind, control in enumerate(self.controls):
            control._fget = lambda s=self,i=ind: s.temp_values[i]
            control._fset = lambda val,i=ind,s=self: s._set_control_value(val, i)

    def _set_control_value(self, val, ind):
        self.temp_values[ind] = val

    def get_value(self) -> Sequence[Any]:
        self.temp_values = self._fget()
        return [control.get_value() for control in self.controls]

    def set_value(self, value: Sequence[Any]) -> None:
        self.temp_values = list(value)
        for val, control in zip(value, self.controls):
            control.set_value(val)
        self._fset(*self.temp_values)

class TimeoutControl(ValueControl):
    """
    A special control, representing a timeout for another control
    """

    def __init__(self, control: ValueControl):
        super().__init__(
            'Timeout', 'ms', None, None, sweepable=False
        )
        # Value is set externally by ControlField
        self.value = cast(float, None)
        self.control = control
        control.read_timeout = self

    def get_value(self):
        if not self.value:
            return ''
        return str(round((self.value)*1000, 2))
