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

from pymeasure.instruments import Instrument, Channel

from pymeasure.instruments.validators import strict_discrete_set
from numpy import array, float64
from time import sleep


class DAQModule(Instrument):
    """ DAQ Input Module

    :param address: The serial port of the instrument
    """

    def __init__(self, adapter, name="CB7018 DAQ module", address='01', **kwargs):
        self.address = address
        kwargs.setdefault('timeout', 500)
        kwargs.setdefault('baudrate', 9600)
        super().__init__(
            adapter,
            name,
            includeSCPI=False,
            **kwargs
        )

    def check_get_errors(self, output):
        if len(output):
            if output[0] == '?':
                raise ValueError("Invalid command")

    def format_output(self, output):
        try:
            return float(output[1:])
        except:
            raise

    def measure_channel(self, channel):
        output = self.ask("#" + str(self.address) + channel)
        self.check_get_errors(output)
        value = self.format_output(output)
        return value

    def reset_channel(self, channel):
        return self.ask("@" + str(self.address) + channel)
