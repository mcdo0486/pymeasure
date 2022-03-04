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

from pymeasure.instruments import Instrument

from .omega_registers import OMEGA_COMMANDS


class CS8DPT(Instrument):
    """ Represents the Omega CS8DPT Universal Benchtop Digital Temperature Controller

    An instance of `OmegaAdapter` is required to instanitate the `CS8DPT`

    .. code-block:: python

        adapter = OmegaAdapter('/dev/ttyACM0', 1)
        inst = CS8DPT(adapter)

    :param adapter: instance of OmegaAdapter

    """
    commands = OMEGA_COMMANDS

    setpoint_1 = Instrument.control(
        "CURRENT_SETPOINT_1", "CURRENT_SETPOINT_1:%f",
        commands['CURRENT_SETPOINT_1']['description'],
    )
    setpoint_2 = Instrument.control(
        "CURRENT_SETPOINT_2", "CURRENT_SETPOINT_2:%f",
        commands['CURRENT_SETPOINT_2']['description'],
    )

    run_mode = Instrument.control(
        "RUN_MODE", None,
        commands['RUN_MODE']['description'],
        cast=int
    )

    thermocouple = Instrument.control(
        "CURRENT_INPUT_VALUE", None,
        commands['CURRENT_INPUT_VALUE']['description'],
    )

    ####################
    # Methods        #
    ####################

    def __init__(self, adapter, **kwargs):
        super().__init__(
            adapter, "Omega CS8DPT", **kwargs
        )
        self.run_modes = {
            'LOAD': (0, 'File transfer in progress'),
            'IDLE': (1, 'Idle, no control'),
            'INPUT_ADJUST': (2, 'Adjusting input value'),
            'CONTROL_ADJUST': (3, 'Adjusting output value'),
            'MODIFY': (4, 'Modify parameter in OPER mode'),
            'WAIT': (5, 'Adjusting input value'),
            'RUN': (6, 'System is running'),
            'STANDBY': (7, 'Standby mode'),
            'STOP': (8, 'Stopped mode'),
            'PAUSE': (9, 'Paused mode'),
            'FAULT': (10, 'Fault detected'),
            'SHUTDOWN': (11, 'Shutdown condition detected'),
            'AUTOTUNE': (12, 'Autotune in progress'),

        }

    def idle(self):
        """ Set the instrument to IDLE mode """
        self.write('RUN_MODE:1')

    def wait(self):
        """ Set the instrument to WAIT mode """
        self.write('RUN_MODE:5')

    def run(self):
        """ Set the instrument to RUN mode """
        self.write('RUN_MODE:6')

    def standby(self):
        """ Set the instrument to STANDBY mode """
        self.write('RUN_MODE:7')

    def stop(self):
        """ Set the instrument to STOP mode """
        self.write('RUN_MODE:8')

    def pause(self):
        """ Set the instrument to PAUSE mode """
        self.write('RUN_MODE:9')

    def shutdown(self):
        """ Set the instrument to PAUSE mode """
        self.write('RUN_MODE:11')

    def read(self):
        """ Omega doesn't implement read(), instead it implements self.ask(command)
         to return data from instrument.
        """
        raise NameError("Omega instrument doesn't implement read()")
