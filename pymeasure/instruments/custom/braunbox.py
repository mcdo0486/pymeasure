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

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class BraunBox(Instrument):
    """
    This is the class for the BraunBox
    """

    def __init__(self, adapter,
                 name="BraunBox", pins=(10, 11, 12), **kwargs):
        super().__init__(
            adapter,
            name,
            includeSCPI=False,
            baud_rate=115200,
            **kwargs
        )

        self.command_array = [0] * 15

        self.ENABLE_PIN = pins[0]
        self.REVERSE_PIN = pins[1]
        self.FORWARD_PIN = pins[2]
        self.delay = .5
        sleep(2)

    def write_command_array(self):
        """ Writes the current command array to the instrument.
        """
        b_str = ''
        for idx, i in enumerate(self.command_array):
            b_str += '{0:02d}'.format(i)
            if idx != len(self.command_array) - 1:
                b_str += ','
        return self.ask(b_str)

    def clear_command(self):
        self.command_array = [0] * 15

    def test_com(self):
        self.command_array[0] = 0
        return self.write_command_array()

    def serial_flush(self):
        self.command_array[0] = 1
        output = self.write_command_array()
        sleep(self.delay)
        return output

    def digital_pin_mode(self, pin, mode):
        self.command_array[0] = 2
        self.command_array[1] = pin
        self.command_array[2] = mode
        output = self.write_command_array()
        sleep(self.delay)
        return output

    def digital_pin_write(self, pin, level):
        self.command_array[0] = 3
        self.command_array[1] = pin
        self.command_array[2] = level
        output = self.write_command_array()
        sleep(self.delay)
        return output

    def initialize_magnetic_field(self):

        # serial flush
        self.serial_flush()

        # Enabled Pin Set Output
        self.digital_pin_mode(self.ENABLE_PIN, 1)
        self.digital_pin_write(self.ENABLE_PIN, 0)

        # Reverse Pin Set Output
        self.digital_pin_mode(self.REVERSE_PIN, 1)
        self.digital_pin_write(self.REVERSE_PIN, 0)

        # Forward Pin Set Output
        self.digital_pin_mode(self.FORWARD_PIN, 1)
        self.digital_pin_write(self.FORWARD_PIN, 0)

        # Turn on Enable and Forward pins
        self.digital_pin_write(self.ENABLE_PIN, 1)
        self.digital_pin_write(self.FORWARD_PIN, 1)

    def shutdown(self):
        log.info("Shutting down %s." % self.name)
        super().shutdown()
