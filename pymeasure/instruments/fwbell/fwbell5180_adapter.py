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

from pymeasure.adapters import Adapter
import usb.core
import struct


class FWBell5180_Adapter(Adapter):
    """ USB adapter FW Bell 5180 Handheld Gaussmeter and
    provides a high-level interface for interacting with the
    instrument. Valid commands are listed in self.COMMANDS.

    .. code-block:: python
        adapter = FWBell5180_Adapter()  # Connects over USB port by builtin VENDOR_ID and PRODUCT_ID
    """

    # Commands in hex to send over USB
    IDN_Q = '012B1800D07B0000'
    MEASURE_FLUX_Q = '012B1000107C0000'
    UNIT_FLUX_Q = '012B1000107C0000'
    UNIT_AC_GAUSS = '012B12020001B440'
    UNIT_AC_TESLA = '012B120201012441'
    UNIT_AC_AM = '012B12020201D441'
    UNIT_DC_GAUSS = '012B120200007481'
    UNIT_DC_TESLA = '012B12020100E480'
    UNIT_DC_AM = '012B120202001480'
    AUTO_RANGE = '012B200101BED100'
    RANGE_Q = '012B1A00B07A0000'
    RANGE_0 = '012B19010073C000'
    RANGE_1 = '012B190101B30100'
    RANGE_2 = '012B190102B24100'
    RESET = '012B37020001B84B'

    # List of supported commands
    COMMANDS = {
        '*IDN?': IDN_Q,
        ':MEASURE:FLUX?': MEASURE_FLUX_Q,
        ':UNIT:FLUX?': UNIT_FLUX_Q,
        ':UNIT:FLUX:AC:GAUSS': UNIT_AC_GAUSS,
        ':UNIT:FLUX:AC:TESLA': UNIT_AC_TESLA,
        ':UNIT:FLUX:AC:AM': UNIT_AC_AM,
        ':UNIT:FLUX:DC:GAUSS': UNIT_DC_GAUSS,
        ':UNIT:FLUX:DC:TESLA': UNIT_DC_TESLA,
        ':UNIT:FLUX:DC:AM': UNIT_DC_AM,
        ':SENS:FLUX:RANG:AUTO': AUTO_RANGE,
        ':SENS:FLUX:RANG?': RANGE_Q,
        ':SENS:FLUX:RANG 0': RANGE_0,
        ':SENS:FLUX:RANG 1': RANGE_1,
        ':SENS:FLUX:RANG 2': RANGE_2,
        '*CLS': RESET,
    }

    QUERIES = [i for i in COMMANDS if '?' in i]

    def __init__(self, preprocess_reply=None, **kwargs):
        self.preprocess_reply = preprocess_reply
        # Decimal VendorID=5794 & ProductID=20736
        # Hexadecimal VendorID=0x16a2 & ProductID=0x5100
        VENDOR_ID = 0x16a2
        PRODUCT_ID = 0x5100
        self.connection = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
        if self.connection is None:
            raise ValueError('FW Bell 5180 not found. Please ensure it is connected to the tablet.')

        # Claim interface 0 - this interface provides IN and OUT endpoints to write to and read from
        usb.util.claim_interface(self.connection, 0)
        # Once connected, we need to send RANGE_Q and read back. This is needed for initialization.
        self.write(':SENS:FLUX:RANG?')

    @staticmethod
    def get_idn(out_data):
        length = int(out_data[3])
        response = out_data[4:length + 4]
        return bytearray(response).decode('utf-8').strip('\x00')

    @staticmethod
    def get_units(out_data):
        response = ''
        ac_dc = bool(out_data[9])
        response += 'AC:' if ac_dc else 'DC:'
        mode = int(out_data[6])
        if mode == 0:
            response += 'GAUSS'
        elif mode == 1:
            response += 'TESLA'
        else:
            response += 'AM'
        return response

    @staticmethod
    def get_range(out_data):
        return int(out_data[4])

    @staticmethod
    def get_measurement(out_data):
        if out_data[2] == 16:
            response = struct.unpack('>h', out_data[4:6])[0]
            scale = int(out_data[7])
            if scale == 0:
                response *= 1e-5
            elif scale == 1:
                response *= 1e-4
            else:
                response *= 1e-3
        else:
            raise ValueError("Invalid output data")
        return response

    def write(self, command, read_bytes=128):
        """ Writes a command to the instrument
        :param command: SCPI command string to be sent to the instrument.
        :param read_bytes: Number of bytes to read from the instrument. Default 128
        """
        command = command.upper()
        if command in self.COMMANDS:
            self.connection.write(0x01, bytearray.fromhex(self.COMMANDS[command]))
            return self.connection.read(0x81, read_bytes)
        else:
            raise NameError("Invalid command")

    def read(self):
        raise NotImplementedError("Read isn't implemented with FWBell5180")

    def ask(self, command, read_bytes=128):
        """ Queries a command to the instrument
        :param command: Query command string to be sent to the instrument
        :param read_bytes: Number of bytes to read from the instrument. Default 128
        """
        command = command.upper()
        if command in self.QUERIES:
            out_data = self.write(command, read_bytes)
            if command == ':MEASURE:FLUX?':
                return self.get_measurement(out_data)
            elif command == ':UNIT:FLUX?':
                return self.get_units(out_data)
            elif command == ':SENS:FLUX:RANG?':
                return self.get_range(out_data)
            else:
                # Last supported ask command is '*IDN?'
                return self.get_idn(out_data)
        else:
            raise NameError("Invalid command")

    def shutdown(self):
        usb.util.dispose_resources(self.connection)
        self.connection = None
