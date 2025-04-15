"""
    pyxperiment/controller/device_factory.py:
    The factory class is used to construst devices

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

import inspect
import pkgutil
import importlib
from os.path import dirname
from typing import Type, Sequence, TypeVar, cast
import types

import logging
import pyvisa
import pyvisa.constants

import pyxperiment.devices
from .instrument import Instrument
from .instrument_module import InstrumentModule
from .visa_instrument import VisaInstrument
from .tcp_instrument import TcpSocketInstrument
from .zurich_instrument import ZurichInstrument

class InstrumentFactory():
    """
    The factory class detect all suitable instrument control modules and
    creates specific devices from their connection strings and class names
    """

    def __init__(self, visa_name: str) -> None:
        self._rm = pyvisa.ResourceManager(visa_name)
        self._device_list = []# type: list[Instrument]
        self._drivers_list = self.__find_drivers(self.__load_modules(pyxperiment.devices))

    @staticmethod
    def __load_modules(folder) -> list[types.ModuleType]:
        all_files = list(pkgutil.walk_packages([dirname(folder.__file__)]))
        modules = [
            importlib.import_module(folder.__name__ + '.' + f.name)
            for f in all_files if not f.ispkg
            ]
        dir_names = filter(lambda x: x.ispkg, all_files)
        for name in dir_names:
            modules = modules + InstrumentFactory.__load_modules(
                importlib.import_module(folder.__name__ + '.' + name.name)
                )
        return modules

    @staticmethod
    def __find_drivers(modules: list[types.ModuleType]) -> list[Type[Instrument]]:
        result = []
        for module in modules:
            for _, obj in inspect.getmembers(module):
                if (
                        inspect.isclass(obj) and issubclass(obj, Instrument) and
                        obj != Instrument and obj != VisaInstrument and
                        obj != ZurichInstrument and
                        obj != TcpSocketInstrument and obj != InstrumentModule
                    ):
                    result.append(obj)
                    if not (obj.is_readable() or obj.is_writable()):
                        logging.warning('%s has no readable or writable controls.', obj)
        return result

    CT = TypeVar('CT', bound=Instrument)
    def open_instrument(self, devcls: type[CT], resource: str) -> CT:
        """
        Opens an instrument based on the locator string
        """
        # TODO: more genereal way
        if devcls.driver_name() == 'Leonardo 2 Digitizer board' or devcls.driver_name() == 'ZTEC ZT410 Oscilloscope/Digitizer':
            devices = list(filter(
                lambda x: isinstance(x, devcls), self._device_list
                ))
        else:
            devices = list(filter(
                lambda x: isinstance(x, devcls) and x.location.lower() == resource.lower(),
                self._device_list
                ))
        if not devices:
            ret = devcls(self._rm, resource)# type: ignore
            self._device_list.append(ret)
            return ret
        return cast(devcls, devices[0])

    def list_drivers(self) -> list[type[Instrument]]:
        """
        List all instrument drivers present. Returns a list of classes.
        """
        return self._drivers_list

    def list_resources(self) -> Sequence[str]:
        """
        List all resources present. Returns a Sequence of VISA strings.
        """
        # Do the discovery
        resources = self._rm.list_resources()
        # Send the GPIB instruments to local
        for res in resources:
            if res.startswith('GPIB'):
                try:
                    dev = cast(pyvisa.resources.GPIBInstrument, self._rm.open_resource(res))
                    dev.control_ren(pyvisa.constants.RENLineOperation.address_gtl)
                    dev.close()
                except pyvisa.VisaIOError:
                    pass
        return resources
