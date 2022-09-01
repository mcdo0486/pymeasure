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
from time import sleep, time

import numpy as np

from pymeasure.instruments import Instrument
from pymeasure.instruments.validators import truncated_discrete_set, \
    modular_range_bidirectional, strict_discrete_set, strict_discrete_range

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class Gen40_38(Instrument):
    """
    This is the class for the DSP 7225 lockin amplifier
    Modified version of the DSP7265 driver with reduced functionality
    """
    
    def __init__(self, resourceName, address, **kwargs):
        super().__init__(
            resourceName,
            "TDK Lambda Gen40-38",
            includeSCPI=False,
            **kwargs
        )
        self.adapter.connection.read_termination = '\r'
        self.adapter.connection.write_termination = '\r'
        self.address = address
    
    
    def write(self, command):
        """ Queries a command to the instrument
        "OK\r"        

        :param command: SCPI command string to be sent to the instrument
        """
        self.ask(command)
        
       # self.adapter.connection.write(command)
       # if '?' is not in command:
       #     # get rid of OK
       #     self.flush()

    address = Instrument.setting(
        'ADR %d',
        """ Address of the power supply [0-30] """,
        validator=strict_discrete_set,
        values=list(range(0,31))
    )

    clear = Instrument.setting(
        'CLS',
        """Clear status sets FEVE and SEVE registers to zero """
    )
    
    reset = Instrument.setting(
        'CLS',
        """Clear status sets FEVE and SEVE registers to zero """
    )
    
    remote = Instrument.control(
        'RMT?','RMT %d',
        """Clear status sets FEVE and SEVE registers to zero """,
        validator=strict_discrete_set,
        values=[0,1,2] 
    )
    
    multidrop_capability = Instrument.measurement(
        'MDAV?',
        """Multi-drop option is available, 1 is installed, 0 is not installed """
    )
    
    master_slave_setting = Instrument.measurement(
        'MS?',
        """Master and slave setting. Master: n = 1,2,3,4 Slave: n = 0 """
    )
    
    repeat = Instrument.measurement(
        '\\',
        """ Repeat the last command """
    )
    
    identity = Instrument.measurement(
        'IDN?',
        """ Identity of the insturment """
    )
    
    version = Instrument.measurement(
        'REV?',
        """ Software version on instrument """
    )
    
    serial = Instrument.measurement(
        'SN?',
        """Serial number of the instrument """
    )
    
    last_test_date = Instrument.measurement(
        'DATE?',
        """ Date of the last experiment """
    )
    
    voltage = Instrument.control(
        'PV?','PV %g',
        """ Sets the desired output voltage """,
        validator=lambda value, values: strict_discrete_range(value, values, step=.01),
        values=[0,40] 
    )
    
    actual_voltage = Instrument.measurement(
        'MV?',
        """ Read the actual, measured voltage """
    )
    
    current = Instrument.control(
        'PC?','PC %g',
        """ Sets the desired output current """,
        validator=lambda value, values: strict_discrete_range(value, values, step=.01),
        values=[0,38] 
    )
    
    actual_current = Instrument.measurement(
        'MC?',
        """ Read the actual, measured current """
    )
    
    mode = Instrument.measurement(
        'MODE?',
        """ Output mode of the power supply """
    )
    
    display = Instrument.measurement(
        'DVC?',
        """ Read power supply data
        Measured voltage, programmed voltaged, measured current,
        programmed current, over voltage set point, under voltage set point,                
        """,
        get_process=lambda v: [float(i) for i in v.split(',')],
    )
    
    def format_display(self, output):
        KEYS = []
        pass
        
    status = Instrument.measurement(
        'STT?',
        """ Power supply status               
        """
    )
    
    pass_filter = Instrument.control(
        'FILTER?','FILTER %d',
        """ Low pass filter frequency of the A to D converter
        for voltage and current measurement
        """,
        validator=strict_discrete_set,
        values=[18, 23, 46] 
    )
    
    source_output = Instrument.control(
        'OUT?','OUT %d',
        """ Enable output of the power supply
        """,
        validator=strict_discrete_set,
        values=[0,1] 
    )
    
    foldback = Instrument.control(
        'FLD?','FLD %d',
        """ Foldback protection status
        """,
        validator=strict_discrete_set,
        values=[0,1] 
    )
    
    foldback_delay = Instrument.control(
        'FBD?','FBD %g',
        """ Foldback delay that is multipled by 0.1 seconds
        """,
        validator=lambda value, values: strict_discrete_range(value, values, step=.01),
        values=[0,255,1] 
    )
    
    foldback_reset = Instrument.setting(
        'FDBRST',
        """ Foldback reset               
        """
    )
    
    over_voltage = Instrument.control(
        'OVP?','OVP %g',
        """ Over voltage protection
        """,
        validator=lambda value, values: strict_discrete_range(value, values, step=.01),
        values=[2,44] 
    )
    
    over_voltage_max = Instrument.setting(
        'OVM',
        """ Over voltage set to maximum
        """,
    )
    
    under_voltage = Instrument.control(
        'UVL?','UVL %g',
        """ Set under voltage limit
        """,
        validator=lambda value, values: strict_discrete_range(value, values, step=.01),
        values=[0,38] 
    )
    
    auto_restart = Instrument.control(
        'AST?','AST %d',
        """ Set auto restart mode
        """,
        validator=strict_discrete_set,
        values=[0,1] 
    )
    
    save = Instrument.setting(
        'SAV',
        """ Save instrument settings
        """,
    )
    
    recall = Instrument.setting(
        'RCL',
        """ Recall instrument settings
        """,
    )
    
    def ramp_to_current(self, target_current, steps=20, pause=0.2):
        """ Ramps to a target current from the set current value over
        a certain number of linear steps, each separated by a pause duration.
        :param target_current: A current in Amps
        :param steps: An integer number of steps
        :param pause: A pause duration in seconds to wait between steps """
        currents = [round(i,2) for i in np.linspace(self.current, target_current, steps)]
        for current in currents:
            self.current = current
            sleep(pause)
    

    def shutdown(self):
        log.info("Shutting down %s." % self.name)
        self.ramp_to_current(0.0)
        self.source_output = False
