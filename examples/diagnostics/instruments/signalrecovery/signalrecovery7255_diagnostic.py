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
# Signal Recovery DSP 7225 Live Test
# =============================================================================

# Procedure file to quickly test that a Signal Recovery DSP 7225 Lock-in
# Amplifier driver file works with the PyMeasure library. File can also be used
# to demonstrate basic connectivity with the instrument.
#
# Disconnect all BNC connections to the lock-in amplifier. The system only
# needs to be turned on and connected to host computer via GPIB card.

# =============================================================================
# Libraries / modules
# =============================================================================

# =============================================================================
# Libraries / modules
# =============================================================================

from pymeasure.instruments.signalrecovery.dsp7225 import DSP7225
from pymeasure.experiment import Procedure, Worker, Results
from pymeasure.experiment import Parameter
from pymeasure.log import console_log

from time import sleep
import logging
import sys


# =============================================================================
# Procedure class
# =============================================================================


class DSP7225Diagnostic(Procedure):
    """ Class that implements the diagnostic test for the DSP7225."""

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Measurement Parameters
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Signal Recovery 7225 communication port address (GPIB)
    lockin_address = Parameter('DSP 7225 Address', default="GPIB0::12::INSTR")

    # Column order of output data file
    DATA_COLUMNS = ["Time [s]",
                    "Frequency [Hz]",
                    "Amplitude [V]",
                    "AC Gain [dB]",
                    "Temp std [K]",
                    "PSU Voltage [V]",
                    "PSU Current [A]",
                    "X [V]",
                    "Y [V]",
                    "R [V]",
                    "Phase [degrees]"]

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Initialization
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Initializes SR 7225 lock-in amplifier object and dwell time constant
    lockin = None
    dwell_constant = 0

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Startup method
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def startup(self):
        """Starts up the diagnostic test."""

        log.info("\nStartup function initiated")
        log.info("Reticulating splines")
        print("\n", file=sys.stderr)

        # Lock-in amplifier setup
        log.info("SR 7225 lock-in amplifier setup: start")
        log.info("System will now put it self in voltage detection mode, "
                 "use the internal oscillator as the signal reference, "
                 "set the oscillator to 1 Hz with 0 V amplitude, "
                 "set the voltage sensitivity to 2 mV, "
                 "set the time constant to 1 s, "
                 "and set the AC gain to 0 dB.")
        self.lockin = DSP7225(self.lockin_address)
        self.lockin.imode = "voltage mode"
        self.lockin.setDifferentialMode(lineFiltering=False)
        self.lockin.reference = "internal"
        self.lockin.fet = 1
        self.lockin.shield = 0
        self.lockin.coupling = 0
        self.lockin.gain = 0
        self.lockin.sensitivity = 2E-3
        self.lockin.time_constant = 1
        self.lockin.frequency = 1
        self.lockin.voltage = 0
        log.info("SR 7225 lock-in amplifier setup: 10 s parameter take time.")
        sleep(10)
        log.info("SR 7225 lock-in amplifier setup: complete!")

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
                 "Check to see if the response is: 7225.")
        id = self.lockin.id
        log.info(f"ID response: {id}.")
        print("\n", file=sys.stderr)
        sleep(10)

        # Sensitivity scale control test
        log.info("The instrument will now change the sensitivity scale from "
                 "2 mV to 10 mV. You have 10 s to set the left panel to display "
                 "the SEN field.")
        sleep(10)
        log.info("Switching sensitivity scales. Check to see if the "
                 "sensitivity values correctly change.")
        self.lockin.sensitivity = 10E-3
        sleep(2)
        sensitivity = self.lockin.sensitivity
        log.info(f"The current sensitivity is {sensitivity} mV. Does this "
                 f"match the front panel value?")
        print("\n", file=sys.stderr)
        sleep(10)

        # Frequency control test
        log.info("The instrument will now change the oscillator frequency from "
                 "1 Hz to 100 Hz. You have 10 s to set the left panel to "
                 "display the OSC frequency field.")
        sleep(10)
        log.info("Switching oscillator frequencies. Check to see if the "
                 "frequencies correctly change.")
        self.lockin.frequency = 100
        sleep(2)
        frequency = self.lockin.frequency
        log.info(f"The current frequency is {frequency} Hz. Does this "
                 f"match the front panel value?")
        print("\n", file=sys.stderr)
        sleep(10)

        # Time constant check
        log.info("The instrument will now change the measurement time constant "
                 "from 1 s to 100 ms. You have 10 s to set the left panel to "
                 "display the TIME CONST field.")
        sleep(10)
        self.lockin.time_constant = 0.10
        time_constant = self.lockin.time_constant
        log.info(f"The current time constant is {time_constant} s. Does this "
                 f"match the front panel value?")
        print("\n", file=sys.stderr)
        sleep(10)

        # Time AC gain check
        log.info("The instrument will now change the AC gain from 0 dB to "
                 "20 dB. You have 10 s to set the left panel to display the AC "
                 "GAIN field.")
        sleep(10)
        self.lockin.gain = 20
        ac_gain = self.lockin.gain
        log.info(f"The AC gain is {int(ac_gain[0] * 10)} dB. Does this "
                 f"match the front panel value?")
        print("\n", file=sys.stderr)
        sleep(10)

        # Oscillator amplitude check
        log.info("The instrument will now change the oscillator amplitude from "
                 "0 V to 1 mV. You have 10 s to set the left panel to display "
                 "the OSC amplitude field.")
        sleep(10)
        self.lockin.voltage = 0.001
        amplitude = self.lockin.voltage
        log.info(f"The current oscillator amplitude is {amplitude} V. Does "
                 f"this match the front panel value?")
        print("\n", file=sys.stderr)
        sleep(10)

        # Voltage measurement check
        log.info("The instrument will now measure the X channel voltage. You "
                 "have 10 s to set the right panel to display the X field.")
        sleep(10)
        x = self.lockin.x
        log.info(f"The current X channel voltage is {x} V. Does this "
                 f"match the front panel value?")
        print("\n", file=sys.stderr)
        sleep(10)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Shutdown method
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def shutdown(self):
        """Shuts down the measurement.

        Puts the SR 7225 lock-in amplifier in a safe state.
        """

        log.info("SR 7225 shutdown: start")
        self.lockin.shutdown()
        log.info("SR 7225 shutdown: complete!")
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

    procedure = DSP7225Diagnostic()
    procedure.lockin_address = "GPIB0::12::INSTR"
    # Currently using current directory for test file
    file_name = "./test.csv"
    print("\n", file=sys.stderr)
    results = Results(procedure, file_name)
    worker = Worker(results)
    worker.start()

    worker.join(timeout=3600)  # wait at most 1 hr (3600 sec)
    scribe.stop()
