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
    """ Represents the F.W. Bell 5081 Handheld Gaussmeter and
    provides a high-level interface for interacting with the
    instrument

    :param port: The serial port of the instrument

    .. code-block:: python

        meter = FWBell5081_Adapter()  # Connects over USB port by builtin  VENDOR_ID and PRODUCT_ID

    """
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
        '*OPC': RESET,
    }

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
        self.connection.write(0x01, bytearray.fromhex(self.RANGE_Q))

    def get_idn(self, out_data):
        length = int(out_data[3])
        response = out_data[4:length + 4]
        return response.decode('utf-8').strip('\x00')

    def get_units(self, out_data):
        response = ''
        ac_dc = int(out_data[9])
        print('ac', ac_dc)
        response += 'ac:' if ac_dc else 'dc:'
        mode = int(out_data[6])
        print(out_data)
        if mode == 0:
            response += 'gauss'
        elif mode == 1:
            response += 'tesla'
        elif mode == 2:
            response += 'am'
        return response

    def get_range(self, out_data):
        scale = int(out_data[7])
        if scale == 0:
            response = 0
        elif scale == 1:
            response = 1
        else:
            response = 2
        return response

    def get_measurement(self, out_data):
        if out_data[10] == 10:
            response = struct.unpack('>h', out_data[4:6])[0]
            print(bytearray(out_data).hex())
            scale = int(out_data[7])
            if scale == 0:
                response *= 1e-5
            elif scale == 1:
                response *= 1e-4
            else:
                response *= 1e-3
        else:
            response = 'invalid'  # -1
        return response

    def write(self, command):
        """ Writes a command to the instrument
        :param command: SCPI command string to be sent to the instrument
        """
        command = command.upper()
        if command in self.COMMANDS:
            self.connection.write(0x01, bytearray.fromhex(self.COMMANDS[command]))
            #out_data = self.connection.read(0x81, 128)
        else:
            raise NameError("Invalid command")

    def read(self, bytes=128):
        return self.connection.read(0x81, bytes)

    def ask(self, command, bytes=128):
        question_commands = [i for i in self.COMMANDS if '?' in i]
        command = command.upper()
        if command in self.COMMANDS:
            self.connection.write(0x01, bytearray.fromhex(self.COMMANDS[command]))
            out_data = self.connection.read(0x81, bytes)
            if command == ':MEASURE:FLUX?':
                return self.get_measurement(out_data)
            elif command == ':UNIT:FLUX?':
                return self.get_units(out_data)
            elif command == ':SENS:FLUX:RANG?':
                return self.get_range(out_data)
            else:
                #'*IDN?'
                return self.get_idn(out_data)
        else:
            raise NameError("Invalid command")

