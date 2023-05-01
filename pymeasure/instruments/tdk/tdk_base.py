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
from pymeasure.instruments.validators import strict_range
from pymeasure.instruments.validators import strict_discrete_set
from pymeasure.instruments.validators import strict_discrete_range
import logging
from time import sleep
import numpy as np

# =============================================================================
# Logging
# =============================================================================

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


# =============================================================================
# Instrument file
# =============================================================================


class TDK_Lambda_Base(Instrument):
    """
    This is the base class for TDK Lambda Genesys Series DC power supplies.

    Do not directly instantiate an object with this class. Use one of the
    TDK-Lambda power supply instrument classes that inherit from this parent
    class.

    Untested commands are noted in docstrings.
    """

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Initializer and important communication methods
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, adapter, address, **kwargs):
        super().__init__(
            adapter,
            name="TDK-Lambda Base",
            includeSCPI=False,
            asrl={'read_termination': "\r", 'write_termination': "\r"},
            **kwargs
        )
        self.address = address

    def write(self, command):
        """Modifies the self.write() method to strip out an "OK" command that
        the instrument returns for any non-querying commands.

        By default, any non-querying commands (i.e., a command that does NOT
        have the "?" symbol in it, a.k.a. a "setting" in PyMeasure syntax) will
        automatically return an "OK" reply. This is done to confirm that the
        instrument has received the command. Any querying commands (i.e., a
        command that does have the "?" symbol in it, a.k.a. a "measurement" in
        PyMeasure syntax) by definition will return a value. The returned value
        itself is confirmation that the command was received.

        The default, the instrument.write() method is not set up to
        automatically strip out  this "OK" for non-querying commands. This
        modification will run the self.ask() method to remove the "OK"
        command from the VISA read buffer. If this is not done, the VISA read
        buffer will hold numerous "OK" commands until the next read command
        is given.

        :param command: Command string to be sent to the instrument.
        """

        self.ask(command)

    def ask(self, command):
        """Modifies the self.ask() method to NOT use the self.write() method,
        but instead to use the self.adapter.connection.query() command.

        This modification is a result due to the .write() method modification.
        Because self.write() now returns self.ask(), the .ask() method goes
        into an infinite loop is this modification is not implemented.

        :param command: Command string to be sent to the instrument
        """
        return self.adapter.connection.query(command)



    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Properties
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    address = Instrument.setting(
        "ADR %d",
        """Set the address of the power supply 
        
        Valid values are integers between 0 - 30 (inclusive).""",
        validator=strict_discrete_set,
        values=list(range(0, 31))
    )

    clear = Instrument.setting(
        "CLS",
        """Set FEVE and SEVE registers to zero.
        
        Property is UNTESTED.
        """
    )

    reset = Instrument.setting(
        "RST",
        """Set the instrument to restart."""
    )

    remote = Instrument.control(
        "RMT?", "RMT %s",
        """Control remote operation of the power supply.
        
        Valid values are ``loc`` for local mode, ``rem`` for remote mode, and 
        ``llc`` for local lockout mode.
        """,
        validator=strict_discrete_set,
        values=["LOC", "REM", "LLO"]
    )

    multidrop_capability = Instrument.measurement(
        "MDAV?",
        """Measure to see if the multi-drop option is available on the power
        supply. 
        
        If return value is 0, the option is not available, if 1 it is 
        available.
        
        Property is UNTESTED.
        """
    )

    master_slave_setting = Instrument.measurement(
        "MS?",
        """Measure the master and slave settings. 
        
        Possible master return values are 1, 2, 3, and 4. The slave value is 0.
        
        Property is UNTESTED.
        """
    )

    repeat = Instrument.measurement(
        "\\",
        """Measure the last command again.
        
        Returns the last command.
        
        Property is UNTESTED.
        """
    )

    identity = Instrument.measurement(
        "IDN?",
        """Measure the identity of the instrument.
        
        Returns the instrument model as an ASCII string in the format:
        ``LAMBDA, GENX-Y``
        
        Property is UNTESTED.
        """
    )

    version = Instrument.measurement(
        "REV?",
        """Measure the software version on instrument.
        
        Returns the software version as an ASCII string.
        
        Property is UNTESTED.
        """
    )

    serial = Instrument.measurement(
        "SN?",
        """Measure the serial number of the instrument.
        
        Returns the serial number of of the instrument as an ASCII string.
        
        Property is UNTESTED.
        """
    )

    last_test_date = Instrument.measurement(
        "DATE?",
        """Measure the date of the last test.
        
        Returns the date of last test in as a string in the format: yyyy/mm/dd.
        
        Property is UNTESTED.
        """
    )

    voltage = Instrument.control(
        "PV?", "PV %g",
        """Control the programmed (set) output voltage.""",
        validator=lambda v, vs: strict_discrete_range(v, vs, step=0.01),
        values=[0, 40],
        dynamic=True
    )

    actual_voltage = Instrument.measurement(
        "MV?",
        """Measure the the actual output voltage."""
    )

    current = Instrument.control(
        "PC?", "PC %g",
        """Control the programmed (set) output current.""",
        validator=lambda v, vs: strict_discrete_range(v, vs, step=0.01),
        values=[0, 38],
        dynamic=True
    )

    actual_current = Instrument.measurement(
        "MC?",
        """Measure the actual output current.
        
        Current value returned with five digits of precision.
        """
    )

    mode = Instrument.measurement(
        "MODE?",
        """Measure the output mode of the power supply.
        
        When power supply is on, the returned value will be either ``CV`` or 
        ``CC`` for control voltage or control current, respectively. If the 
        power supply is off, the returned value will be ``OFF``.
        
        Property is UNTESTED.
        """
    )

    display = Instrument.measurement(
        "DVC?",
        """Measure the display voltage and current.
        
        Returns the measured voltage, programmed voltage, measured current,
        programmed current, over voltage set point, and under voltage set point 
        as a list of floating point numbers.
        """
    )

    status = Instrument.measurement(
        "STT?",
        """Measure the power supply status.
        
        Returns a string of ASCII characters representing the actual voltage 
        (MV), the programmed voltage (PV), the actual current (MC), the 
        programmed current (PC), the status register (SR), and the fault
        register (FR).        
        """
    )

    pass_filter = Instrument.control(
        "FILTER?", "FILTER %d",
        """Control the low pass filter frequency of the A to D converter
        for voltage and current measurement.
        
        Valid frequency values are 18, 23, or 46 Hz. Default value is 18 Hz.
        """,
        validator=strict_discrete_set,
        values=[18, 23, 46]
    )

    source_output = Instrument.control(
        "OUT?", "OUT %s",
        """Control the output of the power supply.
        
        Valid values are ``ON`` and ``OFF``. 
        """,
        validator=strict_discrete_set,
        values=["ON", "OFF"]
    )

    foldback = Instrument.control(
        "FLD?", "FLD %s",
        """Control the fold back protection of the power supply.
        
        Valid values are ``ON`` to arm the fold back protection and ``OFF`` to 
        cancel the fold back protection.
        
        Property is UNTESTED.
        """,
        validator=strict_discrete_set,
        values=["ON", "OFF"]
    )

    foldback_delay = Instrument.control(
        "FBD?", "FBD %g",
        """Control the fold back delay.
         
        Adds an additional delay to the standard fold back delay (250 ms) by 
        multiplying the set value by 0.1. Valid values are integers between 
        0 to 255.
        
        Property is UNTESTED.
        """,
        validator=strict_range,
        values=[0, 255],
        cast=int
    )

    foldback_reset = Instrument.setting(
        "FDBRST",
        """Set the additional fold back delay back to 0 s, restoring the
        standard 250 ms delay.
        
        Property is UNTESTED.
        """
    )

    over_voltage = Instrument.control(
        "OVP?", "OVP %g",
        """Control the over voltage protection.
        
        Property is UNTESTED.
        """,
        validator=lambda v, vs: strict_discrete_range(v, vs, step=0.01),
        values=[2, 44],
        dynamic=True
    )

    over_voltage_max = Instrument.setting(
        "OVM",
        """Set the over voltage protection to the maximum level for the power
        supply.
        
        Property is UNTESTED.
        """
    )

    under_voltage = Instrument.control(
        "UVL?", "UVL %g",
        """Control the under voltage limit.
        
        Property is UNTESTED.
        """,
        validator=lambda v, vs: strict_discrete_range(v, vs, step=0.01),
        values=[0, 38],
        dynamic=True
    )

    auto_restart = Instrument.control(
        "AST?", "AST %s",
        """Control the auto restart mode. 
        
        Valid values are ``ON`` and ``OFF``.
        
        Property is UNTESTED.
        """,
        validator=strict_discrete_set,
        values=["ON", "OFF"]
    )

    save = Instrument.setting(
        "SAV",
        """Set the instrument to save its settings.
        
        Property is UNTESTED.
        """
    )

    recall = Instrument.setting(
        "RCL",
        """Set the instrument to recall its settings.
        
        Property is UNTESTED.
        """
    )

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Methods
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def ramp_to_current(self, target_current, steps=20, pause=0.2):
        """Ramps to a target current from the set current value over
        a certain number of linear steps, each separated by a pause duration.

        :param target_current: Target current in amps
        :param steps: Integer number of steps
        :param pause: Pause duration in seconds to wait between steps
        """

        currents = [round(i, 2) for i in np.linspace(self.current,
                                                     target_current, steps)]
        for current in currents:
            self.current = current
            sleep(pause)

    def shutdown(self):
        """Safety shutdown the power supply.

        Ramps the power supply down to zero current using the
        .ramp_to_current() method and turns the output off.
        """
        log.info("Shutting down %s." % self.name)
        self.ramp_to_current(0.0)
        self.source_output = "OFF"
        log.info("%s has been shut down." % self.name)
        super().shutdown()
