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

from pymeasure.instruments import Instrument
import logging

from pymeasure.instruments.validators import strict_discrete_set, strict_range

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
    This includes DAQ boards under the branding of MCC, CBCOM, or SuperLogics.
    Class assumes that a MCC, CBCOM, or SuperLogics RS232 to RS485 adapter board
    (e.g., MCC CB-7520 or Superlogics 8520) is used to communicate with the DAQ
    board.

    Do not directly instantiate an object with this class. Use one of the
    DAQ board instrument classes that inherit from this parent class. Untested
    commands are noted in docstrings.

    In addition to the typical input arguments that must be set when
    instantiating a device, you must also include the argument called
    ``address`` that declares the daisy chain address of the DAQ board along
    the serial connection.

    Untested methods are noted in docstrings.

    :param address: Daisy chain address number of the DAQ board for the serial
    connection. Valid values are integers between 0 - 255 (inclusive).
    """

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Initializer and important communication methods
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, adapter, name="CB-7018 DAQ module", address=1,
                 asrl={"baud_rate": 9600,
                       "timeout": 500,
                       "read_termination": "\r",
                       "write_termination": "\r"}, **kwargs):
        super().__init__(
            adapter,
            name,
            asrl=asrl,
            includeSCPI=False,
            **kwargs
        )
        # Need to convert address to string that represents hex number
        self.address = self.convert_address_to_hex_string(address)

    def convert_address_to_hex_string(self, address):
        """Convert address integer argument to a string based on a two-digit
        hex number.

        :param address: Daisy chain address number of the DAQ board for the
        serial connection. Valid values are integers between 0 - 255
        (inclusive).
        :type address: int
        :return: Address as a string that represents a two digit HEX number.
        :rtype: str
        """

        # Verify address is between 0 - 255 (inclusive)
        strict_discrete_set(address, range(0, 256))
        # Convert to hex
        address_hex = hex(address)
        # Strip leading "0x" of hex string and upper case
        address_split_upper = address_hex[2:].upper()
        # address needs two digits
        return address_split_upper.zfill(2)

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
            return output[1:]
            # return float(output[1:])
        except:
            raise ValueError("Invalid command.")

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Methods
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def configure_board(self,
                        new_address,
                        input_type,
                        new_baud_rate="06",
                        new_data_format="00", ):
        """Configure the DAQ board.

        Method configures the DAQ board for use. Only need to run when initially
        setting up a new board or if you need to change a board setting. Boards
        retain configuration after powering down. When configuring a board, only
        connect a single board to the computer / communication module.

        :param new_address: New daisy chain address for DAQ board (NN setting
        in manual). Value must be a two digit string (e.g., "02", "03").
        :type new_address: str
        :param input_type: Analog input type for DAQ board (TT setting in
        manual). See manual or label on board for possible TT settings. Value
        must be a two digit string (e.g., "00", "0E").
        :type input_type: str
        :param new_baud_rate: New communication baud rate (CC setting in
        manual). Value must be a two digit string (e.g., "03", "04"). Default
        value is "06", which represents a 9600 baud rate.
        :type new_baud_rate: str
        :param new_data_format: New data format standard for DAQ board (FF
        setting in manual). Value must be a two digit string (e.g., "00", "01").
        Default value is "00", which enables a 60 Hz filter, disables the
        checksum option, and causes the DAQ board to return measured voltages
        in the "engineering unit format".
        :type new_data_format: str
        :return: New address of DAQ board
        :rtype: str

        Method is UNTESTED.
        """

        output = self.ask("%" + self.address + new_address + input_type
                          + new_baud_rate + new_data_format)
        self.check_get_errors(output)
        value = float(self.format_output(output))
        return value

    def measure_all_channels(self):
        """Measure the input signals from all channels.

        Method returns a string containing the measured signal from all DAQ
        channels. Method assumes that DAQ board data format setting is set to
        "engineering format" or "percent format". Do not use if data format
        setting is set to "HEX format".

        :return: Measured signal of all channels as a list of floating point
        numbers. First entry is Channel 0 and final entry is Channel 7.
        :rtype: list
        """

        output = self.ask("#" + self.address)
        self.check_get_errors(output)
        value_str = self.format_output(output)

        # Returned value is a string of voltages with no delimiter. Values are
        # either in the format of "+XX.XXX" for "engineering format" or
        # "+XXX.XX" for "percent format".

        # First, break up string every 7th digit. Create list of str values.
        list_str = [value_str[i:i + 7] for i in range(0, len(value_str), 7)]
        # Convert every str entry in list to float.
        list_float = [float(list_str[i]) for i in range(0, len(list_str))]
        return list_float

    def measure_channel(self, channel):
        """Measure the input signal from a single channel.

        Valid ``channel`` values are integers between 0 - 7 (inclusive). Method
        returns the value of the desired channel as a floating point number.
        Method assumes that DAQ board data format setting is set to
        "engineering format" or "percent format". Do not use if data format
        setting is set to "HEX format".

        :param channel: Channel number of DAQ board.
        :type channel: int
        :return: Measured signal of channel.
        :rtype: float
        """

        strict_discrete_set(channel, range(0, 8))
        output = self.ask("#" + self.address + str(channel))
        self.check_get_errors(output)
        value = float(self.format_output(output))
        return value

    def perform_span_calibration(self):
        """Perform span calibration on the DAQ board.

        Method returns the DAQ board daisy chain address as a string that
        represents a two digit HEX number.

        :return: DAQ board address as a string that represents a two digit
        HEX number.
        :rtype: str
        """

        output = self.ask("$" + self.address + "0")
        self.check_get_errors(output)
        value = self.format_output(output)
        return value

    def perform_zero_calibration(self):
        """Perform zero calibration on the DAQ board.

        Method returns the DAQ board daisy chain address as a string that
        represents a two digit HEX number.

        :return: DAQ board address as a string that represents a two digit
        HEX number.
        :rtype: str
        """

        output = self.ask("$" + self.address + "1")
        self.check_get_errors(output)
        value = self.format_output(output)
        return value

    def read_configuration(self):
        """Read the configuration of the DAQ board.

        Method returns the DAQ board configuration as a string in the format
        "AATTCCFF" where "AA" is the board address represented as a two digit
        HEX number, "TT" is the analog input type code number, "CC" is the baud
        rate setting code number, and "FF" is the data format setting code
        number.

        :return: DAQ board configuration
        :rtype: str
        """

        output = self.ask("$" + self.address + "2")
        self.check_get_errors(output)
        value = self.format_output(output)
        return value

    def read_cjc_temp(self):
        """Read the cold junction compensation (CJC) temperature.

        Method returns the cold junction compensation (CJC) temperature as a
        floating point number in Celsius.

        :return: CJC temperature
        :rtype: float
        """

        output = self.ask("$" + self.address + "3")
        self.check_get_errors(output)
        value = float(self.format_output(output))
        return value

    def set_cjc_offset(self, offset):
        """Set the cold junction compensation (CJC) temperature offset.

        Method returns the cold junction compensation (CJC) temperature as a
        floating point number in Celsius.
        :param offset: Offset temperature (float)
        :return: CJC temperature
        :rtype: float
        """
        # Validate the offset
        offset = strict_range(offset, [-40.96, 40.96])
        offset = round(offset * 100)
        float_hex = '{:+05X}'.format(offset)
        output = self.ask("$" + self.address + "9" + float_hex)
        self.check_get_errors(output)

    def read_channel_status(self):
        """Read what channels are enabled or disabled.

        Method returns an ordered boolean list of ``True`` and ``False`` values
        representing if a data channel is enabled. First entry is Channel 0
        and last entry is Channel 7.

        :return: Boolean list representing if a channel is enabled.
        :rtype: list
        """

        status = [False] * 8
        output = self.ask("$" + self.address + '6')
        self.check_get_errors(output)
        hex_string = output[-2:]
        for idx, i in enumerate(list(reversed(
                [bool(int(i)) for i in bin(int(hex_string, 16))[2:]]))):
            status[idx] = i
        return status
