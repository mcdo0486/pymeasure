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

# =============================================================================
# Libraries / modules
# =============================================================================

from pymeasure.instruments import Instrument, Channel
import logging

from pymeasure.instruments.validators import strict_discrete_set
from numpy import array, float64
from time import sleep

# =============================================================================
# Logging
# =============================================================================

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

# =============================================================================
# Instrument file
# =============================================================================


class DAQModule(Instrument):
    """This is the base class for the Measurement Computing line of DAQ boards.
    This includes DAQ boards under the branding of MMC, CBCOM, and SignalLogics.
    Do not directly instantiate an object with this class. Use one of the
    DAQ board instrument classes that inherit from this parent class. Untested
    commands are noted in docstrings.

    In addition to the typical input arguments that must be set when
    instantiating a device, you must also include the argument called
    ``address`` that declares the daisy chain address of the DAQ board along
    the serial connection.

    :param address: Daisy chain address number of the DAQ board for the serial
    connection. Valid values are two digit string values between 00 to FF
    (string version of 0 - 255 HEX format).
    """

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Initializer and important communication methods
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, adapter, name="CB7018 DAQ module", address=1, **kwargs):
        super().__init__(
            adapter,
            name,
            asrl={"baud_rate": 9600, "timeout": 500},
            includeSCPI=False,
            **kwargs
        )

        #Convert address from int to str representing a two-digit hex character
        #Validate address is between 0 - 255
        strict_discrete_set(address, range(0,256))
        # Convert to hex
        address_hex = hex(address)
        #Strip leading "0x" of hex string and upper case
        address_split_upper = address_hex[2:].upper()
        #Address needs two digits
        self.address = address_split_upper.zfill(2)

        #self.address = address
        #kwargs.setdefault('timeout', 500)
        #kwargs.setdefault('baudrate', 9600)

    def check_get_errors(self, output):
        """Checks for the invalid command delimiter symbol ``?`` in a
        returned value.
        """

        if len(output):
            if output[0] == "?":
                raise ValueError("Invalid command.")

    def format_output(self, output):
        """Strips the first position of a returned value.

        The first position of a valid returned response has the delimiter ``!``
        or `>``. Method will strip out this delimiter and return the response
        as a floating point number.
        """

        try:
            return float(output[1:])
        except:
            raise ValueError("Invalid command.")

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Methods
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    ## Does not work
    def measure_all_channels(self):
        """Measure signals from all channels.

        :return: Measured signal of all channels.
        """

        output = self.ask("#" + self.address)
        self.check_get_errors(output)
        value = self.format_output(output)
        return value

    def measure_channel(self, channel):
        """Measure signal from a channel.

        Valid ``channel`` values are integers between 0 - 7 (inclusive). Method
        returns the value of the desired channel as a floating point number.

        :param channel: Channel number of DAQ board.
        :type channel: int
        :return: Measured signal of channel.
        :rtype: float
        """

        strict_discrete_set(channel, range(0, 8))
        output = self.ask("#" + self.address + str(channel))
        self.check_get_errors(output)
        value = self.format_output(output)
        return value




    # Not valid command?
    def reset_channel(self, channel):
        return self.ask("@" + self.address + channel)
