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

from pymeasure.instruments import Instrument
from pymeasure.instruments.validators import strict_discrete_set
from pyvisa.constants import Parity

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class LakeShore211(Instrument):
    """ Represents the Lake Shore 211 Temperature Monitor and provides
    a high-level interface for interacting with the instrument.
    
    Untested properties and methods will be noted in their docstrings.

    .. code-block:: python

        controller = LakeShore211("GPIB::1")

        print(controller.temperature_A)     # Print the temperature at sensor A

    """
    
    analog_mode = 0
    
    id = Instrument.measurement(
        "*IDN?",
        """Return the identity of the instrument.
        """,
    )
    
    analog = Instrument.control(
        "ANALOG?", "ANALOG %d,%d",
        """
        Set the analog mode and analog range.        
        Values need to be supplied as a tuple of (analog mode, analog range)
        Analog mode can be 0 or 1
        0 = voltage
        1 = current
        
        Analog mode can be 0 through 5
        
        0 = 0 – 20 K 3 = 0 – 325 K
        1 = 0 – 100 K 4 = 0 – 475 K
        2 = 0 – 200 K 5 = 0 – 1000 K        
        """,
        get_process=lambda x: (int(x[0]), int(x[1])),
        )
    
    analog_out = Instrument.measurement(
        "AOUT?",
        """Returns the percentage of output of the analog output.
        """
    )
    
    display = Instrument.control(
        "DISPFLD?", "DISPFLD %d",
        """
        Specifies input data to display. Valid entries:
        0 = Kelvin, 1 = Celsius, 2 = sensor units, 3 = Fahrenheit.
        """,
        values={'kelvin': 0, 'celsius': 1, 'sensor': 2, 'fahrenheit': 3},
        map_values=True
        )
    
    temperature_celsius = Instrument.measurement(
        "CRDG?",
        """Reads the temperature of the sensor in celsius
        """
    )
    
    temperature_fahrenheit = Instrument.measurement(
        "FRDG?",
        """Reads the temperature of the sensor in fahrenheit
        """
    )

    temperature_sensor = Instrument.measurement(
        "SRDG?",
        """Reads the temperature of the sensor in sensor units
        """
    )    

    temperature_kelvin = Instrument.measurement(
        "KRDG?",
        """Reads the temperature of the sensor in kelvin
        """
    )
    
    relay = Instrument.control(
        "RELAY?", "RELAY %d,%d",
        """
        Specifies which relay to configure
        Values need to be supplied as a tuple of (relay number, relay mode)
        Relay number can be 1 or 2
        1 = low alarm relay
        2 = high alarm relay
        
        Relay mode can be 0, 1, or 2
        0 = off
        1 = on
        2 = alarms
        
        Property is UNTESTED
        """,
        get_process=lambda x: int(x)
        )
    
    def __init__(self, adapter,  kwargs={'data_bits': 7, 'parity':Parity.odd}):
        super().__init__(
            adapter,
            "Lake Shore 211 Temperature Monitor",
            **kwargs
        )
        

    def alarm_status(self):        
        status = self.values('ALARM?')
        return [int(status[0]), float(status[1]), float(status[2]), float(status[3]), int(status[4])]
        
    def alarm_config(self, on=True, high_value=270.0, low_value=0.0, deadband=0, latch=False):        
        """Configures the alarm parameters for the input.
        
        1,270.0,0,0,1[term]
        on, high_value, low_value, deadband, latch
        """
        command_string = "ALARM %d,%g,%g,%g,%d" % (on, high_value, low_value, deadband, latch)
        
        self.write(command_string)
        
    def alarm_reset(self):
        """Configures the alarm parameters for the input.
        
        1,270.0,0,0,1[term]
        on, high_value, low_value, deadband, latch
        """
        self.write('ALMRST')
    
    def reset(self):
        """Sets instrument parameters to power-up settings.                
        """
        self.write('*RST')
        