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

from pymeasure.instruments.mcc.daq_module_base import DAQModule
import logging

# =============================================================================
# Logging
# =============================================================================

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


# =============================================================================
# Instrument file
# =============================================================================


class SuperLogics8017(DAQModule):
    """Represents the Superlogics 8017 8-channel analog input module. Class
    assumes that a MCC, CBCOM, or SuperLogics RS232 to RS485 adapter board
    (e.g., MCC CB-7520 or Superlogics 8520) is used to communicate with the DAQ
    board.

    Class inherits commands from the DAQModule parent class.

    .. code-block:: python

    visa_adapter = VISAAdapter("COM5",
                              asrl={"baud_rate": 9600,
                              "timeout": 500,
                              "read_termination": "\r",
                              "write_termination": "\r"})
    sl8017 = DAQModule(visa_adapter, address=1)
    print(sl8017.measure_all_channels())            # Measure all input channels
    print(sl8017.measure_channel(2)                 # Measure Channel 2
    """

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Initializer
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, adapter, name="Superlogics 8017 DAQ module",
                 address=1, **kwargs):
        super().__init__(
            adapter,
            name,
            **kwargs
        )
        # Need to convert address to string that represents hex number. Uses
        # inherited method from DAQModule.
        self.address = self.convert_address_to_hex_string(address)
