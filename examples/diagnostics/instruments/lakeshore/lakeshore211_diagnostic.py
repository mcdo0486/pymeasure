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
# Field Sweep Procedure File
# =============================================================================

# Procedure file for a PyMeasure-based program that measures the magnetic
# response of a sample as a function of magnetic field for the vibrating
# sample magnetometer (VSM).
#
# Program uses the following instruments:
#   Signal Recovery 7225 Lock-in amplifier - Measures pickup voltage from VSM
#   TDK-Lambda Genesys 40-38 power supply: Powers electromagnet
#   BraunBox - Custom-built high current switching relay w/ Arduino
#   control board
#   FW Bell 5080 - Measures magnetic field
#   Lakeshore 211 - Temperature monitor

# =============================================================================
# Libraries / modules
# =============================================================================

from pymeasure.instruments.lakeshore.lakeshore211 import LakeShore211
from pymeasure.experiment import Procedure, Worker, Results
from pymeasure.experiment import Parameter
from pymeasure.log import console_log

from time import sleep
import logging
import sys

# =============================================================================
# Logging
# =============================================================================

log = logging.getLogger(__name__)

if log.hasHandlers():
    log.handlers.clear()

log.addHandler(logging.NullHandler())


# =============================================================================
# Procedure class
# =============================================================================


class TempDiagnostic(Procedure):
    """ Class that implements the Lakeshore 211 diagnostic test procedure."""

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Measurement Parameters
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Lakeshore 211  communication port address (RS232)
    lakeshore_address = Parameter("Lakeshore 211 Address", default="COM5")

    # Column order of output data file
    DATA_COLUMNS = ["Time (s)",
                    "Temp (K)"]

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Initialization
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Initializes Lakeshore 211 temperature monitor object
    lakeshore = None

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Startup method
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def startup(self):
        """Starts up the diagnostic test."""

        log.info("\nStartup function initiated")
        log.info("Reticulating splines")
        print("\n", file=sys.stderr)

        # Lakeshore 211 setup
        log.info("Lakeshore 211 setup: start")
        self.lakeshore = LakeShore211(self.lakeshore_address)
        self.lakeshore.reset()
        sleep(.5)
        self.lakeshore.display_units = "kelvin"
        sleep(.5)
        log.info("Lakeshore 211 setup: complete!")

        log.info("Startup complete!")
        print("\n", file=sys.stderr)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Execute method
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def execute(self):
        """Begin diagnostic test."""

        # Basic communication check: ID query
        log.info("Begin diagnostics")
        log.info("Does the following line resemble "
                 "'LSCI,MODEL211,2110814,040202'?")
        log.info(self.lakeshore.id)
        print("\n", file=sys.stderr)
        sleep(10)

        # Units check
        log.info("""Does the Lakeshore 211 show Celsius as the units?
         Check front panel within 10 seconds.""")
        self.lakeshore.display_units = "celsius"
        sleep(10)
        units = self.lakeshore.display_units
        log.info(f"""Does the Lakeshore 211 is reporting that the current
        units is {units}. Is this correct?""")
        print("\n", file=sys.stderr)
        sleep(10)

        # Temperature reading
        log.info("""The Lakeshore 211 will now read the current temperature
        in Celsius.""")
        temp = self.lakeshore.temperature_celsius
        log.info(f"""Does the Lakeshore 211 front panel show the temperature to
        be approximately {temp} C?""")
        print("\n", file=sys.stderr)
        sleep(10)

        # Switch to Kelvin
        log.info("""Does the Lakeshore 211 show Kelvin as the units?
        Check front panel within 10 seconds.""")
        self.lakeshore.display_units = "kelvin"
        sleep(10)
        temp = self.lakeshore.temperature_kelvin
        log.info(f"""Does the Lakeshore 211 front panel show the temperature to
        be approximately {temp} K?""")
        print("\n", file=sys.stderr)
        sleep(10)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Shutdown method
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def shutdown(self):
        """Shuts down the measurement."""

        log.info("Lakeshore 211 shutdown: start")
        self.lakeshore.shutdown()
        log.info("SR 7225 shutdown: complete!")
        log.info("Program complete! Have a good day!")


if __name__ == "__main__":

    # =========================================================================
    # Logging
    # =========================================================================

    log = logging.getLogger(__name__)

    if log.hasHandlers():
        log.handlers.clear()

    log.addHandler(logging.NullHandler())

    scribe = console_log(log)
    scribe.start()

    # =========================================================================
    # Main Program
    # =========================================================================

    procedure = TempDiagnostic()
    procedure.lakeshore_address = "COM3"
    # Currently using current directory for test file
    file_name = "./test.csv"
    results = Results(procedure, file_name)
    worker = Worker(results)
    worker.start()

    worker.join(timeout=3600)  # wait at most 1 hr (3600 sec)
    scribe.stop()
