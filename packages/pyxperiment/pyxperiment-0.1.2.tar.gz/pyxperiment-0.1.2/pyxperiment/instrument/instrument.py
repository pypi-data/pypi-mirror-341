"""
    pyxperiment/controller/instrument.py:
    The base class for all test and measure instruments

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

from threading import RLock
from typing import Sequence, TypeVar
from abc import ABCMeta, abstractmethod
from pyxperiment.core.utils import classandinstancemethod
from .instrument_control import (
    TimeoutControl, ValueControl, InstrumentControl, ActionControl, RampControl, SweepControl
)

class Instrument(metaclass=ABCMeta):
    """
    This class defines any instruments, controllable with the application

    :param name: A user-friendly unique instrument name
    """

    def __init__(self, name: str) -> None:
        """
        When the device instance is created all the properties must be bound
        to this device instance
        """
        self.name = name
        # Lock for access management
        self._lock = RLock()
        # List of all controls for configuration dialog TODO: find a way to remove
        self._options = None

        for attr in filter(lambda x: not x.startswith("_"), dir(self.__class__)):
            prop = getattr(self.__class__, attr)
            # Controls that are contained directly in the class
            if isinstance(prop, InstrumentControl):
                setattr(self, attr, prop.with_instance(self))
            # Lists of controls
            if isinstance(prop, list) and all(isinstance(el, InstrumentControl) for el in prop):
                setattr(self, attr, list(el.with_instance(self) for el in prop))

    @property
    @abstractmethod
    def location(self) -> str:
        """
        Get the instrument location string
        """

    @staticmethod
    @abstractmethod
    def driver_name() -> str:
        """
        Get the controlled instrument class name string
        """

    @abstractmethod
    def device_name(self) -> str:
        """
        Get the instrument model
        """

    def device_id(self) -> str:
        """
        Get the unique serial number, assigned by the manufacturer
        """
        return 'Unknown'

    def reset(self) -> None:
        """
        Reset the internal connection
        """

    def to_remote(self) -> None:
        """
        Make preparations as an experiment is starting
        """

    def to_local(self) -> None:
        """
        Enable local controls after experiment is over
        """

    def get_options(self) -> Sequence[InstrumentControl]:
        """
        Return the controls list for the configuration window
        """
        if self._options is None:
            return list(filter(
                lambda x: not isinstance(x, RampControl), self.get_controls(InstrumentControl)
                ))
        return self._options

    def set_options(self, options_list: Sequence[InstrumentControl]):
        """
        Set the controls list for the configuration window
        """
        self._options = options_list

    CT = TypeVar('CT', bound=type[object])
    @classandinstancemethod
    def get_controls(cls, control_type: CT) -> list[CT]:
        """
        Return all controls for this instrument
        """
        controls = [
            prop
            for prop in [getattr(cls, attr) for attr in dir(cls) if not attr.startswith("_")]
            if isinstance(prop, control_type)
            ]
        for prop_list in [getattr(cls, attr) for attr in dir(cls) if not attr.startswith("_")]:
            if isinstance(prop_list, list) and prop_list:
                controls.extend([
                    prop for prop in prop_list if isinstance(prop, control_type)
                ])
        return controls

    @classandinstancemethod
    def get_readable_controls(cls) -> list[ValueControl]:
        """
        Get all the readable controls (can not be set) for this class
        """
        return list(
            filter(lambda x: x.is_sweepable() and x.is_readable(),
                   cls.get_controls(ValueControl))
                   )

    @classandinstancemethod
    def get_writable_controls(cls) -> list[ValueControl]:
        """
        Get all the writable controls for this class
        """
        return list(
            filter(lambda x: x.is_sweepable() and x.is_writable(),
                   cls.get_controls(ValueControl))
                   )

    @classandinstancemethod
    def is_readable(cls) -> bool:
        """
        Check if this instrument has any controls that can be read
        """
        return bool(cls.get_readable_controls())

    @classandinstancemethod
    def is_writable(cls) -> bool:
        """
        Check if this instrument has any controls that can be written
        """
        return bool(cls.get_writable_controls())

    def description(self) -> list[tuple[str,str]]:
        """
        Return the description, containing the current status of the device.
        """
        controls = filter(
            lambda x: not isinstance(x, (ActionControl, TimeoutControl, RampControl, SweepControl)),
            self.get_options()
            )
        ret = [(control.name, str(control.get_value())) for control in controls]
        ret.insert(0, ('Address', self.location))
        ret.insert(0, ('Name', self.device_name()))
        return ret
