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

import numpy as np
from time import sleep

from pymeasure.instruments import Instrument
from pymeasure.instruments.validators import strict_discrete_set

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


def trigger_process(value, values):
    """ Provides a validator function that returns the value
    if it is in the discrete set. Otherwise it raises a ValueError.

    :param value: A value to test
    :param values: A set of values that are valid
    :raises: ValueError if the value is not in the set
    """

    if value in values:
        return value
    else:
        raise ValueError('Value of {} is not in the discrete set {}'.format(
            value, values
        ))


class Channel:
    """ Implementation of a Keysight DSO1052B Oscilloscope channel.

    Implementation modeled on Channel object of Keysight DSOX1102G instrument. """

    BOOLS = {True: 1, False: 0}

    def __init__(self, instrument, number):
        self.instrument = instrument
        self.number = number

    def values(self, command, **kwargs):
        """ Reads a set of values from the instrument through the adapter,
        passing on any key-word arguments.
        """
        return self.instrument.values(":channel%d:%s" % (
            self.number, command), **kwargs)

    def ask(self, command):
        self.instrument.ask(":channel%d:%s" % (self.number, command))

    def write(self, command):
        self.instrument.write(":channel%d:%s" % (self.number, command))

    def setup(self, bwlimit=None, coupling=None, display=None, invert=None, offset=None,
              probe_attenuation=None, scale=None):
        """ Setup channel. Unspecified settings are not modified. Modifying values such as
        probe attenuation will modify offset, range, etc. Refer to oscilloscope documentation and
        make multiple consecutive calls to setup() if needed.

        :param bwlimit: A boolean, which enables 25 MHz internal low-pass filter.
        :param coupling: "ac" or "dc".
        :param display: A boolean, which enables channel display.
        :param invert: A boolean, which enables input signal inversion.
        :param offset: Numerical value represented at center of screen, must be inside
            the legal range.
        :param probe_attenuation: Probe attenuation values from 0.1 to 1000.
        :param scale: Units per division. """

        if probe_attenuation is not None:
            self.probe_attenuation = probe_attenuation
        if bwlimit is not None:
            self.bwlimit = bwlimit
        if coupling is not None:
            self.coupling = coupling
        if display is not None:
            self.display = display
        if invert is not None:
            self.invert = invert
        if offset is not None:
            self.offset = offset
        if scale is not None:
            self.scale = scale

    bwlimit = Instrument.control(
        "BWLimit?", "BWLimit %d",
        """ A boolean parameter that toggles 25 MHz internal low-pass filter.""",
        validator=strict_discrete_set,
        values=BOOLS,
        map_values=True
    )

    coupling = Instrument.control(
        "COUPling?", "COUPling %s",
        """ A string parameter that determines the coupling. 
        Values can be "ac" or "dc" or "gnd".
        """,
        validator=strict_discrete_set,
        values={"ac": "AC", "dc": "DC", "gnd": "GND"},
        map_values=True
    )

    display = Instrument.control(
        "DISPlay?", "DISPlay %d",
        """ A boolean parameter that toggles the display.""",
        validator=strict_discrete_set,
        values=BOOLS,
        map_values=True
    )

    invert = Instrument.control(
        "INVert?", "INVert %d",
        """ A boolean parameter that toggles the inversion of the input signal.""",
        validator=strict_discrete_set,
        values=BOOLS,
        map_values=True
    )

    memory_depth = Instrument.control(
        "MEMoryDepth?", "",
        """ A query returns the number of samples in
        memory for the selected channel.
        """
    )

    offset = Instrument.control(
        "OFFSet?", "OFFSet %f",
        """ A float parameter to set value that is represented at center of screen in
        Volts. The range of legal values varies depending on range and scale. If the specified
        value is outside of the legal range, the offset value is automatically set to the nearest
        legal value.
        """
    )

    probe_attenuation = Instrument.control(
        "PROBe?", "PROBe %fX",
        """ A float parameter that specifies the probe attenuation factor for the
        selected channel. The probe attenuation factor may be 0.001X, 0.01X, 0.1X, 1X,
        10X, 100X, or 1000X. This command does not change the actual input sensitivity
        of the oscilloscope. It changes the reference constants for scaling the display
        factors, for making automatic measurements, and for setting trigger levels.
        """,
        validator=strict_discrete_set,
        values=[0.001, 0.01, 0.1, 1, 10, 100, 1000]
    )

    scale = Instrument.control(
        "SCALe?", "SCALe %f",
        """ A float parameter that specifies the vertical scale, or units per division, in Volts."""
    )

    units = Instrument.control(
        "UNITs?", "UNITs %d",
        """ Sets the measurement units for the channel's connected probe. 
        Values can be "volts", "amps", "watts", or "unknown".
        """,
        validator=strict_discrete_set,
        values={"volts": "VOLTs", "amps": "AMPeres", "watts": "WATTs", "unknown": "UNKNown"},
        map_values=True
    )

    vernier = Instrument.control(
        "VERNier?", "VERNier %d",
        """ Turns a channel's vernier (fine vertical adjustment) on or off """,
        validator=strict_discrete_set,
        values=BOOLS,
        map_values=True
    )


class KeysightDSO1052B(Instrument):
    """ Represents the Keysight DSO1052B Oscilloscope interface for interacting
    with the instrument.

    Refer to the Keysight DSO1052B Oscilloscope Programmer's Guide for further details about
    using the lower-level methods to interact directly with the scope.

    .. code-block:: python

        scope = DSO1052B(resource)
        scope.autoscale()
        ch1_data_array, ch1_preamble = scope.download_data(source="channel1", points=2000)
        # ...
        scope.shutdown()
    """

    BOOLS = {True: 1, False: 0}

    def __init__(self, adapter, **kwargs):
        super().__init__(
            adapter, "Keysight DSO1052B Oscilloscope", **kwargs
        )
        # Account for setup time for timebase_mode, waveform_points_mode
        # self.adapter.connection.timeout = 6000
        self.ch1 = Channel(self, 1)
        self.ch2 = Channel(self, 2)

    #################
    # Channel setup #
    #################

    def autoscale(self):
        """ Autoscale displayed channels. """
        self.write(":autoscale")

    ##################
    # Timebase Setup #
    ##################

    @property
    def timebase(self):
        """
        Reads setup data from timebase and converts it to a more convenient dict of values.
        """
        tb_setup_raw = self.ask(":timebase?").strip("\n")

        # tb_setup_raw hat the following format:
        # :TIM:MODE MAIN;REF CENT;MAIN:RANG +1.00E-03;POS +0.0E+00

        # Cut out the ":TIM:" at beginning and split string
        tb_setup_splitted = tb_setup_raw[5:].split(";")

        # Create dict of setup parameters
        tb_setup = dict(map(lambda v: v.split(" "), tb_setup_splitted))

        # Convert values to specific type
        to_str = ["MODE", "REF"]
        to_float = ["MAIN:RANG", "POS"]
        for key in tb_setup:
            if key in to_str:
                tb_setup[key] = str(tb_setup[key])
            elif key in to_float:
                tb_setup[key] = float(tb_setup[key])

        return tb_setup

    timebase_delay_offset = Instrument.control(
        ":TIMebase:DELayed:OFFset?", ":TIMebase:DELayed:OFFset %f",
        """ A float that sets the horizontal position in the
        zoomed view of the main sweep. The main sweep scale and the main sweep
        horizontal position determine the range for this command. The value for this
        command must keep the zoomed view window within the main sweep range.
        """
    )

    timebase_delay_scale = Instrument.control(
        ":TIMebase:DELayed:SCALe?", ":TIMebase:DELayed:SCALe %f",
        """ A float that sets the zoomed window horizontal
        scale (seconds/division). The main sweep scale determines the range for this
        command. The maximum value is equal to the :TIMebase[:MAIN]:SCALe value.
        """
    )

    timebase_format = Instrument.control(
        ":TIMebase:FORMat?", ":TIMebase:FORMat %s",
        """ A string parameter that sets the current time base format. Can be 
        "yt" (default), "xy", or "roll".""",
        validator=strict_discrete_set,
        values={"yt": "YT", "xy": "XY", "roll": "ROLL"},
        map_values=True
    )

    timebase_offset = Instrument.control(
        ":TIMebase:OFFset?", ":TIMebase:OFFset %f",
        """ A float parameter that sets the time interval in seconds between the trigger
        event and the reference position (at center of screen by default)."""
    )

    timebase_scale = Instrument.control(
        ":TIMebase:SCALe?", ":TIMebase:SCALe %f",
        """ A float parameter that sets the horizontal scale (units per division) in seconds
        for the main window."""
    )

    timebase_mode = Instrument.control(
        ":TIMebase:MODE?", ":TIMebase:MODE %s",
        """ A string parameter that sets the current time base. Can be "main" (default) or 
        "delayed".""",
        validator=strict_discrete_set,
        values={"main": "MAIN", "delayed": "DELayed"},
        map_values=True
    )

    ###############
    #   Trigger   #
    ###############

    trigger_coupling = Instrument.control(
        ":TRIGger:COUPling?", ":TRIGger:COUPling %s",
        """ A string parameter that sets the input coupling for the selected trigger
        sources. The coupling can be:
        'dc' sets the input coupling to DC.
        'ac' sets the input coupling to AC (50 Hz cutoff).
        'lf' sets the input coupling to low frequency reject (100 kHz cutoff).
        """,
        validator=strict_discrete_set,
        values={"ac": "AC", "dc": "DC", "lf": "LF"},
        map_values=True
    )

    trigger_hf = Instrument.control(
        ":TRIGger:HFREject?", ":TRIGger:HFREject %d",
        """ A string parameter that turns the high frequency reject filter on or off.
        """,
        validator=strict_discrete_set,
        values=BOOLS,
        map_values=True
    )

    trigger_hold = Instrument.control(
        ":TRIGger:HOLDoff?", ":TRIGger:HOLDoff %d",
        """ A float parameter that defines the holdoff time value in seconds.
        Holdoff keeps a trigger from occurring until after a certain amount of time has
        passed since the last trigger.
        """
    )

    trigger_mode = Instrument.control(
        ":TRIGger:MODE?", ":TRIGger:MODE %s",
        """ A string parameter that selects the trigger mode (trigger type).
        """,
        validator=strict_discrete_set,
        values={"edge": "EDGE", "pulse": "PULSE", "video": "VIDEO", "pattern": "PATTERN",
                "alt": "ALTERNATION"},
        map_values=True
    )

    trigger_sensitivity = Instrument.control(
        ":TRIGger:SENSitivity?", ":TRIGger:SENSitivity %d",
        """ A float parameter that sets the trigger sensitivity value.
        Trigger sensitivity specifies the vertical change that must occur in order for a
        trigger to be recognized.
        """
    )

    trigger_status = Instrument.control(
        ":TRIGger:STATus?", "",
        """ A query that returns the current trigger/acquisition status
        """
    )

    trigger_edge_slope = Instrument.control(
        ":TRIGger:EDGE:SLOPe?", ":TRIGger:EDGE:SLOPe %s",
        """ A string parameter that selects the trigger edge slope mode.
        """,
        validator=strict_discrete_set,
        values={"neg": "NEGative", "pos": "POSITIVE", "alt": "ALTernation"},
        map_values=True
    )

    @property
    def trigger_source(self):
        return self.ask(":TRIGger:" + self.trigger_mode + ":SOURce?")

    @trigger_source.setter
    def trigger_source(self, channel):
        """ Set trigger source for current mode"""
        self.write(":TRIGger:" + self.trigger_mode + ":SOURce " + channel)

    @property
    def trigger_level(self):
        return self.ask(":TRIGger:" + self.trigger_mode + ":LEVel?")

    @trigger_level.setter
    def trigger_level(self, level):
        """ Set trigger source for current mode"""
        self.write(":TRIGger:" + self.trigger_mode + ":LEVel " + level)

    @property
    def trigger_sweep(self):
        """ Get trigger sweep for current mode
        Only edge, pattern, pulse, video, no alt
        """
        mode = self.trigger_mode.upper()
        if strict_discrete_set(mode, ["EDGE", "PULSE", "VIDEO", "PATTERN", ]):
            return self.ask(":TRIGger:" + mode + ":SWEep?")

    @trigger_sweep.setter
    def trigger_sweep(self, sweep):
        """ Set trigger sweep for current mode
        Only edge, pattern, pulse, video, no alt
        """
        mode = self.trigger_mode.upper()
        if strict_discrete_set(mode, ["EDGE", "PULSE", "VIDEO", "PATTERN", ]):
            self.write(":TRIGger:" + mode + ":SWEep " + sweep)

    ###############
    # Acquisition #
    ###############

    def run(self):
        """ Starts repetitive acquisitions.

        This is the same as pressing the Run key on the front panel.
        """
        self.write(":run")

    def stop(self):
        """  Stops the acquisition. This is the same as pressing the Stop key on the front panel."""
        self.write(":stop")

    def single(self):
        """ Causes the instrument to acquire a single trigger of data.
        This is the same as pressing the Single key on the front panel. """
        self.write(":single")

    acquisition_type = Instrument.control(
        ":ACQuire:TYPE?", ":ACQuire:TYPE %s",
        """ A string parameter that sets the type of data acquisition. Can be "normal", "average",
        or "peak".""",
        validator=strict_discrete_set,
        values={"normal": "NORMal", "average": "AVERage", "peak": "PEAKdetect"},
        map_values=True
    )

    acquisition_mode = Instrument.control(
        ":ACQuire:MODE?", "",
        """ A string parameter that queries the acquisition mode.""",
    )

    acquisition_rate = Instrument.control(
        ":ACQuire:SRATe?", "",
        """ A string parameter that queries the acquisition sample rate.""",
    )

    acquisition_averages = Instrument.control(
        ":ACQuire:AVERages?", ":ACQuire:AVERages %d",
        """ An integer parameter that sets the number of averages when in the
        waveform averaging mode (set by the :ACQuire:TYPE AVERage command).""",
        validator=strict_discrete_set,
        values=[2, 4, 8, 16, 32, 64, 128, 256],
    )

    waveform_points_mode = Instrument.control(
        ":WAVeform:POINts:MODE?", ":WAVeform:POINts:MODE %s",
        """ A string parameter that sets the data record to be transferred with the waveform_data
         method. Can be "normal", "maximum", or "raw".""",
        validator=strict_discrete_set,
        values={"normal": "NORMal", "maximum": "MAXimum", "raw": "RAW"},
        map_values=True
    )
    waveform_points = Instrument.control(
        ":WAVeform:POINts?", ":WAVeform:POINts %d",
        """ An integer parameter that sets the number of waveform points to be transferred with
        the waveform_data method.
        In NORMAL mode the number of points can be between 1-600.
        In RAW mode the number of points can be between 1-20480.

        Note that the oscilloscope may provide less than the specified number of points. """,
    )
    waveform_source = Instrument.control(
        ":WAVeform:SOURce?", ":WAVeform:SOURce %s",
        """ A string parameter that selects the analog channel, function, or reference waveform
        to be used as the source for the waveform methods. Can be "channel1", "channel2",
        and "math".""",
        validator=strict_discrete_set,
        values={"channel1": "CHANnel1", "channel2": "CHANnel2", "math": "MATH", },
        map_values=True
    )
    waveform_format = Instrument.control(
        ":WAVeform:FORMat?", ":WAVeform:FORMat %s",
        """ A string parameter that controls how the data is formatted when sent from the
        oscilloscope. Can be "ascii", "word" or "byte". Words are transmitted in big endian by
        default.""",
        validator=strict_discrete_set,
        values={"ascii": "ASCII", "word": "WORD", "byte": "BYTE"},
        map_values=True
    )

    @property
    def waveform_preamble(self):
        """
        Reads waveform preamble and converts it to a more convenient dict of values:
            - "format": byte, word, or ascii (str)
            - "type": normal, peak detect, or average (str)
            - "points": nb of data points transferred (int)
            - "count": always 1 (int)
            - "xincrement": time difference between data points (float)
            - "xorigin": first data point in memory (float)
            - "xreference": data point associated with xorigin (int)
            - "yincrement": voltage difference between data points (float)
            - "yorigin": voltage at center of screen (float)
            - "yreference": data point associated with yorigin (int)
        """
        vals = self.values(":WAVeform:PREamble?")
        # Get values to dict
        vals_dict = dict(zip(["format", "type", "points", "count", "xincrement", "xorigin",
                              "xreference", "yincrement", "yorigin", "yreference"], vals))
        # Map element values
        format_map = {0: "BYTE", 1: "WORD", 2: "ASCII"}
        type_map = {0: "NORMAL", 1: "PEAK DETECT", 2: "AVERAGE"}
        vals_dict["format"] = format_map[int(vals_dict["format"])]
        vals_dict["type"] = type_map[int(vals_dict["type"])]

        # Correct types
        to_int = ["points", "count", "xreference", "yreference"]
        to_float = ["xincrement", "xorigin", "yincrement", "yorigin"]
        for key in vals_dict:
            if key in to_int:
                vals_dict[key] = int(vals_dict[key])
            elif key in to_float:
                vals_dict[key] = float(vals_dict[key])

        return vals_dict

    @property
    def waveform_data(self, delay=2):
        """ Get the binary block of sampled data points transmitted using the IEEE 488.2 arbitrary
        block data format."""
        # Other waveform formats raise UnicodeDecodeError
        # To give the oscilloscope time to ready large amounts of data, like after a
        # :WAVeform:DATA? query, you need to insert a delay between the query write and
        # the data read
        sleep(delay)

        self.waveform_format = "ascii"

        data = self.values(":waveform:data?")
        # Strip header from first data element
        data[0] = float(data[0][10:])

        return data

    ################
    # System Setup #
    ################

    @property
    def system_setup(self):
        """ A string parameter that sets up the oscilloscope. Must be in IEEE 488.2 format.
        It is recommended to only set a string previously obtained from this command."""
        return self.ask(":SYSTem:SETup?")

    @system_setup.setter
    def system_setup(self, setup_string):
        self.write(":SYSTem:SETup " + setup_string)

    def ch(self, channel_number):
        if channel_number == 1:
            return self.ch1
        elif channel_number == 2:
            return self.ch2
        else:
            raise ValueError("Invalid channel number. Must be 1 or 2.")

    def clear_status(self):
        """ Clear device status. """
        self.write("*CLS")

    def factory_reset(self):
        """ Factory default setup, no user settings remain unchanged.
         Settings:
         - acquisition_mode = 'normal'
         - ch1.display = True
         - ch1.offset = 0.0
         - ch1.coupling = 'dc'
         - ch1.probe_attenuation = 10
         - ch1.invert = False
         - ch1.bwlimit = False
         - ch1.units = 'volts'
         - ch1.scale = 100
         - ch2.display = False
         - waveform_source = 'channel1'
         - timebase_mode = 'main'
         - timebase_format = 'yt'
         - timebase_offset = 0.0
         - timebase_delay_offset = 0.0
         - timebase_scale = .00001
         - timebase_delay_scale = .0005
         - trigger_mode = 'edge'
         - trigger_coupling = 'dc'
         - trigger_edge_source = 'channel1'

         """
        self.write("*RST")

    def default_setup(self):
        """ Default setup, some user settings (like preferences) remain unchanged. """
        self.write(":SYSTem:PRESet")

    def timebase_setup(self, mode=None, offset=None, scale=None):
        """ Set up timebase. Unspecified parameters are not modified. Modifying a single parameter
        might impact other parameters. Refer to oscilloscope documentation and make multiple
        consecutive calls to channel_setup if needed.

        :param mode: Timebase mode, can be "yt", "xy", or "roll".
        :param offset: Offset in seconds between trigger and center of screen.
        :param scale: Units-per-division in seconds."""

        if mode is not None:
            self.timebase_mode = mode
        if offset is not None:
            self.timebase_offset = offset
        if scale is not None:
            self.timebase_scale = scale

    def download_image(self, format_="png", color_palette="color"):
        """ Get image of oscilloscope screen in bytearray of specified file format.

        :param format_: "bmp", "bmp8bit", or "png"
        :param color_palette: "color" or "grayscale"
        """
        query = f":DISPlay:DATA? {format_}, {color_palette}"
        # Using binary_values query because default interface does not support binary transfer
        img = self.binary_values(query, header_bytes=10, dtype=np.uint8)
        return bytearray(img)

    def download_data(self, source, waveform_mode = "normal", points=62500):
        """ Get data from specified source of oscilloscope. Returned objects are a np.ndarray of
        data values (no temporal axis) and a dict of the waveform preamble, which can be used to
        build the corresponding time values for all data points.

        Multimeter will be stopped for proper acquisition.

        :param source: measurement source, can be "channel1", "channel2", "math".
        :param waveform_mode: waveform_data data mode. Can be "normal", "maximum", or "raw"
        :param points: integer number of points to acquire.

        :return data_ndarray, waveform_preamble_dict: see waveform_preamble property for dict
            format.
        """
        # TODO: Consider downloading from multiple sources at the same time.
        self.waveform_source = source
        self.waveform_points_mode = waveform_mode
        self.waveform_points = points

        preamble = self.waveform_preamble
        data_bytes = self.waveform_data
        return np.array(data_bytes), preamble
