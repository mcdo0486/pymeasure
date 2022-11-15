#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2022 PyMeasure Developers
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

from pymeasure.instruments import Instrument
from pymeasure.instruments.fwbell.fwbell5080 import FWBell5080
from pymeasure.instruments.fwbell.fwbell5180_adapter import FWBell5180_Adapter


class FWBell5180(FWBell5080):
    """ Represents the F.W. Bell 5180 Handheld Gaussmeter and provides a high-level interface for
    interacting with the instrument. It is a subclass of FWBell5080.
    FWBell5180_Adapter will find USB port the device is plugged into by vendor and product id.


    .. code-block:: python
        meter = FWBell5180()  # Connects over USB by finding device by vendor and product id

        meter.units = 'gauss'               # Sets the measurement units to Gauss
        meter.range = 1                     # Sets the range to 3 kG
        print(meter.field)                  # Reads and prints a field measurement in G

        fields = meter.fields(100)          # Samples 100 field measurements
        print(fields.mean(), fields.std())  # Prints the mean and standard deviation of the samples
    """

    def __init__(self, adapter=None, **kwargs):
        if adapter is None:
            adapter = FWBell5180_Adapter()
        super().__init__(
            adapter,
            "F.W. Bell 5180 Handheld Gaussmeter",
            **kwargs
        )

    field = Instrument.measurement(
        ":MEASure:FLUX?",
        """ Reads a floating point value of the field in the appropriate units.
        """
    )

    def ask(self, command):
        # Pass ask commands directly to USB adapter
        return self.adapter.ask(command)

    def shutdown(self):
        self.adapter.shutdown()
        super().shutdown()
