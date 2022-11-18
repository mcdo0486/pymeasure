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

import logging

from pymeasure.instruments import Instrument
from pymeasure.instruments.validators import strict_discrete_set
from pymeasure.instruments.validators import strict_discrete_range

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class Keithley224(Instrument):
    """ Class that represents the Keithley 224 Programmable Current Source
    equipped with the Keithley 2243 GPIB interface card and provides a
    high-level interface for taking different kinds of measurements. Most
    commands have been coded. Untested commands are noted in the docstrings.
    Note: the Excecute command (X) is enacted after every command.
    """

    ##################
    # Initialization #
    ##################

    def __init__(self, adapter, **kwargs):
        super().__init__(
            adapter, "Keithley 224 Current Source", **kwargs
        )

        ##############

    # Properties #
    ##############

    front_display = Instrument.setting(
        "D%dX",
        """String property that changes the front panel display. Peforms the
        same function as pressing the front panel DISPLAY buttons.""",
        validator=strict_discrete_set,
        values={"Current": 0, "VoltageLimit": 1, "DwellTime": 2},
        map_values=True,
    )

    current_range = Instrument.setting(
        "R%dX",
        """Integer property that sets output range of sourcing current.
        Default range is AUTO. Accepts discrete set of values:
        0 - range: auto, max: +/- 101 mA, step size: 5 nA
        5 - range: 10 uA, max: +/- 19.995 uA, step size: 5 nA
        6 - range: 100 uA, max: +/- 199.95 uA, step size: 50 nA
        7 - range: 1 mA, max: +/- 1.9995 mA, step size: 500 nA
        8 - range: 10 mA, max: +/- 19.995 mA, step size: 5 uA
        9 - range: 100 mA, max: +/- 101 mA, step size: 50 uA""",
        validator=strict_discrete_set,
        values=[0, 5, 6, 7, 8, 9],
    )

    current = Instrument.setting(
        "I%gX",
        """Float property that sets the desired sourcing current value.
        Max current: +/- 101 mA.""",
        validator=lambda v, vs: strict_discrete_range(v, vs, 5e-9),
        values=[-101e-3, 101e-3]
    )

    voltage_limit = Instrument.setting(
        "V%dX",
        """Integer property that sets the desired sourcing current. Max voltage
        limit: 105 V. Default value is 3 V.""",
        validator=strict_discrete_set,
        values=list(range(0, 106)),
    )

    dwell_time = Instrument.setting(
        "W%gX",
        """Float property that sets the desired dwell time. Value must be
        between 50 ms and 999.9 s. Default value is 50 ms.""",
        validator=lambda v, vs: strict_discrete_range(v, vs, 0.001),
        values=[50e-3, 999.9],
    )

    output = Instrument.setting(
        "F%dX",
        """String property that changes the output state. Performs the same
        function as pressing the OPERATE button.""",
        validator=strict_discrete_set,
        values={"OFF": 0, "ON": 1},
        map_values=True,
    )

    data_terminator = Instrument.setting(
        "Y%sX",
        """String prperty that sets the data string terminator. Any ASCII
        character can be used except any capital letter, any number, a blank
        value, +, -, /, ., or e. Default value is LF for carraige return
        and line feed.

        Property is UNTESTED."""
    )

    talk_prefix = Instrument.setting(
        "G%dX",
        """String property that sets the insturment to send data strings
        with prefixes designating current, voltage, and dwell time when
        addressed to talk. Default value is on.""",
        validator=strict_discrete_set,
        values={"ON": 0, "OFF": 1},
        map_values=True,
    )

    eoi = Instrument.setting(
        "K%dX",
        """String property to send the GPIB EOI (End or Identify) line after
        the last byte in a data transfer sequence. Default is to send the
        EOI line.

        Property is UNTESTED.""",
        validator=strict_discrete_set,
        values={"ON": 0, "OFF": 1},
        map_values=True,
    )

    srq_mode = Instrument.setting(
        "M%dX",
        """Integer property that sets SRQ (service request) mode. See Model
        Keithley 2243 IEEE Interface Manual for various mode option. Integer
        range between 0 to 31 (inclusive).

        Property is UNTESTED.""",
        validator=strict_discrete_set,
        values=list(range(0, 32)),
    )

    ###########
    # Methods #
    ###########

    def status(self):
        """ Method that reads status of the instrument. Data provided as a
        string with order of current, voltage limit, and dwell time. Data
        prefixes present by default.
        """
        return self.read()

    def shutdown(self):
        """Method that puts the instrument in a safe standby state. Output is
        turned off and current set to 1 uA.
        """
        self.output = "OFF"
        self.current = 1E-6
