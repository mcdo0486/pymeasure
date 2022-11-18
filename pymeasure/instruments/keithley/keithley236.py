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

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class Keithley236(Instrument):
    """ Class that represents the Keithley 236 Source Measure Units provides a
    high-level interface for taking different kinds of measurements. Most
    commands have been coded. Untested commands are noted in the docstrings.
    Note: the Execute command (X) is enacted after every command.
    """

    ##################
    # Initialization #
    ##################

    def __init__(self, adapter, **kwargs):
        super().__init__(
            adapter, "Keithley 236 Source Measure Units", **kwargs
        )

    ##############
    # Properties #
    ##############

    output_level = Instrument.setting(
        "B%s,%d,%dX",
        """The B command sets the output level of the instrument. When in source voltage dc mode
        `self.source(0,0)` or source current dc mode `self.source(1,0)` the output level is the
        source output level. When in source voltage sweep mode `self.source(0,1)` or source current
        sweep mode `self.source(1,1)` the output level is the bias for the sweep.
        """,
    )

    source = Instrument.setting(
        "F%d,%dX",
        """The F command selects the source and function.
        0,0 -> source voltage dc
        0,1 -> source voltage sweep
        1,0 -> source current dc
        1,1 -> source current sweep
        """,
    )

    data_format = Instrument.setting(
        "G%dX",
        """String sets data output format""",
    )

    immediate_trigger = Instrument.setting(
        "H0X",
        """The H command immediately triggers the instrument.""",
    )

    reset = Instrument.setting(
        "J%dX",
        """Do a reset or test
        0 -> Restore factory defaults
        1 -> Perform memory test
        2 -> Perform display test""",
    )

    compliance = Instrument.setting(
        "L%d,%dX",
        """The L command sets the compliance level for the programmed source and selects the
        measurement range.
        """,
    )

    operate = Instrument.setting(
        "N%dX",
        """In operate, the programmed bias level is available at the output of the instrument.
        When programmed for sweep operation, the bias level is output, but the sweep does
        not start until a trigger is received.
        O -> Standby
        1 -> Operate
        """,
    )

    filter = Instrument.setting(
        "P%dX",
        """The P command controls the amount of filtering for each measurement. With the filter
        enabled, the unit acquires and averages up to 32 successive A/D conversions for
        each measurement.
        O -> Disabled
        1 -> 2 readings
        2 -> 4 readings
        3 -> 8 readings
        4 -> 16 readings
        5 -> 32 readings
        """,
    )

    trigger_control = Instrument.setting(
        "R%dX",
        """Integer property that sets trigger control.
        0 - Disable input / output triggers
        1 - Enable input / output triggers""",
    )

    integration = Instrument.setting(
        "P%dX",
        """The S command controls the A/D hardware integration time during each measure
        phase and the display resolution of the source-measure unit. The integration times
        offer a tradeoff among speed, resolution, and noise rejection.
        O -> Fast 4 digit
        1 -> Medium 5 digit
        2 -> Line Cycle 60Hz 5 digit
        3 -> Line Cycle 50Hz 5 digit""",
    )

    config = Instrument.measurement(
        "U%dX",
        """By sending the appropriate U command and then addressing the instrument to talk
        as with normal data, you can obtain information on machine status, error conditions,
        and other data. The information is transmitted only once for each U command.
        U0
        """,
    )

    default_delay = Instrument.setting(
        "W%dX",
        """The W command controls the enabling/ disabling of a fixed delay used to
        compensate for the instrument settling time when measuring resistive loads.
        """,
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
        self.operate = False
