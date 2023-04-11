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

from pymeasure.test import expected_protocol

from pymeasure.instruments.lakeshore.lakeshore211 import LakeShore211


def test_init():
    with expected_protocol(
            LakeShore211,
            [],
    ):
        pass  # Verify the expected communication.


def test_temp_kelvin():
    with expected_protocol(
            LakeShore211,
            [(b"KRDG?", b"27.1")],
    ) as instr:
        assert instr.temperature_kelvin == 27.1


def test_temp_celsius():
    with expected_protocol(
            LakeShore211,
            [(b"CRDG?", b"27.1")],
    ) as instr:
        assert instr.temperature_celsius == 27.1


def test_set_analog():
    with expected_protocol(
            LakeShore211,
            [(b"ANALOG 0,1", None),
             (b"ANALOG?", b"0,1")],
    ) as instr:
        instr.analog = (0, 1)
        assert instr.analog == (0, 1)


def test_set_display():
    with expected_protocol(
            LakeShore211,
            [(b"DISPFLD 1", None),
             (b"DISPFLD?", b"1")],
    ) as instr:
        instr.display = 'celsius'
        assert instr.display == 'celsius'
