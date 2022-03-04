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
import minimalmodbus

from .omega_registers import OMEGA_COMMANDS


class OmegaAdapter(Adapter):
    """ Adapter class for CS8DPT instrument using the minimalmodbus package to allow
    serial communication to instrument

    :param port: String denoting the serial port name, for example ``/dev/ttyACM0`` (Linux), ``/dev/tty.usbserial`` (OS X) or ``COM3`` (Windows).
    :param address: Integer denoting the address of the device, default is 1
    :param kwargs: Any valid key-word argument for adapter class
    """
    commands = OMEGA_COMMANDS

    def __init__(self, port, address=1, **kwargs):
        super().__init__(**kwargs)
        self.connection = minimalmodbus.Instrument(port, address)

    def valid(self, command, mode):
        """ Validates command and read/write mode

        :returns: Dictionary from OMEGA_COMMANDS with register information
        """
        if command in self.commands:
            if mode in self.commands[command]['read_write']:
                return self.commands[command]
            else:
                raise ValueError("Mode is not supported for command %s: %s".format(command, mode))
        else:
            raise NameError("Command is not supported: %s".format(command))

    def write(self, command_value):
        """ Writes a value to a register on the instrument

        :param command_value: Semicolon delimited string in the format of "command:value" which is split, validated, then sent to instrument.
        """
        command = command_value.split(':')[0]
        value = command_value.split(':')[1]
        register = self.valid(command, 'W')
        data_type = register['data_type']
        if data_type == 'F':
            self.connection.write_float(register['register'], float(value))
        elif data_type == 'L':
            self.connection.write_long(register['register'], int(value))
        elif data_type == 'R':
            self.connection.write_register(register['register'], int(value))

    def ask(self, command):
        """ Reads a register on the instrument

        :param command: String of the command which is validated then sent to the instrument.
        :returns: Value from the instrument
        """
        register = self.valid(command, 'R')
        data_type = register['data_type']
        if data_type == 'F':
            return self.connection.read_float(register['register'])
        elif data_type == 'L':
            return self.connection.read_long(register['register'])
        elif data_type == 'R':
            return self.connection.read_register(register['register'])

        raise ValueError("Mode is not supported for command %s: %s" % command)
