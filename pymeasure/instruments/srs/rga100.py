#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2024 PyMeasure Developers
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

import struct
import numpy as np

from pymeasure.instruments import Instrument
from pymeasure.instruments.validators import strict_range, strict_discrete_range, \
    strict_discrete_set


class RGA100(Instrument):
    # Upper mass limit depends on RGA model, for RGA100 the man mass limit is 100
    MASS_LIMIT = 100

    def __init__(self, adapter, name="Stanford Research Systems RGA100 Residual Gas Analyzer",
                 **kwargs):
        super().__init__(
            adapter,
            name,
            includeSCPI=False,
            asrl={'baud_rate': 28800, 'write_termination': '\r', 'read_termination': '\n\r'},
            **kwargs
        )

    def error_checking(self):
        # error = int(self.ask('ER?'))
        # 0: com - EC?
        # 1: filament - EF?
        # 2: not used
        # 3: electron multiplier - EM?
        # 4: quad mass filter - EQ?
        # 5: electrometer - ED?
        # 6: 24 V psu - EP?
        # dev_error_map = {0: 'EC?'}
        return []

    def check_get_errors(self):
        return []

    def check_set_errors(self):
        return []

    id = Instrument.measurement(
        "ID?",
        """Get the instrument model, firmware version, and serial number.""",
        cast=str,
        check_get_errors=True,
    )

    cdem_available = Instrument.measurement(
        "MO?",
        """Get electron multiplier availability.""",
        cast=bool,
        check_get_errors=True,
    )

    analog_points = Instrument.measurement(
        "AP?",
        """Get the total number of ion currents that will be measured and transmitted during an
        analog scan.""",
        check_get_errors=True,
        cast=int
    )

    histogram_points = Instrument.measurement(
        "HP?",
        """Get the total number of ion currents that will be measured and transmitted during a
         histogram scan.""",
        check_get_errors=True,
    )

    degas_ionizer = Instrument.setting(
        "DG%d",
        """Controls the degas time of the ionizer. Must be an integer. """,
        validator=lambda v, vs: strict_discrete_range(v, vs, 1),
        values=(0, 20),
        check_set_errors=True,
    )

    electron_energy = Instrument.control(
        "EE?", "EE%d",
        """Control the electron energy of the ionizer. The units are in electron volts (eV). Values
         must be an integer.""",
        validator=lambda v, vs: strict_discrete_range(v, vs, 1),
        values=(25, 105),
        cast=int,
        check_set_errors=True,
        check_get_errors=True,
    )

    filament_emission = Instrument.control(
        "FL?", "FL%.2f",
        """Control the filament electron emission current of the instrument. The heater is activated
         until current is achieved. The units are in milliamps (mA).""",
        validator=strict_range,
        values=(0.02, 3.5),
        # check_set_errors=True,
        # check_get_errors=True,
    )

    ion_energy = Instrument.control(
        "IE?", "IE%d",
        """Control the ion energy of the instrument. The units are in electron volts (eV) and values
         are either 8eV or 12eV.""",
        validator=strict_discrete_set,
        map_values=True,
        values={0: 8, 1: 12},
        cast=int,
        check_set_errors=True,
        check_get_errors=True,
    )

    focus_voltage = Instrument.control(
        "VF?", "VF%d",
        """Control th   e focus plate voltage of the instrument. The units are in volts (V).
        The value represents the magnitude of the biasing voltage (negative).""",
        validator=lambda v, vs: strict_discrete_range(v, vs, 1),
        values=(0, 155),
        cast=int,
        check_set_errors=True,
        check_get_errors=True,
    )

    electron_high_voltage = Instrument.control(
        "HV?", "HV%d",
        """Control the negative high voltage across the electron multiplier.
        The units are in volts (V).
        The value represents the magnitude of the biasing voltage (negative).""",
        validator=lambda v, vs: strict_discrete_range(v, vs, 1),
        values=(10, 2490),
        cast=int,
        check_set_errors=True,
        check_get_errors=True,
    )

    noise_floor = Instrument.control(
        "NF?", "NF%d",
        """Control the electrometer's noise floor setting.""",
        validator=lambda v, vs: strict_discrete_range(v, vs, 1),
        values=(0, 7),
        cast=int,
        check_set_errors=True,
        check_get_errors=True,
    )

    final_mass_spectra = Instrument.control(
        "MF?", "MF%d",
        """Final Mass (amu) of mass spectra (Analog and Histogram).""",
        validator=lambda v, vs: strict_discrete_range(v, vs, 1),
        values=(1, MASS_LIMIT),
        cast=int,
        check_set_errors=True,
        check_get_errors=True,
    )

    initial_mass_spectra = Instrument.control(
        "MI?", "MI%d",
        """Initial Mass (amu) of mass spectra (Analog and Histogram).""",
        validator=lambda v, vs: strict_discrete_range(v, vs, 1),
        values=(1, MASS_LIMIT),
        cast=int,
        check_set_errors=True,
        check_get_errors=True,
    )

    analog_scan_steps = Instrument.control(
        "SA?", "SA%d",
        """Set the number of steps executed per amu of analog scan. The parameter
        specifies the number of steps-per-amu""",
        validator=lambda v, vs: strict_discrete_range(v, vs, 1),
        values=(10, 25),
        cast=int,
        check_set_errors=True,
        check_get_errors=True,
    )

    ion_current = Instrument.measurement(
        "TP?",
        """Measure ion current (Total Pressure measurement)""",
        check_get_errors=True,

    )

    enable_total_pressure = Instrument.setting(
        "TP%d",
        """The response of the RGA to a Total Pressure measurement
        request depends on the status of TP_Flag at the time the measurement is
        requested""",
        validator=strict_discrete_set,
        values={0: False, 1: True},
        check_set_errors=True
    )

    stored_multiplier_gain = Instrument.control(
        "MG?", "MG%.4f",
        """Set value of electron multiplier (CDEM) Gain, expressed in units of
        thousands, in the non-volatile memory of the RGA head.""",
        validator=strict_range,
        values=(0, 2000),
        check_set_errors=True,
        check_get_errors=True,
    )

    stored_multiplier_bias = Instrument.control(
        "MV?", "MV%d",
        """Set the value of electron multiplier (CDEM) Gain, expressed in units of
        thousands, in the non-volatile memory of the RGA head.""",
        validator=lambda v, vs: strict_discrete_range(v, vs, 1),
        values=(0, 2490),
        cast=int,
        check_set_errors=True,
        check_get_errors=True,
    )

    stored_partial_pressure = Instrument.control(
        "SP?", "SP%.4f",
        """Set value of Partial Pressure Sensitivity, expressed in units of mA/Torr, in
        the non-volatile memory of the SRS RGA head.""",
        validator=strict_range,
        values=(0, 10),
        check_set_errors=True,
        check_get_errors=True,
    )

    stored_total_pressure = Instrument.control(
        "ST?", "ST%.4f",
        """Set value of Total Pressure Sensitivity, expressed in units of mA/Torr, in the
        non-volatile memory of the SRS RGA head.""",
        validator=strict_range,
        values=(0, 100),
        check_set_errors=True,
        check_get_errors=True,
    )

    def mass_filter_passband(self, mass):
        """Activate the quadrupole mass filter (QMF) and center its pass-band at the mass
        value specified by the parameter. The QMF is parked at the mass requested but
        no ion current measurements take place.
        The parameter is a real number and the mass increments are limited to a
        minimum value of 1/256 amu."""
        if strict_range(0.004, self.MASS_LIMIT):
            self.write('ML%.4f' % mass)

    def disable_mass_filter_passband(self):
        """The RF/DC voltages are completely shut down and no measurement is
        performed (no ion current is transmitted back to the host computer).
        Use this command format at the end of a set of single mass measurements to
        make sure the RF/DC are completely turned off."""
        self.write('ML0')

    def single_mass_measurement(self, mass):
        """Execute a single ion current measurement at a specified mass setting. The
        parameter is the integer mass number (mass-to-charge ratio in amu units) at
        which the measurement is performed."""
        if isinstance(mass, int) and 1 <= mass <= self.MASS_LIMIT:
            self.write('MR%d' % mass)

    def disable_mass_measurement(self):
        """The RF/DC voltages are completely shut down and no measurement is
        performed (no ion current is transmitted back to the host computer).
        Use this command format at the end of a set of single mass measurements to
        make sure the RF/DC are completely turned off."""
        self.write('MR0')

    # HISTOGRAM SCANNING
    def trigger_histogram_continuous(self):
        """Execute one or multiple Histogram Scans under the present scan conditions.
        The scan parameter can be set for single, ie and continuous scanning
        operation."""
        self.write('HS')

    # HISTOGRAM SCANNING
    def trigger_histogram_scan(self, scan_count):
        """Execute one or multiple Histogram Scans under the present scan conditions.
        The scan parameter can be set for single, multiple and continuous scanning
        operation."""
        if isinstance(scan_count, int) and 1 <= scan_count <= 255:
            self.write('HS%d' % scan_count)

    # HISTOGRAM SCANNING
    def interrupt_histogram_scan(self):
        self.write('HS0')

    # ANALOG SCANNING
    def trigger_analog_continuous(self):
        """Execute one or multiple Histogram Scans under the present scan conditions.
        The scan parameter can be set for single, multiple and continuous scanning
        operation."""
        self.write('SC')

    # ANALOG SCANNING
    def trigger_analog_scan(self, scan_count):
        """Execute one or multiple Histogram Scans under the present scan conditions.
        The scan parameter can be set for single, multiple and continuous scanning
        operation."""
        if isinstance(scan_count, int) and 1 <= scan_count <= 255:
            self.write('SC%d' % scan_count)

    def analog_scan(self):
        scale_factor = 1e-13 / self.stored_partial_pressure
        step = 1.0 / self.analog_scan_steps
        points = self.analog_points
        # scan count 1-255
        self.trigger_analog_scan(1)
        data = []
        for i in range(points):
            # read integer
            point = struct.unpack('<i', self.read_bytes(4))[0]
            data.append(point * scale_factor)

        mass_axis = np.arange(self.initial_mass_spectra, self.final_mass_spectra + step / 2.0, step)
        return [data, mass_axis]

    def mass_count(self, data):
        pass

    # ANALOG SCANNING
    def interrupt_analog_scan(self):
        self.write('SC')

    def calibrate_instrument(self):
        """Readjust the zero of the ion detector under the present detector settings, and
        correct the internal scan parameters against small temperature fluctuations to
        assure that the correct RF voltages (i.e. as specified by the last Peak Tuning
        procedure) are programmed on the QMF rods as a function of mass."""
        self.write('CA')

    def calibrate_electrometer(self):
        """Perform a complete calibration of the electrometer’s I-V response."""
        self.write('CL')

    def disable_electron_multiplier(self):
        """The Electron Multiplier is turned off and the Faraday Cup (FC) Detection is enabled."""
        self.write('HV0')

    def disable_filament(self):
        """The filament is turned off and the repeller grid and the focus plate are
        grounded."""
        self.write('FL0.00')

    def clear_buffers(self):
        """The IN0 command clears all the RGA’s RS232 buffers, runs a fresh set of tests on the
        ECU’s hardware and sends back the STATUS Byte. Check the value of the STATUS
        byte for potential errors."""
        self.write('IN0')
        e = self.read_bytes(1)
        print('STATUS', e)
        return e

    def factory_reset(self):
        """Reset the RGA to its factory default settings.
        """
        self.write('IN1')

    def standby(self):
        """Put instrument in standby mode. The filament and CDEM are turned off.
        """
        self.write('IN2')
