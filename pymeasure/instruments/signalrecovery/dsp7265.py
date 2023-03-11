#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2023 PyMeasure Developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import logging
from time import sleep

from pymeasure.instruments import Instrument
from pymeasure.instruments.validators import strict_discrete_range
from .dsp_base import DSPBase

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class DSP7265(DSPBase):

    CURVE_BITS = ['x', 'y', 'magnitude', 'phase', 'sensitivity', 'adc1',
                  'adc2', 'adc3', 'dac1', 'dac2', 'noise', 'ratio', 'log ratio',
                  'event', 'frequency part 1', 'frequency part 2',
                  # Dual modes
                  'x2', 'y2', 'magnitude2', 'phase2', 'sensitivity2']

    def __init__(self, adapter, **kwargs):
        super().__init__(
            adapter,
            name="Signal Recovery DSP 7265",
            **kwargs
        )

    dac3 = Instrument.control(
        "DAC. 3", "DAC. 3 %g",
        """ A floating point property that represents the output
        value on DAC3 in Volts. This property can be set. """,
        validator=lambda value, values: strict_discrete_range(value, values, step=.001),
        values=[-12, 12]
    )
    dac4 = Instrument.control(
        "DAC. 4", "DAC. 4 %g",
        """ A floating point property that represents the output
        value on DAC4 in Volts. This property can be set. """,
        validator=lambda value, values: strict_discrete_range(value, values, step=.001),
        values=[-12, 12]
    )

    @property
    def adc3(self):
        # 50,000 for 1V signal over 1 s
        integral = self.values("ADC 3")[0]
        return integral / (50000.0 * self.adc3_time)

    @property
    def adc3_time(self):
        # Returns time in seconds
        return self.values("ADC3TIME")[0] / 1000.0

    @adc3_time.setter
    def adc3_time(self, value):
        # Takes time in seconds
        self.write("ADC3TIME %g" % int(1000 * value))
        sleep(value * 1.2)
