"""
    pyxperiment/devices/agilent/agilent344xx.py: Support for Keysight344xx

    This file is part of the PyXperiment project.

    Copyright (c) 2022 PyXperiment Developers

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

from decimal import Decimal

from pyxperiment.instrument import (
    VisaInstrument, ListControl, ValueControl, BooleanControl, TimeoutControl
)

class Agilent34xxxDMM(VisaInstrument):
    """
    Support for Keysight344xx multimeters.
    Tested with 34401A, 34411A and 34461A.
    To archieve best performance we turn off the display while measuring
    """

    MODEL_34401A = '34401A'
    MODEL_34411A = '34411A'
    MODEL_34461A = '34461A'
    MODEL_34465A = '34465A'
    MODEL_34470A = '34470A'

    def __init__(self, rm, resource):
        super().__init__(rm, resource)
        self.write('*CLS')
        self.idn = self.query_id().translate({ord(c): None for c in ['\r', '\n']}).split(',')
        self.model = self.idn[1]
        self.set_options([
            self.autorange,
            self.measurement_range,
            self.resolution,
            self.nplc,
            self.autozero,
            self.highz,
            self.aperture_on,
            self.aperture,
            self.display_state,
            self.sample_count,
            self.trigger_delay_auto,
            self.trigger_delay,
            self.value,
            TimeoutControl(self.value)
        ])

    @staticmethod
    def driver_name():
        return 'HP/Agilent/Keysight 34xxx DMM'

    def device_name(self):
        return self.idn[0].title() + ' ' + self.idn[1] + ' DMM'

    def device_id(self):
        return self.idn[2] if self.idn[2] != '0' else 'Unknown'

    function = ListControl(
        'Function', dict(zip(['Voltage', 'Current'], ['volt', 'curr'])),
        get_func=lambda instr: instr.query('func?'),
        set_func=lambda instr, val: instr.write('func:' + val + ':dc')
    )

    def set_autorange(self, value: str):
        self.write('sens:volt:dc:rang:auto ' + value)

    def get_autorange(self) -> str:
        return self.query('volt:dc:rang:auto?')

    autorange = BooleanControl(
        'Auto Range',
        get_autorange,
        set_autorange
    )

    range_values = [
        '1000', '100', '10', '1', '0.1'
        ]

    def _set_range(self, value):
        if value in self.range_values:
            self.write('volt:rang ' + value)
        else:
            raise ValueError('Invalid range.')

    def _get_range(self):
        value = self.query('volt:rang?')
        for range_value in self.range_values:
            if Decimal(range_value) == Decimal(value):
                return range_value
        raise ValueError('Unkwown range ' + value)

    measurement_range = ListControl(
        'Range, V',
        range_values,
        get_func=_get_range,
        set_func=_set_range,
        enabled=lambda instr: not instr.autorange.get_value(),
    )

    nplc_values = [
        '0.02', '0.2', '1', '10', '100'
        ]

    def _set_nplc(self, value):
        if value in self.nplc_values:
            self.write('volt:nplc ' + value)
        else:
            raise ValueError('Invalid NPLC.')

    def _get_nplc(self):
        value = self.query('volt:nplc?')
        for nplc_value in self.nplc_values:
            if Decimal(nplc_value) == Decimal(value):
                return nplc_value
        raise ValueError('Unkwown NPLC: ' + value)

    nplc = ListControl(
        'Power cycles',
        nplc_values,
        _get_nplc,
        _set_nplc
    )

    resolution = ValueControl(
        'Resolution', 'V',
        get_func=lambda instr: instr.query('volt:dc:res?'),
        set_func=lambda instr, value: instr.write('volt:dc:res ' + value),
        enabled=lambda instr: not instr.autorange.get_value(),
        sweepable=False
    )

    def get_value(self):
        self.init_get_value()
        return self.end_get_value()

    def init_get_value(self):
        self.write('read?')

    def end_get_value(self):
        value = self.read().translate({ord(c): None for c in ['\r', '\n']})
        return value.split(',') if (',' in value) else value

    value = ValueControl(
        'Value', 'V',
        get_func=lambda instr: instr.get_value(),
        channels=lambda instr: int(instr.sample_count.get_value())
    )

    def _set_autozero(self, value):
        cmd = 'sens:volt:dc:zero:auto ' if self.model != '34401A' else 'zero:auto '
        self.write(cmd + value)

    def _get_autozero(self):
        cmd = 'sens:volt:dc:zero:auto?' if self.model != '34401A' else 'zero:auto?'
        return self.query(cmd)

    autozero = BooleanControl(
        'Auto Zero',
        _get_autozero,
        _set_autozero
    )

    def _can_use_aperture(self):
        return self.model in (
            Agilent34xxxDMM.MODEL_34411A, Agilent34xxxDMM.MODEL_34465A, Agilent34xxxDMM.MODEL_34470A
            )

    def _get_apertureon(self):
        if not self._can_use_aperture():
            return '0'
        return self.query('volt:aper:enab?')

    aperture_on = BooleanControl(
        'Aperture on',
        get_func=_get_apertureon,
        set_func=lambda instr, value: instr.write('volt:aper:enab ' + value),
        enabled=_can_use_aperture
    )

    aperture = ValueControl(
        'Aperture', 's',
        get_func=lambda instr: instr.query('volt:aper?'),
        set_func=lambda instr, value: instr.write('volt:aper ' + str(value)),
        enabled=lambda instr: instr.aperture_on.get_value(),
        sweepable=False
    )

    def _set_highz(self, value):
        cmd = 'volt:dc:imp:auto ' if self.model != '34401A' else 'inp:imp:auto '
        self.write(cmd + value)

    def _get_highz(self):
        return self.query('volt:dc:imp:auto?' if self.model != '34401A' else 'inp:imp:auto?')

    highz = BooleanControl(
        'Auto Impedance',
        get_func=_get_highz,
        set_func=_set_highz
    )

    sample_count = ValueControl(
        'Sample count', None,
        get_func=lambda instr: instr.query('SAMP:COUN?'),
        set_func=lambda instr, value: instr.write('SAMP:COUN ' + str(value)),
        sweepable=False
    )

    """
    The delay between trigger event and acquisition
    """
    trigger_delay = ValueControl(
        'Trigger delay', 's',
        get_func=lambda instr: instr.query('TRIG:DEL?'),
        set_func=lambda instr, value: instr.write('TRIG:DEL ' + str(value)),
        enabled=lambda instr: not instr.trigger_delay_auto.get_value(),
        sweepable=False
    )

    trigger_delay_auto = BooleanControl(
        'Auto trigger delay',
        get_func=lambda instr: instr.query('TRIG:DEL:AUTO?'),
        set_func=lambda instr, value: instr.write('TRIG:DEL:AUTO ' + value),
    )

    def _set_display_state(self, value):
        if self._can_turn_off_display():
            self.write('disp ' + value)
            self.write('disp:text' + (' "Measurement in progress..."' if value == '0' else ':cle'))

    def _get_display_state(self):
        if not self._can_turn_off_display():
            return '1'
        return self.query('disp?')

    def _can_turn_off_display(self):
        return (self.model == Agilent34xxxDMM.MODEL_34461A or
                self.model == Agilent34xxxDMM.MODEL_34465A or
                self.model == Agilent34xxxDMM.MODEL_34470A)

    display_state = BooleanControl(
        'Display on',
        get_func=_get_display_state,
        set_func=_set_display_state,
        enabled=_can_turn_off_display
    )

    def to_remote(self):
        self.display_state.set_value(False)

    def to_local(self):
        """
        Enable local controls after sweep is over
        """
        if self.model != Agilent34xxxDMM.MODEL_34461A:
            self.gpib_to_local()
        else:
            self.write('SYST:LOC')
