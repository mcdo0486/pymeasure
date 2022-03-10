#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2021 PyMeasure Developers
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
from pymeasure.instruments.validators import strict_discrete_set, strict_range
from collections import OrderedDict
import re


class HP4192A_settings(object):
    # We can't read the settings from the HP4192a, and so we need to keep track of them
    # as they are set.
    def __init__(self):
        # When the machine is turned on these are the default settings
        self.spot_frequency = 100.
        self.osc_level = 1.
        self.start_frequency = .005
        self.end_frequency = 13000.
        self.step_frequency = 1.
        self.spot_bias = 0.
        self.start_bias = -35.
        self.end_bias = 35.
        self.step_bias = 1.
        self.display_a = 1
        self.display_b = 1
        self.display_a_dev = 'N'
        self.display_b_dev = 'N'
        self.dc_bias = False
        self.zero_open = False
        self.zero_short = False
        self.average = False
        self.high_speed = False
        self.log_sweep = False
        self.sweep_mode = False
        self.circuit_mode = 1
        self.zy_range = 7
        self.trigger = 1
        self.data_ready = False
        self.data_format = 0


class HP4192A(Instrument):
    """ Represents the Hewlett Packard 4192A impedance analyzer
    and provides a high-level interface for interacting
    with the instrument.
    """

    def __init__(self, adapter, **kwargs):
        super(HP4192A, self).__init__(
            adapter,
            "Hewlett-Packard HP4192A",
            includeSCPI=False,
            send_end=True,
            read_termination="\r\n",
            **kwargs
        )
        self.settings = HP4192A_settings()
        # Send initial settings to the instrument
        # for attr in self.settings.__dict__:
        #    setattr(self, attr, getattr(self.settings, attr))

    # Because we need to track settings in self.settings, we need to override the setting
    # staticmethod from Instrument class
    @staticmethod
    def setting(set_command, docs, attr,
                validator=lambda x, y: x, values=(),
                set_process=lambda v: v, self_validator=None,
                **kwargs):
        """Returns a property for the class based on the supplied
        commands. This property may be set, but cannot be read from the instrument.
        This property returns the attribute of self.settings when queried for a setting
        :param set_command: A string command that writes the value
        :param docs: A docstring that will be included in the documentation
        :param attr: A string that is the name of the settings object attribute to be changed
        :param validator: A function that takes both a value and a group of valid values
        and returns a valid value, while it otherwise raises an exception
        :param values: A list, tuple, range, or dictionary of valid values, that can be used
        as to map values if :code:`map_values` is True.
        :param set_process: A function that takes a value and allows processing
        before value mapping, returning the processed value
        """

        def fget(self):
            return getattr(self.settings, attr)

        def fset(self, value):
            if self_validator:
                value = set_process(self_validator(self, value, values, validator))
            else:
                value = set_process(validator(value, values))
            command_str = set_command % str(value)
            self.write(command_str)
            setattr(self.settings, attr, value)

        # Add the specified document string to the getter
        fget.__doc__ = docs
        return property(fget, fset)

    @staticmethod
    def choices(mode):
        """ Convenience function to print out the choices for a mode.
        e.g. inst.choices(inst.ZY_RANGE)
        :param mode: mode to print out
        """
        modes = mode['modes']
        index = mode['idx']
        return [str(idx + index) + ': ' + i for idx, i in enumerate(modes)]

    data_ready = setting.__func__('D%s',
                                  """ Return 'Data Ready' status, this property can be set to True
                                    or False
                                    +--------+----------------------+
                                    | Value  | Status               | 
                                    +--------+----------------------+
                                    | True   | 'Data Ready' active  |
                                    +--------+----------------------+
                                    | False  | 'Data Ready' disabled|
                                    +--------+----------------------+
                                  """, attr='data_ready', set_process=lambda x: int(x),
                                  validator=strict_discrete_set,
                                  values=[0, 1])

    def display_validator(self, value, values, validator):
        if self.settings.display_a < 5:
            return validator(value, values)
        else:
            raise ValueError(
                """ZY RANGE commands cannot be used with Display A
                 A5, A6, and A7. Display Mode: %s""" % str(
                    self.settings.display_a))

    # ZY_RANGE is 1 indexed for commands  i.e. 1 - 8
    ZY_RANGE = {'modes': ['1 Ω / 10 s', '10 Ω / 1 s', '100 Ω / 100 ms', '1 kΩ / 10 ms',
                          '10 kΩ / 1 ms', '100 kΩ / 0.1 ms', '1 MΩ / 0.01 ms', 'auto'], 'idx': 1}
    zy_range = setting.__func__('R%s',
                                """ Return 'ZY RANGE' status, this property can be set
                                to the 1 indexed array ZY RANGE.
                                +--------+----------------------+
                                | Value  | Status               | 
                                +--------+----------------------+
                                | 1      | 1 Ω / 10 s           |
                                +--------+----------------------+
                                | 2      | 10 Ω / 1 s           |
                                +--------+----------------------+
                                | 3      | 100 Ω / 100 ms       |
                                +--------+----------------------+
                                | 4      | 1 kΩ / 10 ms         |
                                +--------+----------------------+
                                | 5      | 10 kΩ / 1 ms         |
                                +--------+----------------------+
                                | 6      | 100 kΩ / 0.1 ms      |
                                +--------+----------------------+
                                | 7      | 1 MΩ / 0.01 ms       |
                                +--------+----------------------+
                                | 8      | auto                 |
                                +--------+----------------------+
                                """, attr='zy_range', set_process=lambda x: int(x),
                                self_validator=display_validator,
                                validator=strict_range,
                                values=[1, 8])
    average = setting.__func__('V%s',
                               """Return 'Average' status, this property can be set to True 
                               or False
                               
                               +--------+----------------------+
                               | Value  | Status               | 
                               +--------+----------------------+
                               | True   | 'Average' active     |
                               +--------+----------------------+
                               | False  | 'Average' disabled   |
                               +--------+----------------------+
                               """, attr='average', set_process=lambda x: int(x),
                               validator=strict_discrete_set,
                               values=[0, 1])
    data_format = setting.__func__('F%s',
                                   """ Return 'Output Data Format' status, this property can be set
                                   to 0 or 1
                                   +--------+-------------------------------------+
                                   | Value  | Status                              | 
                                   +--------+-------------------------------------+
                                   | 0      | 'Output Data Format' Display A/B    |
                                   +--------+-------------------------------------+
                                   | 1      | 'Output Data Format' Display A/B/C  |
                                   +--------+-------------------------------------+
                                   """, attr='average', set_process=lambda x: int(x),
                                   validator=strict_discrete_set,
                                   values=[0, 1])
    # DISPLAY_A is 1 indexed for commands i.e. 1 - 7
    DISPLAY_A = {
        'modes': ['Z (abs impedance) / Y (abs admittance)', 'R (resistance) / G (conductance)',
                  'L (inductance)',
                  'C (capacitance)', 'B - A (dB)', 'A (dBm / dBV)', 'B (dBm / dBV)'], 'idx': 1}
    display_a = setting.__func__('A%s',
                                 """ Return 'Display A' status, this property can be set
                                 to the 1 indexed array DISPLAY_A.
                                 +--------+----------------------+
                                 | Value  | Status               | 
                                 +--------+----------------------+
                                 | 1      | Z / Y                |
                                 +--------+----------------------+
                                 | 2      | R / G                |
                                 +--------+----------------------+
                                 | 3      | L                    |
                                 +--------+----------------------+
                                 | 4      | C                    |
                                 +--------+----------------------+
                                 | 5      | B - A (dB)           |
                                 +--------+----------------------+
                                 | 6      | A (dBm / dBV)        |
                                 +--------+----------------------+
                                 | 7      | B (dBm / dBV)        |
                                 +--------+----------------------+
                                 """, attr='display_a', set_process=lambda x: int(x),
                                 validator=strict_range,
                                 values=[1, 7])
    # DISPLAY_B is 1 indexed for commands i.e. 1 - 7
    DISPLAY_B = {'modes': ['θ phase angle (degrees)', 'θ phase angle (radians)',
                           'X (reactance) / B (susceptance)',
                           'Q (quality factor)',
                           'D (dissipation factor', 'R (resistance) / G (conductance)',
                           'Group Delay'], 'idx': 1}
    display_b = setting.__func__('B%s',
                                 """ Return 'Display B' status, this property can be set
                                 as a secondary function mode of A
                                 +--------+--------+--------------+
                                 | Value  | A mode | Status       |
                                 +--------+--------+--------------+
                                 | 1      | 1      | θ (degrees)  |
                                 +--------+--------+--------------+
                                 | 2      | 1      | θ (radians)  |
                                 +--------+--------+--------------+
                                 | 1-3    | 2      | X / B        |
                                 +--------+--------+--------------+
                                 | 1      | 3 or 4 | Q            |
                                 +--------+--------+--------------+
                                 | 2      | 3 or 4 | D            |
                                 +--------+--------+--------------+
                                 | 3      | 3 or 4 | R / G        |
                                 +--------+--------+--------------+
                                 | 1      | 5      | Group Delay  |
                                 +--------+--------+--------------+
                                 | 1      | 5      | θ (degrees)  |
                                 +--------+--------+--------------+
                                 | 1      | 5      | θ (radians)  |
                                 +--------+--------+--------------+
                                 """, attr='display_b', set_process=lambda x: int(x),
                                 validator=strict_range,
                                 values=[1, 7])
    FUNCTION_MODES_VERBOSE = {
        'modes': OrderedDict(
            [('Z (abs impedance) / Y (abs admittance) | θ phase angle (degrees)', (1, 1)),
             ('Z (abs impedance) / Y (abs admittance) | θ phase angle (radians)', (1, 2)),
             ('R (resistance) / G (conductance) | X (reactance) / B (susceptance)', (2, 1)),
             ('L (inductance) | Q (quality factor)', (3, 1)),
             ('L (inductance) | D (dissipation factor', (3, 2)),
             ('L (inductance) | R (resistance) / G (conductance)', (3, 3)),
             ('C (capacitance) | Q (quality factor)', (4, 1)),
             ('C (capacitance) | D (dissipation factor', (4, 2)),
             ('C (capacitance) | R (resistance) / G (conductance)', (4, 3)),
             ('B - A (dB) | Group Delay', (5, 1)),
             ('B - A (dB) | θ phase angle (degrees)', (5, 2)),
             ('B - A (dB) | θ phase angle (radians)', (5, 3)),
             ('A (dBm / dBV)', (6, 1)),
             ('B (dBm / dBV)', (7, 1)),
             ]),
        'idx': 0}
    FUNCTION_MODES = {
        'modes': OrderedDict([('Z / Y | θ (degrees)', (1, 1)),
                              ('Z / Y | θ (radians)', (1, 2)),
                              ('R / G | X / B', (2, 1)),
                              ('L | Q', (3, 1)),
                              ('L | D', (3, 2)),
                              ('L | R / G', (3, 3)),
                              ('C | Q', (4, 1)),
                              ('C | D', (4, 2)),
                              ('C | R / G', (4, 3)),
                              ('B - A (dB) | Group Delay', (5, 1)),
                              ('B - A (dB) | θ (degrees)', (5, 2)),
                              ('B - A (dB) | θ (radians)', (5, 3)),
                              ('A (dBm / dBV)', (6, 1)),
                              ('B (dBm / dBV)', (7, 1)),
                              ]),
        'idx': 0}

    def set_mode(self, mode_idx):
        """Convenience function to set combinations of display_a and display_b
        :param mode_idx: Index of the selected mode from FUNCTION_MODES
        """
        mode_key = list(self.FUNCTION_MODES['modes'].keys())[mode_idx]
        mode = self.FUNCTION_MODES['modes'][mode_key]
        self.display_a = mode[0]
        self.display_b = mode[1]

    display_a_dev = setting.__func__('A%s',
                                     """ Return 'Deviation measurement' status for display A
                                     
                                     +--------+----------------------+
                                     | Value  | Status               | 
                                     +--------+----------------------+
                                     | N      | Off                  |
                                     +--------+----------------------+
                                     | D      | Delta                |
                                     +--------+----------------------+
                                     | P      | Delta percentage     |
                                     +--------+----------------------+
                                     """, attr='display_a_dev', set_process=lambda x: int(x),
                                     validator=strict_discrete_set,
                                     values=['N', 'D', 'P'])
    display_b_dev = setting.__func__('B%s',
                                     """ Return 'Deviation measurement' status for display B
                                     
                                     +--------+----------------------+
                                     | Value  | Status               | 
                                     +--------+----------------------+
                                     | N      | Off                  |
                                     +--------+----------------------+
                                     | D      | Delta                |
                                     +--------+----------------------+
                                     | P      | Delta percentage     |
                                     +--------+----------------------+
                                     """, attr='display_b_dev', set_process=lambda x: int(x),
                                     validator=strict_discrete_set,
                                     values=['N', 'D', 'P'])
    # CIRCUIT_MODE is 1 indexed for commands i.e. 1 - 3
    CIRCUIT_MODE = {
        'modes': ['AUTO', 'Series', 'Parallel'], 'idx': 1}
    circuit_mode = setting.__func__('C%s',
                                    """ Return 'CIRCUIT_MODE' status, this property can be set
                                    to the 1 indexed array CIRCUIT_MODE.
                                    +--------+----------------------+
                                    | Value  | Status               | 
                                    +--------+----------------------+
                                    | 1      | Auto                 |
                                    +--------+----------------------+
                                    | 2      | Series               |
                                    +--------+----------------------+
                                    | 3      | Parallel             |
                                    +--------+----------------------+
                                    """, attr='circuit_mode', set_process=lambda x: int(x),
                                    validator=strict_range,
                                    values=[1, 3])
    TRIGGER = {
        'modes': ['Internal', 'External', 'Hold / Manual'], 'idx': 1}
    trigger = setting.__func__('T%s',
                               """ Return 'TRIGGER' status, this property can be set
                               to the 1 indexed array TRIGGER.
                               +--------+----------------------+
                               | Value  | Status               | 
                               +--------+----------------------+
                               | 1      | Internal             |
                               +--------+----------------------+
                               | 2      | External             |
                               +--------+----------------------+
                               | 3      | Hold / Manual        |
                               +--------+----------------------+
                               """, attr='trigger', set_process=lambda x: int(x),
                               validator=strict_range,
                               values=[1, 3])
    osc_level = setting.__func__('OL%sEN',
                                 """ Return 'OSC level' status in volts, this property can be set
                                 as a float for OSC range.  Resolution is dependent
                                 on the set 'OSC level'
                                 +------------+----------------------+
                                 | OSC level  | 0.005 V - 1.100 V    | 
                                 +------------+----------------------+
                                 
                                 +-------------+-------------------------+
                                 | Resolution  | OSC level               |
                                 +-------------+-------------------------+
                                 | 0.001 V     | 0.005 V - 0.100 V       |
                                 +-------------+-------------------------+
                                 | 0.005 V     | 0.100 V - 1.100 V       |
                                 +-------------+-------------------------+
                                 """, attr='osc_level', set_process=lambda x: float(x),
                                 validator=strict_range,
                                 values=[.005, 1.100])
    spot_frequency = setting.__func__('FR%sEN',
                                      """ Return 'spot frequency' status in kilohertz, this property
                                      can be set as a float for OSC range
                                      Resolution is dependent on the set 'spot frequency'
                                      +-----------------+-----------------------------+
                                      | Spot frequency  | 0.0005 kHz - 13000.0 kHz    | 
                                      +-----------------+-----------------------------+
                                        
                                      +-------------+-------------------------+
                                      | Resolution  | Spot frequency          |
                                      +-------------+-------------------------+
                                      | 0.000001 kHz| 0.005 kHz - 9.999999 kHz|
                                      +-------------+-------------------------+
                                      | 0.00001  kHz| 10    kHz - 99.99999 kHz|
                                      +-------------+-------------------------+
                                      | 0.0001   kHz| 100   kHz - 999.9999 kHz|
                                      +-------------+-------------------------+
                                      | 0.001    kHz| 1000  kHz - 13000.00 kHz|
                                      +-------------+-------------------------+
                                      """, attr='spot_frequency', set_process=lambda x: float(x),
                                      validator=strict_range,
                                      values=[.0005, 13000.])
    sweep_mode = setting.__func__('W%s',
                                  """ Return 'Sweep Mode' status, this property can be set
                                  +--------+----------------------+
                                  | Value  | Status               | 
                                  +--------+----------------------+
                                  | 0      | Manual               |
                                  +--------+----------------------+
                                  | 1      | Auto                 |
                                  +--------+----------------------+
                                   """, attr='sweep_mode', set_process=lambda x: int(x),
                                  validator=strict_discrete_set,
                                  values=[0, 1])
    start_frequency = setting.__func__('TF%sEN',
                                       """ Return 'start frequency' status in kilohertz, this
                                       property can be set as a float for OSC range
                                       Resolution is dependent on the set 'start frequency'
                                       +-----------------+-----------------------------+
                                       | Start frequency | 0.0005 kHz - 13000.0 kHz    | 
                                       +-----------------+-----------------------------+
                                       
                                       +-------------+-------------------------+
                                       | Resolution  | Start frequency         |
                                       +-------------+-------------------------+
                                       | 0.000001 kHz| 0.005 kHz - 9.999999 kHz|
                                       +-------------+-------------------------+
                                       | 0.00001  kHz| 10    kHz - 99.99999 kHz|
                                       +-------------+-------------------------+
                                       | 0.0001   kHz| 100   kHz - 999.9999 kHz|
                                       +-------------+-------------------------+
                                       | 0.001    kHz| 1000  kHz - 13000.00 kHz|
                                       +-------------+-------------------------+
                                       """, attr='start_frequency', set_process=lambda x: float(x),
                                       validator=strict_range,
                                       values=[.0005, 13000.])
    end_frequency = setting.__func__('PF%sEN',
                                     """ Return 'end frequency' status in kilohertz, this property
                                      can be set as a float for OSC range
                                     Resolution is dependent on the set 'end frequency'
                                        +-----------------+-----------------------------+
                                        | End frequency   | 0.0005 kHz - 13000.0 kHz    | 
                                        +-----------------+-----------------------------+
                                        
                                        +-------------+-------------------------+
                                        | Resolution  | End frequency           |
                                        +-------------+-------------------------+
                                        | 0.000001 kHz| 0.005 kHz - 9.999999 kHz|
                                        +-------------+-------------------------+
                                        | 0.00001  kHz| 10    kHz - 99.99999 kHz|
                                        +-------------+-------------------------+
                                        | 0.0001   kHz| 100   kHz - 999.9999 kHz|
                                        +-------------+-------------------------+
                                        | 0.001    kHz| 1000  kHz - 13000.00 kHz|
                                        +-------------+-------------------------+
                                     """, attr='end_frequency', set_process=lambda x: float(x),
                                     validator=strict_range,
                                     values=[.0005, 13000.])
    step_frequency = setting.__func__('SF%sEN',
                                      """ Return 'step frequency' status in kilohertz, this property
                                       can be set as a float for OSC range
                                      Resolution is dependent on the set 'step frequency'
                                        +-----------------+-----------------------------+
                                        | Step frequency  | 0.0005 kHz - 13000.0 kHz    | 
                                        +-----------------+-----------------------------+
                                        
                                        +-------------+-------------------------+
                                        | Resolution  | Step frequency          |
                                        +-------------+-------------------------+
                                        | 0.000001 kHz| 0.005 kHz - 9.999999 kHz|
                                        +-------------+-------------------------+
                                        | 0.00001  kHz| 10    kHz - 99.99999 kHz|
                                        +-------------+-------------------------+
                                        | 0.0001   kHz| 100   kHz - 999.9999 kHz|
                                        +-------------+-------------------------+
                                        | 0.001    kHz| 1000  kHz - 13000.00 kHz|
                                        +-------------+-------------------------+
                                      """, attr='step_frequency', set_process=lambda x: float(x),
                                      validator=strict_range,
                                      values=[.0005, 13000.])
    spot_bias = setting.__func__('BI%sEN',
                                 """ Return 'spot bias' status in kilohertz, this property can be
                                 set as a float in bias voltage range
                                 +-----------------+-----------------------------+
                                 | Spot bias       | -35.0 V - +35.0 V           | 
                                 +-----------------+-----------------------------+
                                 
                                 +-------------+-------------------------+
                                 | Resolution  | Step bias               |
                                 +-------------+-------------------------+
                                 | 0.01     kHz| -35.0 V - +35.0 V       |
                                 +-------------+-------------------------+
                                 """, attr='spot_bias', set_process=lambda x: float(x),
                                 validator=strict_range,
                                 values=[-35.0, 35.0])
    start_bias = setting.__func__('TB%sEN',
                                  """ Return 'start bias' status in kilohertz, this property can
                                  be set as a float in bias voltage range
                                  +-----------------+-----------------------------+
                                  | Start bias      | -35.0 V - +35.0 V           | 
                                  +-----------------+-----------------------------+
                                    
                                  +-------------+-------------------------+
                                  | Resolution  | Start bias              |
                                  +-------------+-------------------------+
                                  | 0.01     kHz| -35.0 V - +35.0 V       |
                                  +-------------+-------------------------+
                                  """, attr='start_bias', set_process=lambda x: float(x),
                                  validator=strict_range,
                                  values=[-35.0, 35.0])
    end_bias = setting.__func__('PB%sEN',
                                """ Return 'end bias' status in kilohertz, this property can be set
                                as a float in bias voltage range
                                +-----------------+-----------------------------+
                                | End bias        | -35.0 V - +35.0 V           | 
                                +-----------------+-----------------------------+
                                
                                +-------------+-------------------------+
                                | Resolution  | End bias                |
                                +-------------+-------------------------+
                                | 0.01     kHz| -35.0 V - +35.0 V       |
                                +-------------+-------------------------+
                                """, attr='end_bias', set_process=lambda x: float(x),
                                validator=strict_range,
                                values=[-35.0, 35.0])
    log_sweep = setting.__func__('G%s',
                                 """ Return 'Log Sweep' status, this property can be set
                                        +--------+----------------------+
                                        | Value  | Status               | 
                                        +--------+----------------------+
                                        | 0      | Manual               |
                                        +--------+----------------------+
                                        | 1      | Auto                 |
                                        +--------+----------------------+
                                  """, attr='log_sweep', set_process=lambda x: int(x),
                                 validator=strict_discrete_set,
                                 values=[0, 1])
    manual_sweep = setting.__func__('W%s',
                                    """ Return 'Manual Sweep' status, this property can be set
                                        +--------+----------------------+
                                        | Value  | Status               | 
                                        +--------+----------------------+
                                        | 2      | Step up              |
                                        +--------+----------------------+
                                        | 4      | Step down            |
                                        +--------+----------------------+
                                     """, attr='manual_sweep', set_process=lambda x: int(x),
                                    validator=strict_discrete_set,
                                    values=[2, 4])
    dc_bias = setting.__func__('I%s',
                               """ Return 'dc_bias' status, this property can be set only to I0
                                       +--------+----------------------+
                                       | Value  | Status               | 
                                       +--------+----------------------+
                                       | 0      | Off                  |
                                       +--------+----------------------+
                                """, attr='dc_bias', set_process=lambda x: int(x),
                               self_validator=display_validator,
                               validator=strict_discrete_set,
                               values=[0, ])
    zero_open = setting.__func__('ZO%s',
                                 """ Return 'Zero Open' status, this property can be set
                                        +--------+----------------------+
                                        | Value  | Status               | 
                                        +--------+----------------------+
                                        | 0      | Off                  |
                                        +--------+----------------------+
                                        | 1      | On                   |
                                        +--------+----------------------+
                                  """, attr='zero_open', set_process=lambda x: int(x),
                                 validator=strict_discrete_set,
                                 self_validator=display_validator,
                                 values=[0, 1])
    zero_short = setting.__func__('ZS%s',
                                  """ Return 'Zero Short' status, this property can be set
                                        +--------+----------------------+
                                        | Value  | Status               | 
                                        +--------+----------------------+
                                        | 0      | Off                  |
                                        +--------+----------------------+
                                        | 1      | On                   |
                                        +--------+----------------------+
                                   """, attr='zero_short', set_process=lambda x: int(x),
                                  self_validator=display_validator, validator=strict_discrete_set,
                                  values=[0, 1])
    test_level_monitor = setting.__func__('T%s',
                                          """ Return 'Test Level Monitor' status, this property
                                          can be set
                                          +--------+----------------------+
                                          | Value  | Status               | 
                                          +--------+----------------------+
                                          | V      | Volts                |
                                          +--------+----------------------+
                                          | A      | Milliamp             |
                                          +--------+----------------------+
                                          """, attr='test_level_monitor',
                                          set_process=lambda x: int(x),
                                          self_validator=display_validator,
                                          validator=strict_discrete_set,
                                          values=['V', 'A'])
    high_speed = setting.__func__('H%s',
                                  """ Return 'High Speed' status, this property can be set
                                        +--------+----------------------+
                                        | Value  | Status               | 
                                        +--------+----------------------+
                                        | 0      | Off                  |
                                        +--------+----------------------+
                                        | 1      | On                   |
                                        +--------+----------------------+
                                   """, attr='high_speed', set_process=lambda x: int(x),
                                  validator=strict_discrete_set,
                                  values=[0, 1])
    self_test = setting.__func__('S%s',
                                 """ Return 'Self Test' status, this property can be set only to 1
                                        +--------+----------------------+
                                        | Value  | Status               |
                                        +--------+----------------------+
                                        | 1      | On                   |
                                        +--------+----------------------+
                                  """, attr='self_test', set_process=lambda x: int(x),
                                 validator=strict_discrete_set,
                                 values=[1, ])

    def sweep_abort(self):
        """
        Abort the current sweep
        """
        self.write('AB')

    def execute(self):
        """
        Execute the current command
        """
        self.write('EX')

    def interpret_output(self, output):
        """
        Intrepet the output string from the HP4192A, which includes
        letter codes and measurement values
        e.g. NZFN+02.817E+03
        :param output: Output from HP4192A
        :return: Tuple of (float(value), code)
        """
        valid = re.match(r'([A-Z]+)([+-][0-9.]+)(E[+-][0-9.]+)*', output)
        if valid is not None and len(valid.groups()) > 1:
            code = valid.groups()[0]
            value = valid.groups()[1]
            value_exponent = valid.groups()[2]
            if value_exponent is not None:
                value += value_exponent
            return (float(value), code)
        else:
            raise ValueError('Invalid interpretation of output: %s' % output)

    def execute_read(self):
        """
        Execute and read output from instrument
        """
        result_split = self.ask('EX').split(',')
        if 1 < len(result_split) < 4:
            # self.data_format = 0
            # NZFN+02.817E+03,NTDN-000.03E+00
            # self.data_format = 1
            # NZFN+02.817E+03,NTDN-000.03E+00,K+01.000000
            return [self.interpret_output(i) for i in result_split]
        else:
            raise ValueError('Invalid output format from instrument: %s' % result_split)

    def reset(self):
        """
        Initatiates a reset (like a power-on reset) of the HP4192A
        """
        self.adapter.connection.clear()

    def shutdown(self):
        """
        Provides a way to gracefully close the connection to the HP4192A
        Abort any sweep and then clear and close VISA connection
        """
        self.sweep_abort()
        self.adapter.connection.clear()
        self.adapter.connection.close()
        super().shutdown()
