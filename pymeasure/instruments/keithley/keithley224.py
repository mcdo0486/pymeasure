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
    commands have been coded. Status of commands have been included in
    the docstrings. Note: the Excecute command (X) is enacted after every 
    command.
    """
    

    ##############
    # Properties #
    ##############
    
    srq_mode = Instrument.setting(
        "M%dX", 
        """Integer property that sets SRQ (service request) mode. See Model 
        Keithley 2243 IEEE Interface Manual for various mode option. Integer 
        range between 0 to 31 (inclusive). Property has not been tested.""",
        validator = strict_discrete_set,
        values = list(range(0,32)),
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
        9 - range: 100 mA, max: +/- 101 mA, step size: 50 uA
        Property has been tested. Property has been tested.""",
        validator = strict_discrete_set,
        values = [0, 5, 6, 7, 8, 9],
        )
        
    current = Instrument.setting(
        "I%gX",
        """Float property that sets the desired sourcing current value. 
        Max current: +/- 101 mA. Property has been tested.""",
        validator = lambda v, vs: strict_discrete_range(v, vs, 5e-9),
        values = [-101e-3, 101e-3]    
        )
    
    voltage_limit = Instrument.setting(
        "V%dX",
        """Integer property that sets the desired sourcing current. Max voltage 
        limit: 105 V. Default value is 3 V. Property has been tested.""",
        validator = strict_discrete_set,
        values = list(range(0,106)),       
        )
    
    dwell_time = Instrument.setting(
        "W%gX",
        """Float property that sets the desired dwell time. Value must be 
        between 50 ms and 999.9 s. Default value is 50 ms. Property has been
        tested.""",
        validator = lambda v, vs: strict_discrete_range(v, vs, 0.001),
        values = [50e-3, 999.9],     
        )
    
        
    data_terminator = Instrument.setting(
        "Y%sX",
        """String prperty that sets the data string terminator. Any ASCII 
        character can be used except any capital letter, any number, a blank 
        value, +, -, /, ., or e. Default value is LF for carraige return 
        and line feed. Property has not been tested."""
        )
    
    
    ###########
    # Methods #
    ###########
    
    def __init__(self, adapter, **kwargs):
        super().__init__(
            adapter, "Keithley 224 Current Source",
        )   
     
    def display_current(self):
        """Method that displays the sourcing current on the instrument front 
        panel. Performs the same function as pressing the front panel SOURCE 
        button. Method has been tested.
        """
        self.write("D0X")
    
    def display_voltage_limit(self):
        """Method that displays the voltage limit on the instrument front 
        panel. Performs the same function as pressing the front panel V-LIMIT 
        button. Method has been tested.
        """
        self.write("D1X")
    
    def display_dwell_time(self):
        """Method that displays the dwell time on the instrument front panel. 
        Performs the same function as pressing the front panel TIME button.
        Method has been tested.
        """
        self.write("D2X")

    def output_off(self):
        """ Method that turns off output. Performs the same function as 
        pressing the OPERATE button and having the OUTPUT light turn off.
        Method has been tested.
        """
        self.write("F0X")

    def output_on(self):
        """ Method that turns on output. Performs the same function as 
        pressing the OPERATE button and having the OUTPUT light turn on.
        Method has been tested.
        """
        self.write("F1X")

    def talk_prefix_on(self):
        """ Method that that sets the insturment to send data strings
        with prefixes designating current, voltage, and dwell time when
        addressed to talk. Default value is on. Method has been tested.
        """
        self.write("G0X")

    def talk_prefix_off(self):
        """ Method that that sets the insturment to send data strings
        without prefixes designating current, voltage, and dwell time when
        addressed to talk. Default value is on.
        Method has been tested.
        """
        self.write("G1X")

    def eoi_on(self):
        """ Method to send the GPIB EOI (End or Identify) line after the last 
        byte in a data transfer sequence. Default is to send the EOI line.
        Method has not been tested.
        """
        self.write("K0X")

    def eoi_off(self):
        """ Method to not send the GPIB the EOI (End or Identify) line after 
        the last byte in a data transfer sequence. Default value is to send 
        the EOI line. Method has not been tested.
        """
        self.write("K1X")
        
    def status(self):
        """ Method that reads status of the instrument. Data provided as a 
        string with order of current, voltage limit, and dwell time. Data 
        prefixes present by default. Method has been tested.
        """
        return self.read()



