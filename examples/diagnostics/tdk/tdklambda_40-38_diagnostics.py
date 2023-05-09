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
# TDK Lambda Genesys 40-38 DC power supply Live Test
# =============================================================================

# Procedure file to quickly test that a TDK Lambda Genesys 40-38 DC power supply
# driver file works with the PyMeasure library. File can also be used
# to demonstrate basic connectivity with the instrument.
#
# Instrument may or may not be hooked up to anything. Tests will not supply
# a live voltage.

# =============================================================================
# Libraries / modules
# =============================================================================

from pymeasure.instruments.tdk.tdk_gen40_38 import TDK_Gen40_38
from pymeasure.experiment import Procedure, Worker, Results
from pymeasure.experiment import Parameter
from pymeasure.log import console_log

from time import sleep
import logging
import sys


# =============================================================================
# Procedure class
# =============================================================================


class TDK_Gen40_38Diagnostic(Procedure):
    """ Class that implements the diagnostic test for the DSP7225."""

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Measurement Parameters
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # TDK Lambda Genesys 40-38 communication port
    tdk_port = Parameter('TDK_Gen40_38 Port', default="COM4")

    # TDK Lambda Genesys 40-38 communication address
    tdk_address = Parameter('TDK_Gen40_38 address', default=6)

    # Column order of output data file
    DATA_COLUMNS = ["Time [s]",
                    "PSU Voltage [V]",
                    "PSU Current [A]"]

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Initialization
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Initializes TDK Lambda Genesys 40-38 object
    tdk = None

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Startup method
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def startup(self):
        """Starts up the diagnostic test."""

        log.info("\nStartup function initiated")
        log.info("Reticulating splines")
        print("\n", file=sys.stderr)

        # Lock-in amplifier setup
        log.info("TDK Lambda Genesys 40-38 setup: start")
        self.tdk = TDK_Gen40_38(self.tdk_port)
        self.tdk.remote = "REM"
        self.tdk.output_enabled = False
        log.info("TDK Lambda Genesys 40-38 is now in remote mode with "
                 "output off.")
        sleep(10)
        log.info("TDK Lambda Genesys 40-38 setup: complete!")

        log.info("Startup complete!")
        print("\n", file=sys.stderr)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Execute method
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def execute(self):
        """Begin diagnostic test."""

        # Basic communication check: ID query
        log.info("Begin diagnostic test")
        log.info("The first test is read the response for a ID command. "
                 "Check to see if the response is: ['LAMBDA', 'GEN40-38]")
        id = self.tdk.id
        log.info(f"ID response: {id}.")
        print("\n", file=sys.stderr)
        sleep(10)

        log.info("Switching to local mode.")
        self.tdk.remote = 'LOC'
        local_mode = self.tdk.remote
        log.info(f"The instrument remote mode is {local_mode}. Does this "
                 "match the front panel value? The REM/LOC light should "
                 "be off.")
        sleep(10)

        log.info("Switching to remote mode.")
        self.tdk.remote = 'REM'
        local_mode = self.tdk.remote
        log.info(f"The instrument remote mode is {local_mode}. Does this "
                 "match the front panel value? The REM/LOC light should "
                 "be on.")
        print("\n", file=sys.stderr)
        sleep(10)

        # Over voltage test
        log.info("The instrument will now set the max over voltage.")
        self.tdk.set_max_over_voltage()
        sleep(2)

        over_voltage = self.tdk.over_voltage
        log.info(f"The over voltage is {over_voltage} V. Does this "
                 "match the front panel value? To check the over voltage, "
                 "first press the REM/LOC button. Then press the OVP button "
                 "to see the over voltage protection. Once done, press the "
                 "OVP button two times more to get back to the front panel.")
        print("\n", file=sys.stderr)
        sleep(30)

        # Output enabled
        log.info("The instrument will now enable the source output.")
        self.tdk.output_enabled = True
        log.info(f"The source output mode is {self.tdk.output_enabled}."
                 f" Does this match the front panel value?")
        print("\n", file=sys.stderr)
        sleep(10)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Shutdown method
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def shutdown(self):
        """Shuts down the measurement.

        Puts the TDK Lambda Genesys 40-38 in a safe state.
        """

        log.info("TDK Lambda Genesys 40-38 shutdown: start")
        self.tdk.shutdown()
        log.info("TDK Lambda Genesys 40-38 shutdown: complete!")
        log.info("Program complete! Have a good day!")


if __name__ == "__main__":
    # =============================================================================
    # Logging
    # =============================================================================

    log = logging.getLogger(__name__)

    if log.hasHandlers():
        log.handlers.clear()

    log.addHandler(logging.NullHandler())

    scribe = console_log(log)
    scribe.start()

    # =============================================================================
    # Main Program
    # =============================================================================

    procedure = TDK_Gen40_38Diagnostic()
    procedure.tdk_port = "COM4"
    procedure.tdk_address = 6
    # Currently using current directory for test file
    file_name = "./test.csv"
    print("\n", file=sys.stderr)
    results = Results(procedure, file_name)
    worker = Worker(results)
    worker.start()

    worker.join(timeout=3600)  # wait at most 1 hr (3600 sec)
    scribe.stop()
