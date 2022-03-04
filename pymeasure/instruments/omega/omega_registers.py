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

OMEGA_COMMANDS = {
    "ABSOLUTE_ALARM_1_HIGH": {
        "data_type": "F",
        "description": "Alarm High value (Absolute mode)",
        "read_write": "NV",
        "register": 1290,
        "register_hex": "0x050a"
    },
    "ABSOLUTE_ALARM_1_LOW": {
        "data_type": "F",
        "description": "Alarm Low value (Absolute mode)",
        "read_write": "NV",
        "register": 1288,
        "register_hex": "0x0508"
    },
    "ABSOLUTE_ALARM_2_HIGH": {
        "data_type": "F",
        "description": "Alarm High value (Absolute mode)",
        "read_write": "NV",
        "register": 1322,
        "register_hex": "0x052a"
    },
    "ABSOLUTE_ALARM_2_LOW": {
        "data_type": "F",
        "description": "Alarm Low value (Absolute mode)",
        "read_write": "NV",
        "register": 1320,
        "register_hex": "0x0528"
    },
    "ABSOLUTE_SETPOINT_1": {
        "data_type": "F",
        "description": "Setpoint 1 Absolute value",
        "read_write": "NV",
        "register": 738,
        "register_hex": "0x02e2"
    },
    "ABSOLUTE_SETPOINT_2": {
        "data_type": "F",
        "description": "Setpoint 2 Absolute value",
        "read_write": "NV",
        "register": 742,
        "register_hex": "0x02ea"
    },
    "ALARM_1_CONTACT_CLOSURE_TYPE": {
        "data_type": "R",
        "description": "Enumerated Contact closure type",
        "read_write": "NV",
        "register": 1286,
        "register_hex": "0x0506"
    },
    "ALARM_1_DISPLAY_COLOR": {
        "data_type": "R",
        "description": "Enumerated Alarm Color",
        "read_write": "NV",
        "register": 1283,
        "register_hex": "0x0503"
    },
    "ALARM_1_HIGH_HIGH_MODE": {
        "data_type": "R",
        "description": "Enumerated Toggle value",
        "read_write": "NV",
        "register": 1284,
        "register_hex": "0x0504"
    },
    "ALARM_1_HIGH_HIGH_OFFSET": {
        "data_type": "F",
        "description": "Alarm High-High offset",
        "read_write": "NV",
        "register": 1296,
        "register_hex": "0x0510"
    },
    "ALARM_1_LATCH_TYPE": {
        "data_type": "R",
        "description": "Enumerated Toggle value",
        "read_write": "NV",
        "register": 1285,
        "register_hex": "0x0505"
    },
    "ALARM_1_MODE": {
        "data_type": "R",
        "description": "Enumerated Alarm Mode",
        "read_write": "NV",
        "register": 1282,
        "register_hex": "0x0502"
    },
    "ALARM_1_OFF_DELAY": {
        "data_type": "F",
        "description": "Alarm Off Delay",
        "read_write": "NV",
        "register": 1300,
        "register_hex": "0x0514"
    },
    "ALARM_1_ON_DELAY": {
        "data_type": "F",
        "description": "Alarm On Delay",
        "read_write": "NV",
        "register": 1298,
        "register_hex": "0x0512"
    },
    "ALARM_1_POWER_ON_STATE": {
        "data_type": "R",
        "description": "Enumerated Power on control",
        "read_write": "NV",
        "register": 1287,
        "register_hex": "0x0507"
    },
    "ALARM_1_TYPE": {
        "data_type": "R",
        "description": "Enumerated Alarm type",
        "read_write": "NV",
        "register": 1281,
        "register_hex": "0x0501"
    },
    "ALARM_2_CONTACT_CLOSURE_TYPE": {
        "data_type": "R",
        "description": "Enumerated Contact closure type",
        "read_write": "NV",
        "register": 1318,
        "register_hex": "0x0526"
    },
    "ALARM_2_DISPLAY_COLOR": {
        "data_type": "R",
        "description": "Enumerated Alarm Color",
        "read_write": "NV",
        "register": 1315,
        "register_hex": "0x0523"
    },
    "ALARM_2_HIGH_HIGH_MODE": {
        "data_type": "R",
        "description": "Enumerated Toggle value",
        "read_write": "NV",
        "register": 1316,
        "register_hex": "0x0524"
    },
    "ALARM_2_HIGH_HIGH_OFFSET": {
        "data_type": "F",
        "description": "Alarm High-High offset",
        "read_write": "NV",
        "register": 1328,
        "register_hex": "0x0530"
    },
    "ALARM_2_LATCH_TYPE": {
        "data_type": "R",
        "description": "Enumerated Toggle value",
        "read_write": "NV",
        "register": 1317,
        "register_hex": "0x0525"
    },
    "ALARM_2_MODE": {
        "data_type": "R",
        "description": "Enumerated Alarm Mode",
        "read_write": "NV",
        "register": 1314,
        "register_hex": "0x0522"
    },
    "ALARM_2_OFF_DELAY": {
        "data_type": "F",
        "description": "Alarm Off Delay Excitation Voltage",
        "read_write": "NV",
        "register": 1332,
        "register_hex": "0x0534"
    },
    "ALARM_2_ON_DELAY": {
        "data_type": "F",
        "description": "Alarm On Delay",
        "read_write": "NV",
        "register": 1330,
        "register_hex": "0x0532"
    },
    "ALARM_2_POWER_ON_STATE": {
        "data_type": "R",
        "description": "Enumerated Power on control",
        "read_write": "NV",
        "register": 1319,
        "register_hex": "0x0527"
    },
    "ALARM_2_TYPE": {
        "data_type": "R",
        "description": "Enumerated Alarm type",
        "read_write": "NV",
        "register": 1313,
        "register_hex": "0x0521"
    },
    "ALARM_STATE": {
        "data_type": "R",
        "description": "Alarm state (Bit 0)",
        "read_write": "R",
        "register": 1312,
        "register_hex": "0x0520"
    },
    "BOOT_LOADER_VERSION": {
        "data_type": "L",
        "description": "Boot Loader Version",
        "read_write": "R",
        "register": 518,
        "register_hex": "0x0206"
    },
    "CONTROL_SETPOINT": {
        "data_type": "F",
        "description": "Setpoint used for PID/Control functions",
        "read_write": "RW",
        "register": 624,
        "register_hex": "0x0270"
    },
    "CURRENT_INPUT_VALID": {
        "data_type": "R",
        "description": "Flag indicating process value is valid",
        "read_write": "R",
        "register": 556,
        "register_hex": "0x022c"
    },
    "CURRENT_INPUT_VALUE": {
        "data_type": "F",
        "description": "Current Process value",
        "read_write": "R",
        "register": 640,
        "register_hex": "0x0280"
    },
    "CURRENT_PROFILE": {
        "data_type": "R",
        "description": "Use to select R&S profile to access ",
        "read_write": "RW",
        "register": 610,
        "register_hex": "0x0262"
    },
    "CURRENT_SEGMENT": {
        "data_type": "R",
        "description": "Use to select profile segment to access",
        "read_write": "RW",
        "register": 611,
        "register_hex": "0x0263"
    },
    "CURRENT_SETPOINT_1": {
        "data_type": "F",
        "description": "Current value of Setpoint 1",
        "read_write": "RW",
        "register": 544,
        "register_hex": "0x0220"
    },
    "CURRENT_SETPOINT_2": {
        "data_type": "F",
        "description": "Current value of Setpoint 2",
        "read_write": "RW",
        "register": 546,
        "register_hex": "0x0222"
    },
    "DB_0_24_INPUT_1": {
        "data_type": "F",
        "description": "Scale input value 1",
        "read_write": "NV",
        "register": 804,
        "register_hex": "0x0324"
    },
    "DB_0_24_INPUT_2": {
        "data_type": "F",
        "description": "Scale input value 2",
        "read_write": "NV",
        "register": 808,
        "register_hex": "0x0328"
    },
    "DB_0_24_MANUAL_LIVE": {
        "data_type": "R",
        "description": "Enumerated Input Process mode",
        "read_write": "NV",
        "register": 800,
        "register_hex": "0x0320"
    },
    "DB_0_24_READING_1": {
        "data_type": "F",
        "description": "Scale reading value 1",
        "read_write": "NV",
        "register": 802,
        "register_hex": "0x0322"
    },
    "DB_0_24_READING_2": {
        "data_type": "F",
        "description": "Scale reading value 2",
        "read_write": "NV",
        "register": 806,
        "register_hex": "0x0326"
    },
    "DB_10_INPUT_1": {
        "data_type": "F",
        "description": "Scale input value 1",
        "read_write": "NV",
        "register": 836,
        "register_hex": "0x0344"
    },
    "DB_10_INPUT_2": {
        "data_type": "F",
        "description": "Scale input value 2",
        "read_write": "NV",
        "register": 840,
        "register_hex": "0x0348"
    },
    "DB_10_MANUAL_LIVE": {
        "data_type": "R",
        "description": "Enumerated Input Process mode",
        "read_write": "NV",
        "register": 832,
        "register_hex": "0x0340"
    },
    "DB_10_READING_1": {
        "data_type": "F",
        "description": "Scale reading value 1",
        "read_write": "NV",
        "register": 834,
        "register_hex": "0x0342"
    },
    "DB_10_READING_2": {
        "data_type": "F",
        "description": "Scale reading value 2",
        "read_write": "NV",
        "register": 838,
        "register_hex": "0x0346"
    },
    "DB_1_INPUT_1": {
        "data_type": "F",
        "description": "Scale input value 1",
        "read_write": "NV",
        "register": 868,
        "register_hex": "0x0364"
    },
    "DB_1_INPUT_2": {
        "data_type": "F",
        "description": "Scale input value 2",
        "read_write": "NV",
        "register": 872,
        "register_hex": "0x0368"
    },
    "DB_1_MANUAL_LIVE": {
        "data_type": "R",
        "description": "Enumerated Input Process mode",
        "read_write": "NV",
        "register": 864,
        "register_hex": "0x0360"
    },
    "DB_1_READING_1": {
        "data_type": "F",
        "description": "Scale reading value 1",
        "read_write": "NV",
        "register": 866,
        "register_hex": "0x0362"
    },
    "DB_1_READING_2": {
        "data_type": "F",
        "description": "Scale reading value 2",
        "read_write": "NV",
        "register": 870,
        "register_hex": "0x0366"
    },
    "DB_4_20_INPUT_1": {
        "data_type": "F",
        "description": "Scale input value 1",
        "read_write": "NV",
        "register": 772,
        "register_hex": "0x0304"
    },
    "DB_4_20_INPUT_2": {
        "data_type": "F",
        "description": "Scale input value 2",
        "read_write": "NV",
        "register": 776,
        "register_hex": "0x0308"
    },
    "DB_4_20_MANUAL_LIVE": {
        "data_type": "R",
        "description": "Enumerated Input Process mode",
        "read_write": "NV",
        "register": 768,
        "register_hex": "0x0300"
    },
    "DB_4_20_READING_1": {
        "data_type": "F",
        "description": "Scale reading value 1",
        "read_write": "NV",
        "register": 770,
        "register_hex": "0x0302"
    },
    "DB_4_20_READING_2": {
        "data_type": "F",
        "description": "Scale reading value 2",
        "read_write": "NV",
        "register": 774,
        "register_hex": "0x0306"
    },
    "DB_ANNUNCIATOR_1_MODE": {
        "data_type": "R",
        "description": "Enumerated Annunciator Mode",
        "read_write": "NV",
        "register": 1505,
        "register_hex": "0x05e1"
    },
    "DB_ANNUNCIATOR_2_MODE": {
        "data_type": "R",
        "description": "Enumerated Annunciator Mode",
        "read_write": "NV",
        "register": 1509,
        "register_hex": "0x05e5"
    },
    "DB_ANNUNCIATOR_3_MODE": {
        "data_type": "R",
        "description": "Enumerated Annunciator Mode",
        "read_write": "NV",
        "register": 1513,
        "register_hex": "0x05e9"
    },
    "DB_ANNUNCIATOR_4_MODE": {
        "data_type": "R",
        "description": "Enumerated Annunciator Mode",
        "read_write": "NV",
        "register": 1517,
        "register_hex": "0x05ed"
    },
    "DB_ANNUNCIATOR_STATE": {
        "data_type": "R",
        "description": "Enumerated Annunciator State",
        "read_write": "R",
        "register": 1516,
        "register_hex": "0x05ec"
    },
    "DB_LINEARIZATION_MANUAL_LIVE": {
        "data_type": "R",
        "description": "Enumerated Linearization mode",
        "read_write": "NV",
        "register": 1792,
        "register_hex": "0x0700"
    },
    "DB_NUMBER_LINEARIZATION_POINTS": {
        "data_type": "R",
        "description": "Number of active points",
        "read_write": "NV",
        "register": 1793,
        "register_hex": "0x0701"
    },
    "DB_POINT_05_INPUT_1": {
        "data_type": "F",
        "description": "Scale input value 1",
        "read_write": "NV",
        "register": 932,
        "register_hex": "0x03a4"
    },
    "DB_POINT_05_INPUT_2": {
        "data_type": "F",
        "description": "Scale input value 2",
        "read_write": "NV",
        "register": 936,
        "register_hex": "0x03a8"
    },
    "DB_POINT_05_MANUAL_LIVE": {
        "data_type": "R",
        "description": "Enumerated Input Process mode",
        "read_write": "NV",
        "register": 928,
        "register_hex": "0x03a0"
    },
    "DB_POINT_05_READING_1": {
        "data_type": "F",
        "description": "Scale reading value 1",
        "read_write": "NV",
        "register": 930,
        "register_hex": "0x03a2"
    },
    "DB_POINT_05_READING_2": {
        "data_type": "F",
        "description": "Scale reading value 2",
        "read_write": "NV",
        "register": 934,
        "register_hex": "0x03a6"
    },
    "DB_POINT_1_INPUT_1": {
        "data_type": "F",
        "description": "Linearization input value 1",
        "read_write": "NV",
        "register": 1796,
        "register_hex": "0x0704"
    },
    "DB_POINT_1_INPUT_10": {
        "data_type": "F",
        "description": "Linearization input value 10",
        "read_write": "NV",
        "register": 1832,
        "register_hex": "0x0728"
    },
    "DB_POINT_1_INPUT_2": {
        "data_type": "F",
        "description": "Linearization input value 2",
        "read_write": "NV",
        "register": 1800,
        "register_hex": "0x0708"
    },
    "DB_POINT_1_INPUT_3": {
        "data_type": "F",
        "description": "Linearization input value 3",
        "read_write": "NV",
        "register": 1804,
        "register_hex": "0x070c"
    },
    "DB_POINT_1_INPUT_4": {
        "data_type": "F",
        "description": "Linearization input value 4",
        "read_write": "NV",
        "register": 1808,
        "register_hex": "0x0710"
    },
    "DB_POINT_1_INPUT_5": {
        "data_type": "F",
        "description": "Linearization input value 5",
        "read_write": "NV",
        "register": 1812,
        "register_hex": "0x0714"
    },
    "DB_POINT_1_INPUT_6": {
        "data_type": "F",
        "description": "Linearization input value 6",
        "read_write": "NV",
        "register": 1816,
        "register_hex": "0x0718"
    },
    "DB_POINT_1_INPUT_7": {
        "data_type": "F",
        "description": "Linearization input value 7",
        "read_write": "NV",
        "register": 1820,
        "register_hex": "0x071c"
    },
    "DB_POINT_1_INPUT_8": {
        "data_type": "F",
        "description": "Linearization input value 8",
        "read_write": "NV",
        "register": 1824,
        "register_hex": "0x0720"
    },
    "DB_POINT_1_INPUT_9": {
        "data_type": "F",
        "description": "Linearization input value 9",
        "read_write": "NV",
        "register": 1828,
        "register_hex": "0x0724"
    },
    "DB_POINT_1_MANUAL_LIVE": {
        "data_type": "R",
        "description": "Enumerated Input Process mode",
        "read_write": "NV",
        "register": 896,
        "register_hex": "0x0380"
    },
    "DB_POINT_1_READING_1": {
        "data_type": "F",
        "description": "Linearization reading value 1",
        "read_write": "NV",
        "register": 1794,
        "register_hex": "0x0702"
    },
    "DB_POINT_1_READING_10": {
        "data_type": "F",
        "description": "Linearization reading value 10",
        "read_write": "NV",
        "register": 1830,
        "register_hex": "0x0726"
    },
    "DB_POINT_1_READING_2": {
        "data_type": "F",
        "description": "Linearization reading value 2",
        "read_write": "NV",
        "register": 1798,
        "register_hex": "0x0706"
    },
    "DB_POINT_1_READING_3": {
        "data_type": "F",
        "description": "Linearization reading value 3",
        "read_write": "NV",
        "register": 1802,
        "register_hex": "0x070a"
    },
    "DB_POINT_1_READING_4": {
        "data_type": "F",
        "description": "Linearization reading value 4",
        "read_write": "NV",
        "register": 1806,
        "register_hex": "0x070e"
    },
    "DB_POINT_1_READING_5": {
        "data_type": "F",
        "description": "Linearization reading value 5",
        "read_write": "NV",
        "register": 1810,
        "register_hex": "0x0712"
    },
    "DB_POINT_1_READING_6": {
        "data_type": "F",
        "description": "Linearization reading value 6",
        "read_write": "NV",
        "register": 1814,
        "register_hex": "0x0716"
    },
    "DB_POINT_1_READING_7": {
        "data_type": "F",
        "description": "Linearization reading value 7",
        "read_write": "NV",
        "register": 1818,
        "register_hex": "0x071a"
    },
    "DB_POINT_1_READING_8": {
        "data_type": "F",
        "description": "Linearization reading value 8",
        "read_write": "NV",
        "register": 1822,
        "register_hex": "0x071e"
    },
    "DB_POINT_1_READING_9": {
        "data_type": "F",
        "description": "Linearization reading value 9",
        "read_write": "NV",
        "register": 1826,
        "register_hex": "0x0722"
    },
    "DEVIATION_ALARM_1_HIGH": {
        "data_type": "F",
        "description": "Alarm High offset (Deviation mode)",
        "read_write": "NV",
        "register": 1294,
        "register_hex": "0x050e"
    },
    "DEVIATION_ALARM_1_LOW": {
        "data_type": "F",
        "description": "Alarm Low offset (Deviation mode)",
        "read_write": "NV",
        "register": 1292,
        "register_hex": "0x050c"
    },
    "DEVIATION_ALARM_2_HIGH": {
        "data_type": "F",
        "description": "Alarm High offset (Deviation mode)",
        "read_write": "NV",
        "register": 1326,
        "register_hex": "0x052e"
    },
    "DEVIATION_ALARM_2_LOW": {
        "data_type": "F",
        "description": "Alarm Low offset (Deviation mode)",
        "read_write": "NV",
        "register": 1324,
        "register_hex": "0x052c"
    },
    "DEVIATION_SETPOINT_2": {
        "data_type": "F",
        "description": "Setpoint 2 value (derivative mode)",
        "read_write": "NV",
        "register": 744,
        "register_hex": "0x02ec"
    },
    "DEVICE_ID": {
        "data_type": "L",
        "description": "Device Identifier ",
        "read_write": "R",
        "register": 512,
        "register_hex": "0x0200"
    },
    "DISPLAY_ALARM_CONTROL": {
        "data_type": "R",
        "description": "",
        "read_write": "",
        "register": 589,
        "register_hex": "0x024d"
    },
    "DISPLAY_BRIGHTNESS": {
        "data_type": "R",
        "description": "Enumerated value to set display brightness",
        "read_write": "NV",
        "register": 587,
        "register_hex": "0x024b"
    },
    "DISPLAY_COLOR_NORMAL": {
        "data_type": "R",
        "description": "Enumerated value to set display color",
        "read_write": "NV",
        "register": 586,
        "register_hex": "0x024a"
    },
    "DISPLAY_ROUNDING": {
        "data_type": "F",
        "description": "Determines display rounding",
        "read_write": "NV",
        "register": 590,
        "register_hex": "0x024e"
    },
    "DISPLAY_UNITS": {
        "data_type": "R",
        "description": "Enumerated value - units of measure",
        "read_write": "NV",
        "register": 585,
        "register_hex": "0x0249"
    },
    "ETH_CONTINUOUS_DATA_PERIO": {
        "data_type": "F",
        "description": "",
        "read_write": "NV",
        "register": 1572,
        "register_hex": "0x0624"
    },
    "ETH_DATA_FLOW": {
        "data_type": "R",
        "description": "",
        "read_write": "NV",
        "register": 1570,
        "register_hex": "0x0622"
    },
    "ETH_DATA_FORMAT_PEAK": {
        "data_type": "R",
        "description": "",
        "read_write": "NV",
        "register": 1576,
        "register_hex": "0x0628"
    },
    "ETH_DATA_FORMAT_READING": {
        "data_type": "R",
        "description": "",
        "read_write": "NV",
        "register": 1575,
        "register_hex": "0x0627"
    },
    "ETH_DATA_FORMAT_STATUS": {
        "data_type": "R",
        "description": "",
        "read_write": "NV",
        "register": 1574,
        "register_hex": "0x0626"
    },
    "ETH_DATA_FORMAT_UNIT": {
        "data_type": "R",
        "description": "",
        "read_write": "NV",
        "register": 1578,
        "register_hex": "0x062a"
    },
    "ETH_DATA_FORMAT_VALLEY": {
        "data_type": "R",
        "description": "",
        "read_write": "NV",
        "register": 1577,
        "register_hex": "0x0629"
    },
    "ETH_DEVICE_ADDRESS": {
        "data_type": "R",
        "description": "",
        "read_write": "NV",
        "register": 1581,
        "register_hex": "0x062d"
    },
    "ETH_ECHO_MODE": {
        "data_type": "R",
        "description": "",
        "read_write": "NV",
        "register": 1571,
        "register_hex": "0x0623"
    },
    "ETH_LINE_FEED": {
        "data_type": "R",
        "description": "",
        "read_write": "NV",
        "register": 1579,
        "register_hex": "0x062b"
    },
    "ETH_MODBUS_EOF": {
        "data_type": "R",
        "description": "",
        "read_write": "NV",
        "register": 1583,
        "register_hex": "0x062f"
    },
    "ETH_MODBUS_MODE": {
        "data_type": "R",
        "description": "",
        "read_write": "NV",
        "register": 1582,
        "register_hex": "0x062e"
    },
    "ETH_PROTOCOL": {
        "data_type": "R",
        "description": "",
        "read_write": "NV",
        "register": 1568,
        "register_hex": "0x0620"
    },
    "ETH_RECOGNITION_CHARACTER": {
        "data_type": "R",
        "description": "",
        "read_write": "NV",
        "register": 1569,
        "register_hex": "0x0621"
    },
    "ETH_SEPARATION_CHAR": {
        "data_type": "R",
        "description": "",
        "read_write": "NV",
        "register": 1580,
        "register_hex": "0x062c"
    },
    "EXCITATION_VOLTAGE": {
        "data_type": "R",
        "description": "Enumerated Excitation Voltage",
        "read_write": "NV",
        "register": 1472,
        "register_hex": "0x05c0"
    },
    "FACTORY_RESET": {
        "data_type": "R",
        "description": "Write 1 to force reset to factory defaults",
        "read_write": "W",
        "register": 577,
        "register_hex": "0x0241"
    },
    "HARDWARE_VERSION": {
        "data_type": "L",
        "description": "Hardware Version",
        "read_write": "R",
        "register": 520,
        "register_hex": "0x0208"
    },
    "INPUT_DIGITAL": {
        "data_type": "R",
        "description": "State of digital input pin",
        "read_write": "R",
        "register": 542,
        "register_hex": "0x021e"
    },
    "INPUT_SENSOR": {
        "data_type": "R",
        "description": "Enumerated sensor (input) type",
        "read_write": "NV",
        "register": 642,
        "register_hex": "0x0282"
    },
    "ISOLATED_OUTPUT_VERSION": {
        "data_type": "L",
        "description": "Isolated Output Module Version",
        "read_write": "R",
        "register": 524,
        "register_hex": "0x020c"
    },
    "LATCH_RESET": {
        "data_type": "R",
        "description": "Write 1 to reset latched alarms",
        "read_write": "W",
        "register": 578,
        "register_hex": "0x0242"
    },
    "LOOP_BREAK_ENABLE": {
        "data_type": "R",
        "description": "Enumerated Toggle",
        "read_write": "NV",
        "register": 710,
        "register_hex": "0x02c6"
    },
    "LOOP_BREAK_TIME": {
        "data_type": "L",
        "description": "Time (msec) for break test",
        "read_write": "NV",
        "register": 712,
        "register_hex": "0x02c8"
    },
    "OPEN_CIRCUIT_ENABLE": {
        "data_type": "R",
        "description": "Write 1 to enable open circuit test Password / Access Control",
        "read_write": "NV",
        "register": 714,
        "register_hex": "0x02ca"
    },
    "OUTPUT_1_HW_TYPE": {
        "data_type": "R",
        "description": "Enumerated Hardware Type - upper 4 bits provide the 'Instance' count",
        "read_write": "R",
        "register": 1024,
        "register_hex": "0x0400"
    },
    "OUTPUT_1_MODE": {
        "data_type": "R",
        "description": "Enumerated Output Mode",
        "read_write": "NV",
        "register": 1025,
        "register_hex": "0x0401"
    },
    "OUTPUT_1_ON_OFF_ACTION": {
        "data_type": "R",
        "description": "Enumerated On-Off Action",
        "read_write": "NV",
        "register": 1026,
        "register_hex": "0x0402"
    },
    "OUTPUT_1_ON_OFF_DEADBAND": {
        "data_type": "F",
        "description": "Deadband",
        "read_write": "NV",
        "register": 1030,
        "register_hex": "0x0406"
    },
    "OUTPUT_1_OUTPUT_RANGE": {
        "data_type": "R",
        "description": "Enumerated Output Analog Range",
        "read_write": "NV",
        "register": 1032,
        "register_hex": "0x0408"
    },
    "OUTPUT_1_PULSE_LENGTH": {
        "data_type": "F",
        "description": "Pulse Length (.1 sec increments)",
        "read_write": "NV",
        "register": 1028,
        "register_hex": "0x0404"
    },
    "OUTPUT_1_RETRAN_OUTPUT_1": {
        "data_type": "F",
        "description": "Output Level Low",
        "read_write": "NV",
        "register": 1036,
        "register_hex": "0x040c"
    },
    "OUTPUT_1_RETRAN_OUTPUT_2": {
        "data_type": "F",
        "description": "Output Level High",
        "read_write": "NV",
        "register": 1040,
        "register_hex": "0x0410"
    },
    "OUTPUT_1_RETRAN_READING_1": {
        "data_type": "F",
        "description": "Retransmission Reading Low",
        "read_write": "NV",
        "register": 1034,
        "register_hex": "0x040a"
    },
    "OUTPUT_1_RETRAN_READING_2": {
        "data_type": "F",
        "description": "Retransmission Reading High",
        "read_write": "NV",
        "register": 1038,
        "register_hex": "0x040e"
    },
    "OUTPUT_1_SETPOINT": {
        "data_type": "R",
        "description": "Output Setpoint selection",
        "read_write": "NV",
        "register": 1027,
        "register_hex": "0x0403"
    },
    "OUTPUT_1_STATE": {
        "data_type": "R",
        "description": "State of Output (0/1)",
        "read_write": "R",
        "register": 560,
        "register_hex": "0x0230"
    },
    "OUTPUT_2_HW_TYPE": {
        "data_type": "R",
        "description": "Enumerated Hardware Type - upper 4 bits provide the 'Instance' count",
        "read_write": "R",
        "register": 1056,
        "register_hex": "0x0420"
    },
    "OUTPUT_2_MODE": {
        "data_type": "R",
        "description": "Enumerated Output Mode",
        "read_write": "NV",
        "register": 1057,
        "register_hex": "0x0421"
    },
    "OUTPUT_2_ON_OFF_ACTION": {
        "data_type": "R",
        "description": "Enumerated On-Off Action",
        "read_write": "NV",
        "register": 1058,
        "register_hex": "0x0422"
    },
    "OUTPUT_2_ON_OFF_DEADBAND": {
        "data_type": "F",
        "description": "Deadband",
        "read_write": "NV",
        "register": 1062,
        "register_hex": "0x0426"
    },
    "OUTPUT_2_OUTPUT_RANGE": {
        "data_type": "R",
        "description": "Enumerated Output Analog Range",
        "read_write": "NV",
        "register": 1064,
        "register_hex": "0x0428"
    },
    "OUTPUT_2_PULSE_LENGTH": {
        "data_type": "F",
        "description": "Pulse Length (.1 sec increments)",
        "read_write": "NV",
        "register": 1060,
        "register_hex": "0x0424"
    },
    "OUTPUT_2_RETRAN_OUTPUT_1": {
        "data_type": "F",
        "description": "Output Level Low",
        "read_write": "NV",
        "register": 1068,
        "register_hex": "0x042c"
    },
    "OUTPUT_2_RETRAN_OUTPUT_2": {
        "data_type": "F",
        "description": "Output Level High",
        "read_write": "NV",
        "register": 1072,
        "register_hex": "0x0430"
    },
    "OUTPUT_2_RETRAN_READING_1": {
        "data_type": "F",
        "description": "Retransmission Reading Low",
        "read_write": "NV",
        "register": 1066,
        "register_hex": "0x042a"
    },
    "OUTPUT_2_RETRAN_READING_2": {
        "data_type": "F",
        "description": "Retransmission Reading High",
        "read_write": "NV",
        "register": 1070,
        "register_hex": "0x042e"
    },
    "OUTPUT_2_SETPOINT": {
        "data_type": "R",
        "description": "Output Setpoint selection",
        "read_write": "NV",
        "register": 1059,
        "register_hex": "0x0423"
    },
    "OUTPUT_2_STATE": {
        "data_type": "R",
        "description": "State of Output (0/1)",
        "read_write": "R",
        "register": 561,
        "register_hex": "0x0231"
    },
    "OUTPUT_3_HW_TYPE": {
        "data_type": "R",
        "description": "Enumerated Hardware Type - upper 4 bits provide the 'Instance' count",
        "read_write": "R",
        "register": 1088,
        "register_hex": "0x0440"
    },
    "OUTPUT_3_MODE": {
        "data_type": "R",
        "description": "Enumerated Output Mode",
        "read_write": "NV",
        "register": 1089,
        "register_hex": "0x0441"
    },
    "OUTPUT_3_ON_OFF_ACTION": {
        "data_type": "R",
        "description": "Enumerated On-Off Action",
        "read_write": "NV",
        "register": 1090,
        "register_hex": "0x0442"
    },
    "OUTPUT_3_ON_OFF_DEADBAND": {
        "data_type": "F",
        "description": "Deadband",
        "read_write": "NV",
        "register": 1094,
        "register_hex": "0x0446"
    },
    "OUTPUT_3_OUTPUT_RANGE": {
        "data_type": "R",
        "description": "Enumerated Output Analog Range",
        "read_write": "NV",
        "register": 1096,
        "register_hex": "0x0448"
    },
    "OUTPUT_3_PULSE_LENGTH": {
        "data_type": "F",
        "description": "Pulse Length (.1 sec increments)",
        "read_write": "NV",
        "register": 1092,
        "register_hex": "0x0444"
    },
    "OUTPUT_3_RETRAN_OUTPUT_1": {
        "data_type": "F",
        "description": "Output Level Low",
        "read_write": "NV",
        "register": 1100,
        "register_hex": "0x044c"
    },
    "OUTPUT_3_RETRAN_OUTPUT_2": {
        "data_type": "F",
        "description": "Output Level High",
        "read_write": "NV",
        "register": 1104,
        "register_hex": "0x0450"
    },
    "OUTPUT_3_RETRAN_READING_1": {
        "data_type": "F",
        "description": "Retransmission Reading Low",
        "read_write": "NV",
        "register": 1098,
        "register_hex": "0x044a"
    },
    "OUTPUT_3_RETRAN_READING_2": {
        "data_type": "F",
        "description": "Retransmission Reading High",
        "read_write": "NV",
        "register": 1102,
        "register_hex": "0x044e"
    },
    "OUTPUT_3_SETPOINT": {
        "data_type": "R",
        "description": "Output Setpoint selection",
        "read_write": "NV",
        "register": 1091,
        "register_hex": "0x0443"
    },
    "OUTPUT_3_STATE": {
        "data_type": "R",
        "description": "State of Output (0/1)",
        "read_write": "R",
        "register": 562,
        "register_hex": "0x0232"
    },
    "OUTPUT_4_HW_TYPE": {
        "data_type": "R",
        "description": "Enumerated Hardware Type - upper 4 bits provide the 'Instance' count",
        "read_write": "R",
        "register": 1120,
        "register_hex": "0x0460"
    },
    "OUTPUT_4_MODE": {
        "data_type": "R",
        "description": "Enumerated Output Mode",
        "read_write": "NV",
        "register": 1121,
        "register_hex": "0x0461"
    },
    "OUTPUT_4_ON_OFF_ACTION": {
        "data_type": "R",
        "description": "Enumerated On-Off Action",
        "read_write": "NV",
        "register": 1122,
        "register_hex": "0x0462"
    },
    "OUTPUT_4_ON_OFF_DEADBAND": {
        "data_type": "F",
        "description": "Deadband",
        "read_write": "NV",
        "register": 1126,
        "register_hex": "0x0466"
    },
    "OUTPUT_4_OUTPUT_RANGE": {
        "data_type": "R",
        "description": "Enumerated Output Analog Range",
        "read_write": "NV",
        "register": 1128,
        "register_hex": "0x0468"
    },
    "OUTPUT_4_PULSE_LENGTH": {
        "data_type": "F",
        "description": "Pulse Length (.1 sec increments)",
        "read_write": "NV",
        "register": 1124,
        "register_hex": "0x0464"
    },
    "OUTPUT_4_RETRAN_OUTPUT_1": {
        "data_type": "F",
        "description": "Output Level Low",
        "read_write": "NV",
        "register": 1132,
        "register_hex": "0x046c"
    },
    "OUTPUT_4_RETRAN_OUTPUT_28": {
        "data_type": "F",
        "description": "Output Level High",
        "read_write": "NV",
        "register": 1136,
        "register_hex": "0x0470"
    },
    "OUTPUT_4_RETRAN_READING_1": {
        "data_type": "F",
        "description": "Retransmission Reading Low",
        "read_write": "NV",
        "register": 1130,
        "register_hex": "0x046a"
    },
    "OUTPUT_4_RETRAN_READING_2": {
        "data_type": "F",
        "description": "Retransmission Reading High",
        "read_write": "NV",
        "register": 1134,
        "register_hex": "0x046e"
    },
    "OUTPUT_4_SETPOINT": {
        "data_type": "R",
        "description": "Output Setpoint selection",
        "read_write": "NV",
        "register": 1123,
        "register_hex": "0x0463"
    },
    "OUTPUT_4_STATE": {
        "data_type": "R",
        "description": "State of Output (0/1)",
        "read_write": "R",
        "register": 563,
        "register_hex": "0x0233"
    },
    "OUTPUT_5_HW_TYPE": {
        "data_type": "R",
        "description": "Enumerated Hardware Type - upper 4 bits provide the 'Instance' count",
        "read_write": "R",
        "register": 1152,
        "register_hex": "0x0480"
    },
    "OUTPUT_5_MODE": {
        "data_type": "R",
        "description": "Enumerated Output Mode",
        "read_write": "NV",
        "register": 1153,
        "register_hex": "0x0481"
    },
    "OUTPUT_5_ON_OFF_ACTION": {
        "data_type": "R",
        "description": "Enumerated On-Off Action",
        "read_write": "NV",
        "register": 1154,
        "register_hex": "0x0482"
    },
    "OUTPUT_5_ON_OFF_DEADBAND": {
        "data_type": "F",
        "description": "Deadband",
        "read_write": "NV",
        "register": 1158,
        "register_hex": "0x0486"
    },
    "OUTPUT_5_OUTPUT_RANGE": {
        "data_type": "R",
        "description": "Enumerated Output Analog Range",
        "read_write": "NV",
        "register": 1160,
        "register_hex": "0x0488"
    },
    "OUTPUT_5_PULSE_LENGTH": {
        "data_type": "F",
        "description": "Pulse Length (.1 sec increments)",
        "read_write": "NV",
        "register": 1156,
        "register_hex": "0x0484"
    },
    "OUTPUT_5_RETRAN_OUTPUT_1": {
        "data_type": "F",
        "description": "Output Level Low",
        "read_write": "NV",
        "register": 1164,
        "register_hex": "0x048c"
    },
    "OUTPUT_5_RETRAN_OUTPUT_28": {
        "data_type": "F",
        "description": "Output Level High",
        "read_write": "NV",
        "register": 1168,
        "register_hex": "0x0490"
    },
    "OUTPUT_5_RETRAN_READING_1": {
        "data_type": "F",
        "description": "Retransmission Reading Low",
        "read_write": "NV",
        "register": 1162,
        "register_hex": "0x048a"
    },
    "OUTPUT_5_RETRAN_READING_2": {
        "data_type": "F",
        "description": "Retransmission Reading High",
        "read_write": "NV",
        "register": 1165,
        "register_hex": "0x048e"
    },
    "OUTPUT_5_SETPOINT": {
        "data_type": "R",
        "description": "Output Setpoint selection",
        "read_write": "NV",
        "register": 1155,
        "register_hex": "0x0483"
    },
    "OUTPUT_5_STATE": {
        "data_type": "R",
        "description": "State of Output (0/1)",
        "read_write": "R",
        "register": 564,
        "register_hex": "0x0234"
    },
    "OUTPUT_6_HW_TYPE": {
        "data_type": "R",
        "description": "Enumerated Hardware Type - upper 4 bits provide the 'Instance' count",
        "read_write": "R",
        "register": 1184,
        "register_hex": "0x04a0"
    },
    "OUTPUT_6_MODE": {
        "data_type": "R",
        "description": "Enumerated Output Mode",
        "read_write": "NV",
        "register": 1185,
        "register_hex": "0x04a1"
    },
    "OUTPUT_6_ON_OFF_ACTION": {
        "data_type": "R",
        "description": "Enumerated On-Off Action",
        "read_write": "NV",
        "register": 1186,
        "register_hex": "0x04a2"
    },
    "OUTPUT_6_ON_OFF_DEADBAND": {
        "data_type": "F",
        "description": "Deadband",
        "read_write": "NV",
        "register": 1190,
        "register_hex": "0x04a6"
    },
    "OUTPUT_6_OUTPUT_RANGE": {
        "data_type": "R",
        "description": "Enumerated Output Analog Range",
        "read_write": "NV",
        "register": 1192,
        "register_hex": "0x04a8"
    },
    "OUTPUT_6_PULSE_LENGTH": {
        "data_type": "F",
        "description": "Pulse Length (.1 sec increments)",
        "read_write": "NV",
        "register": 1188,
        "register_hex": "0x04a4"
    },
    "OUTPUT_6_RETRAN_OUTPUT_1": {
        "data_type": "F",
        "description": "Output Level Low",
        "read_write": "NV",
        "register": 1196,
        "register_hex": "0x04ac"
    },
    "OUTPUT_6_RETRAN_OUTPUT_28": {
        "data_type": "F",
        "description": "Output Level High",
        "read_write": "NV",
        "register": 1200,
        "register_hex": "0x04b0"
    },
    "OUTPUT_6_RETRAN_READING_1": {
        "data_type": "F",
        "description": "Retransmission Reading Low",
        "read_write": "NV",
        "register": 1194,
        "register_hex": "0x04aa"
    },
    "OUTPUT_6_RETRAN_READING_2": {
        "data_type": "F",
        "description": "Retransmission Reading High",
        "read_write": "NV",
        "register": 1198,
        "register_hex": "0x04ae"
    },
    "OUTPUT_6_SETPOINT": {
        "data_type": "R",
        "description": "Output Setpoint selection",
        "read_write": "NV",
        "register": 1187,
        "register_hex": "0x04a3"
    },
    "OUTPUT_6_STATE": {
        "data_type": "R",
        "description": "State of Output (0/1)",
        "read_write": "R",
        "register": 565,
        "register_hex": "0x0235"
    },
    "OUTPUT_7_HW_TYPE": {
        "data_type": "R",
        "description": "Enumerated Hardware Type - upper 4 bits provide the 'Instance' count",
        "read_write": "R",
        "register": 1216,
        "register_hex": "0x04c0"
    },
    "OUTPUT_7_MODE": {
        "data_type": "R",
        "description": "Enumerated Output Mode",
        "read_write": "NV",
        "register": 1217,
        "register_hex": "0x04c1"
    },
    "OUTPUT_7_ON_OFF_ACTION": {
        "data_type": "R",
        "description": "Enumerated On-Off Action",
        "read_write": "NV",
        "register": 1218,
        "register_hex": "0x04c2"
    },
    "OUTPUT_7_ON_OFF_DEADBAND": {
        "data_type": "F",
        "description": "Deadband",
        "read_write": "NV",
        "register": 1222,
        "register_hex": "0x04c6"
    },
    "OUTPUT_7_OUTPUT_RANGE": {
        "data_type": "R",
        "description": "Enumerated Output Analog Range",
        "read_write": "NV",
        "register": 1224,
        "register_hex": "0x04c8"
    },
    "OUTPUT_7_PULSE_LENGTH": {
        "data_type": "F",
        "description": "Pulse Length (.1 sec increments)",
        "read_write": "NV",
        "register": 1220,
        "register_hex": "0x04c4"
    },
    "OUTPUT_7_RETRAN_OUTPUT_1": {
        "data_type": "F",
        "description": "Output Level Low",
        "read_write": "NV",
        "register": 1228,
        "register_hex": "0x04cc"
    },
    "OUTPUT_7_RETRAN_OUTPUT_28": {
        "data_type": "F",
        "description": "Output Level High",
        "read_write": "NV",
        "register": 1232,
        "register_hex": "0x04d0"
    },
    "OUTPUT_7_RETRAN_READING_1": {
        "data_type": "F",
        "description": "Retransmission Reading Low",
        "read_write": "NV",
        "register": 1226,
        "register_hex": "0x04ca"
    },
    "OUTPUT_7_RETRAN_READING_2": {
        "data_type": "F",
        "description": "Retransmission Reading High",
        "read_write": "NV",
        "register": 1230,
        "register_hex": "0x04ce"
    },
    "OUTPUT_7_SETPOINT": {
        "data_type": "R",
        "description": "Output Setpoint selection",
        "read_write": "NV",
        "register": 1219,
        "register_hex": "0x04c3"
    },
    "OUTPUT_7_STATE": {
        "data_type": "R",
        "description": "State of Output (0/1)",
        "read_write": "R",
        "register": 566,
        "register_hex": "0x0236"
    },
    "OUTPUT_8_HW_TYPE": {
        "data_type": "R",
        "description": "Enumerated Hardware Type - upper 4 bits provide the 'Instance' count",
        "read_write": "R",
        "register": 1248,
        "register_hex": "0x04e0"
    },
    "OUTPUT_8_MODE": {
        "data_type": "R",
        "description": "Enumerated Output Mode",
        "read_write": "NV",
        "register": 1259,
        "register_hex": "0x04e1"
    },
    "OUTPUT_8_ON_OFF_ACTION": {
        "data_type": "R",
        "description": "Enumerated On-Off Action",
        "read_write": "NV",
        "register": 1250,
        "register_hex": "0x04e2"
    },
    "OUTPUT_8_ON_OFF_DEADBAND": {
        "data_type": "F",
        "description": "Deadband",
        "read_write": "NV",
        "register": 1254,
        "register_hex": "0x04e6"
    },
    "OUTPUT_8_OUTPUT_RANGE": {
        "data_type": "R",
        "description": "Enumerated Output Analog Range",
        "read_write": "NV",
        "register": 1256,
        "register_hex": "0x04e8"
    },
    "OUTPUT_8_PULSE_LENGTH": {
        "data_type": "F",
        "description": "Pulse Length (.1 sec increments)",
        "read_write": "NV",
        "register": 1252,
        "register_hex": "0x04e4"
    },
    "OUTPUT_8_RETRAN_OUTPUT_1": {
        "data_type": "F",
        "description": "Output Level Low",
        "read_write": "NV",
        "register": 1260,
        "register_hex": "0x04ec"
    },
    "OUTPUT_8_RETRAN_OUTPUT_28": {
        "data_type": "F",
        "description": "Output Level High",
        "read_write": "NV",
        "register": 1264,
        "register_hex": "0x04f0"
    },
    "OUTPUT_8_RETRAN_READING_1": {
        "data_type": "F",
        "description": "Retransmission Reading Low",
        "read_write": "NV",
        "register": 1258,
        "register_hex": "0x04ea"
    },
    "OUTPUT_8_RETRAN_READING_2": {
        "data_type": "F",
        "description": "Retransmission Reading High",
        "read_write": "NV",
        "register": 1262,
        "register_hex": "0x04ee"
    },
    "OUTPUT_8_SETPOINT": {
        "data_type": "R",
        "description": "Output Setpoint selection",
        "read_write": "NV",
        "register": 1251,
        "register_hex": "0x04e3"
    },
    "OUTPUT_8_STATE": {
        "data_type": "R",
        "description": "State of Output (0/1)",
        "read_write": "R",
        "register": 567,
        "register_hex": "0x0237"
    },
    "PASSWORD_INIT": {
        "data_type": "L",
        "description": "INIT menu password",
        "read_write": "NV",
        "register": 722,
        "register_hex": "0x02d2"
    },
    "PASSWORD_INIT_ENABLE": {
        "data_type": "R",
        "description": "Write 1 to enable INIT menu password",
        "read_write": "NV",
        "register": 720,
        "register_hex": "0x02d0"
    },
    "PASSWORD_PROGRAM": {
        "data_type": "L",
        "description": "PROG menu password",
        "read_write": "NV",
        "register": 726,
        "register_hex": "0x02d6"
    },
    "PASSWORD_PROGRAM_ENABLE": {
        "data_type": "R",
        "description": "Write 1 to enable PROG menu password",
        "read_write": "NV",
        "register": 724,
        "register_hex": "0x02d4"
    },
    "PEAK_VALUE": {
        "data_type": "F",
        "description": "Maximum Value processed ",
        "read_write": "RW",
        "register": 550,
        "register_hex": "0x0226"
    },
    "PID_ACTION": {
        "data_type": "R",
        "description": "Enumerated PID control action",
        "read_write": "NV",
        "register": 673,
        "register_hex": "0x02a1"
    },
    "PID_ADAPTIVE_CONTROL_ENABLE": {
        "data_type": "R",
        "description": "Enumerated Toggle",
        "read_write": "NV",
        "register": 672,
        "register_hex": "0x02a0"
    },
    "PID_AUTOTUNE_DONE": {
        "data_type": "R",
        "description": "Internal use only",
        "read_write": "R",
        "register": 580,
        "register_hex": "0x0244"
    },
    "PID_AUTOTUNE_START": {
        "data_type": "R",
        "description": "Write 1 to force Autotuning to start",
        "read_write": "W",
        "register": 579,
        "register_hex": "0x0243"
    },
    "PID_AUTOTUNE_TIMEOUT": {
        "data_type": "L",
        "description": "Timeout (msec) for Autotuning",
        "read_write": "NV",
        "register": 674,
        "register_hex": "0x02a2"
    },
    "PID_D": {
        "data_type": "F",
        "description": "Derivative Gain value",
        "read_write": "NV",
        "register": 680,
        "register_hex": "0x02a8"
    },
    "PID_I": {
        "data_type": "F",
        "description": "Integral Gain value",
        "read_write": "NV",
        "register": 678,
        "register_hex": "0x02a6"
    },
    "PID_MAX_RATE": {
        "data_type": "F",
        "description": "PID maximum rate of change",
        "read_write": "NV",
        "register": 686,
        "register_hex": "0x02ae"
    },
    "PID_OUTPUT": {
        "data_type": "F",
        "description": "PID Output level (0.100%)",
        "read_write": "R",
        "register": 554,
        "register_hex": "0x022a"
    },
    "PID_P": {
        "data_type": "F",
        "description": "Proportional Gain value",
        "read_write": "NV",
        "register": 676,
        "register_hex": "0x02a4"
    },
    "PID_PERCENT_HIGH": {
        "data_type": "F",
        "description": "Maximum PID Control output value",
        "read_write": "NV",
        "register": 684,
        "register_hex": "0x02ac"
    },
    "PID_PERCENT_LOW": {
        "data_type": "F",
        "description": "Minimum PID Control output value",
        "read_write": "NV",
        "register": 682,
        "register_hex": "0x02aa"
    },
    "PID_STABILITY_RATE": {
        "data_type": "F",
        "description": "Autotune maximum rate of  change stability test",
        "read_write": "NV",
        "register": 690,
        "register_hex": "0x02b2"
    },
    "PID_STABILITY_TIMEOUT": {
        "data_type": "L",
        "description": "Autotune stability test timeout",
        "read_write": "NV",
        "register": 688,
        "register_hex": "0x02b0"
    },
    "PROCESS_RANGE": {
        "data_type": "R",
        "description": "Enumerated process input range",
        "read_write": "NV",
        "register": 647,
        "register_hex": "0x0287"
    },
    "PROCESS_SCALE_ENABLE": {
        "data_type": "R",
        "description": "Enables Scaling on Process values (LIVE/MANUAL)",
        "read_write": "RW",
        "register": 581,
        "register_hex": "0x0245"
    },
    "PROCESS_TYPE": {
        "data_type": "R",
        "description": "Enumerated input type",
        "read_write": "NV",
        "register": 648,
        "register_hex": "0x0288"
    },
    "RAMP_EVENT": {
        "data_type": "R",
        "description": "RE.ON flag set for current segment",
        "read_write": "NV",
        "register": 616,
        "register_hex": "0x0268"
    },
    "RAMP_SOAK_MODE": {
        "data_type": "R",
        "description": "Enumerated - Ramp and Soak mode",
        "read_write": "NV",
        "register": 608,
        "register_hex": "0x0260"
    },
    "RAMP_SOAK_PROFILE_SELECT": {
        "data_type": "R",
        "description": "Starting Profile for Ramp and Soak",
        "read_write": "RW",
        "register": 609,
        "register_hex": "0x0261"
    },
    "RAMP_SOAK_REMAINING_TIME": {
        "data_type": "L",
        "description": "Ramp or Soak time remaining",
        "read_write": "R",
        "register": 626,
        "register_hex": "0x0272"
    },
    "RAMP_SOAK_STATE": {
        "data_type": "R",
        "description": "Enumerated - R&S flags",
        "read_write": "R",
        "register": 628,
        "register_hex": "0x0274"
    },
    "RAMP_TIME": {
        "data_type": "L",
        "description": "Time (msec) to reach target SOAK setpoint",
        "read_write": "NV",
        "register": 620,
        "register_hex": "0x026c"
    },
    "RATE_MODE": {
        "data_type": "R",
        "description": "Rate Mode (RESERVED)",
        "read_write": "NV",
        "register": 654,
        "register_hex": "0x028e"
    },
    "READING_DECIMAL_POSITION": {
        "data_type": "R",
        "description": "Enumerated value - number of decimal points",
        "read_write": "NV",
        "register": 584,
        "register_hex": "0x0248"
    },
    "READING_FILTER_CONSTANT": {
        "data_type": "R",
        "description": "Enumerated input filtering constant",
        "read_write": "NV",
        "register": 655,
        "register_hex": "0x028f"
    },
    "REMOTE_SENSOR_VALUE": {
        "data_type": "F",
        "description": "Internal Use Only",
        "read_write": "",
        "register": 530,
        "register_hex": "0x0212"
    },
    "REMOTE_SETPOINT_VALUE": {
        "data_type": "F",
        "description": "",
        "read_write": "RW",
        "register": 532,
        "register_hex": "0x0214"
    },
    "RSP_0_10_INPUT_MAX": {
        "data_type": "F",
        "description": "",
        "read_write": "NV",
        "register": 1006,
        "register_hex": "0x03ee"
    },
    "RSP_0_10_INPUT_MIN": {
        "data_type": "F",
        "description": "",
        "read_write": "NV",
        "register": 1002,
        "register_hex": "0x03ea"
    },
    "RSP_0_10_SETPOINT_MAX": {
        "data_type": "F",
        "description": "",
        "read_write": "NV",
        "register": 1004,
        "register_hex": "0x03ec"
    },
    "RSP_0_10_SETPOINT_MIN": {
        "data_type": "F",
        "description": "",
        "read_write": "NV",
        "register": 1000,
        "register_hex": "0x03e8"
    },
    "RSP_0_1_INPUT_MAX": {
        "data_type": "F",
        "description": "",
        "read_write": "NV",
        "register": 1014,
        "register_hex": "0x03f6"
    },
    "RSP_0_1_INPUT_MIN": {
        "data_type": "F",
        "description": "",
        "read_write": "NV",
        "register": 1010,
        "register_hex": "0x03f2"
    },
    "RSP_0_1_SETPOINT_MAX": {
        "data_type": "F",
        "description": "",
        "read_write": "NV",
        "register": 1012,
        "register_hex": "0x03f4"
    },
    "RSP_0_1_SETPOINT_MIN": {
        "data_type": "F",
        "description": "",
        "read_write": "NV",
        "register": 1008,
        "register_hex": "0x03f0"
    },
    "RSP_0_24_INPUT_MAX": {
        "data_type": "F",
        "description": "",
        "read_write": "NV",
        "register": 998,
        "register_hex": "0x03e6"
    },
    "RSP_0_24_INPUT_MIN": {
        "data_type": "F",
        "description": "",
        "read_write": "NV",
        "register": 994,
        "register_hex": "0x03e2"
    },
    "RSP_0_24_SETPOINT_MAX": {
        "data_type": "F",
        "description": "",
        "read_write": "NV",
        "register": 996,
        "register_hex": "0x03e4"
    },
    "RSP_0_24_SETPOINT_MIN": {
        "data_type": "F",
        "description": "",
        "read_write": "NV",
        "register": 992,
        "register_hex": "0x03e0"
    },
    "RSP_4_20_INPUT_MAX": {
        "data_type": "F",
        "description": "Maximum Input",
        "read_write": "NV",
        "register": 990,
        "register_hex": "0x03de"
    },
    "RSP_4_20_INPUT_MIN": {
        "data_type": "F",
        "description": "Minimum Input",
        "read_write": "NV",
        "register": 986,
        "register_hex": "0x03da"
    },
    "RSP_4_20_SETPOINT_MIN": {
        "data_type": "F",
        "description": "Minimum Setpoint",
        "read_write": "NV",
        "register": 984,
        "register_hex": "0x03d8"
    },
    "RSP_4_20_SETPPOINT_MAX": {
        "data_type": "F",
        "description": "Maximum Setpoint",
        "read_write": "NV",
        "register": 988,
        "register_hex": "0x03dc"
    },
    "RSP_ENABLE": {
        "data_type": "R",
        "description": "Enumerated Toggle (sets SP 1 mode)",
        "read_write": "NV",
        "register": 977,
        "register_hex": "0x03d2"
    },
    "RSP_PROCESS_RANGE": {
        "data_type": "R",
        "description": "Enumerated Process Range",
        "read_write": "NV",
        "register": 976,
        "register_hex": "0x03d0"
    },
    "RTD_ACRV_OHM_TYPE": {
        "data_type": "R",
        "description": "Enumerated RTD Curve",
        "read_write": "NV",
        "register": 645,
        "register_hex": "0x0285"
    },
    "RTD_WIRE": {
        "data_type": "R",
        "description": "Enumerated RTD wire type ",
        "read_write": "NV",
        "register": 644,
        "register_hex": "0x0284"
    },
    "RUN_MODE": {
        "data_type": "R",
        "description": "Enumerated value - system running state",
        "read_write": "RW",
        "register": 576,
        "register_hex": "0x0240"
    },
    "SAFETY_DELAYED_OPER_RUN": {
        "data_type": "R",
        "description": "Write 1 to DISABLE return to RUN in OPER",
        "read_write": "NV",
        "register": 705,
        "register_hex": "0x02c1"
    },
    "SAFETY_DELAYED_POWER_ON_RUN": {
        "data_type": "R",
        "description": "Write 1 to DISABLE auto RUN on power up",
        "read_write": "NV",
        "register": 704,
        "register_hex": "0x02c0"
    },
    "SAFETY_SETPOINT_LIMIT_HIGH": {
        "data_type": "F",
        "description": "Maximum allowed setpoint value",
        "read_write": "NV",
        "register": 708,
        "register_hex": "0x02c4"
    },
    "SAFETY_SETPOINT_LIMIT_LOW": {
        "data_type": "F",
        "description": "Minimum allowed setpoint value",
        "read_write": "NV",
        "register": 706,
        "register_hex": "0x02c2"
    },
    "SEGMENTS_PER_PROFILE": {
        "data_type": "R",
        "description": "Number of segments in current profile",
        "read_write": "NV",
        "register": 612,
        "register_hex": "0x0264"
    },
    "SERIAL_232_485": {
        "data_type": "R",
        "description": "Enumerated serial interface type",
        "read_write": "NV",
        "register": 1616,
        "register_hex": "0x0650"
    },
    "SERIAL_BAUD_RATE": {
        "data_type": "R",
        "description": "Enumerated baud rate value",
        "read_write": "NV",
        "register": 1617,
        "register_hex": "0x0651"
    },
    "SERIAL_CONTINUOUS_DATA_PE": {
        "data_type": "F",
        "description": "",
        "read_write": "NV",
        "register": 1604,
        "register_hex": "0x0644"
    },
    "SERIAL_DATABITS": {
        "data_type": "R",
        "description": "Enumerated data bits value",
        "read_write": "NV",
        "register": 1619,
        "register_hex": "0x0653"
    },
    "SERIAL_DATA_FLOW": {
        "data_type": "R",
        "description": "",
        "read_write": "NV",
        "register": 1602,
        "register_hex": "0x0642"
    },
    "SERIAL_DATA_FORMAT_PEAK": {
        "data_type": "R",
        "description": "",
        "read_write": "NV",
        "register": 1608,
        "register_hex": "0x0648"
    },
    "SERIAL_DATA_FORMAT_READIN": {
        "data_type": "R",
        "description": "",
        "read_write": "NV",
        "register": 1607,
        "register_hex": "0x0647"
    },
    "SERIAL_DATA_FORMAT_STATUS": {
        "data_type": "R",
        "description": "",
        "read_write": "NV",
        "register": 1606,
        "register_hex": "0x0646"
    },
    "SERIAL_DATA_FORMAT_UNIT": {
        "data_type": "R",
        "description": "",
        "read_write": "NV",
        "register": 1610,
        "register_hex": "0x064a"
    },
    "SERIAL_DATA_FORMAT_VALLEY": {
        "data_type": "R",
        "description": "",
        "read_write": "NV",
        "register": 1609,
        "register_hex": "0x0649"
    },
    "SERIAL_DEVICE_ADDRESS": {
        "data_type": "R",
        "description": "",
        "read_write": "NV",
        "register": 1613,
        "register_hex": "0x064d"
    },
    "SERIAL_ECHO_MODE": {
        "data_type": "R",
        "description": "",
        "read_write": "NV",
        "register": 1603,
        "register_hex": "0x0643"
    },
    "SERIAL_LINE_FEED": {
        "data_type": "R",
        "description": "",
        "read_write": "NV",
        "register": 1611,
        "register_hex": "0x064b"
    },
    "SERIAL_MODBUS_EOF": {
        "data_type": "R",
        "description": "",
        "read_write": "NV",
        "register": 1615,
        "register_hex": "0x064f"
    },
    "SERIAL_MODBUS_MODE": {
        "data_type": "R",
        "description": "",
        "read_write": "NV",
        "register": 1614,
        "register_hex": "0x064e"
    },
    "SERIAL_PARITY": {
        "data_type": "R",
        "description": "Enumerated parity value",
        "read_write": "NV",
        "register": 1618,
        "register_hex": "0x0652"
    },
    "SERIAL_PROTOCOL": {
        "data_type": "R",
        "description": "",
        "read_write": "NV",
        "register": 1600,
        "register_hex": "0x0640"
    },
    "SERIAL_RECOGNITION_CHARAC": {
        "data_type": "R",
        "description": "",
        "read_write": "NV",
        "register": 1601,
        "register_hex": "0x0641"
    },
    "SERIAL_SEPARATION_CHAR": {
        "data_type": "R",
        "description": "",
        "read_write": "NV",
        "register": 1612,
        "register_hex": "0x064c"
    },
    "SERIAL_STOPBITS": {
        "data_type": "R",
        "description": "Enumerated stop bits value",
        "read_write": "NV",
        "register": 1620,
        "register_hex": "0x0654"
    },
    "SETPOINT_1_MODE": {
        "data_type": "R",
        "description": "Enumerated Setpoint 1 mode",
        "read_write": "NV",
        "register": 736,
        "register_hex": "0x02e0"
    },
    "SETPOINT_2_MODE": {
        "data_type": "R",
        "description": "Enumerated Setpoint 2 mode",
        "read_write": "NV",
        "register": 740,
        "register_hex": "0x02e8"
    },
    "SET_ICE_POINT": {
        "data_type": "R",
        "description": "Write 1 to set ICE POINT offset",
        "read_write": "NV",
        "register": 593,
        "register_hex": "0x0251"
    },
    "SET_TCAL_1_POINT": {
        "data_type": "R",
        "description": "Write 1 to set 1 point Cal. offset ",
        "read_write": "NV",
        "register": 594,
        "register_hex": "0x0252"
    },
    "SET_TCAL_2_POINT_HIGH": {
        "data_type": "R",
        "description": "Write 1 to set 2 point Cal. HIGH point",
        "read_write": "NV",
        "register": 596,
        "register_hex": "0x0254"
    },
    "SET_TCAL_2_POINT_LOW": {
        "data_type": "R",
        "description": "Write 1 to set 2 point Cal. LOW point",
        "read_write": "NV",
        "register": 595,
        "register_hex": "0x0253"
    },
    "SMART_OUTPUT_VERSION": {
        "data_type": "L",
        "description": "Smart Output Module Version",
        "read_write": "R",
        "register": 522,
        "register_hex": "0x020a"
    },
    "SMART_SENSOR_PRESET": {
        "data_type": "R",
        "description": "Enumerated Toggle",
        "read_write": "R",
        "register": 656,
        "register_hex": "0x0290"
    },
    "SMART_SENSOR_READING_1": {
        "data_type": "F",
        "description": "Sensor 1 Input",
        "read_write": "R",
        "register": 658,
        "register_hex": "0x0292"
    },
    "SMART_SENSOR_READING_2": {
        "data_type": "F",
        "description": "",
        "read_write": "R",
        "register": 659,
        "register_hex": "0x0294"
    },
    "SMART_SENSOR_READING_3": {
        "data_type": "F",
        "description": "",
        "read_write": "R",
        "register": 660,
        "register_hex": "0x0296"
    },
    "SMART_SENSOR_READING_4": {
        "data_type": "F",
        "description": "",
        "read_write": "R",
        "register": 661,
        "register_hex": "0x0298"
    },
    "SMART_SENSOR_SELECT": {
        "data_type": "R",
        "description": "Selects active Sensor input ",
        "read_write": "NV",
        "register": 657,
        "register_hex": "0x0291"
    },
    "SMART_SENSOR_VALUE": {
        "data_type": "F",
        "description": "Currently selected Smart Sensor value",
        "read_write": "R",
        "register": 534,
        "register_hex": "0x0216"
    },
    "SOAK_ACTION": {
        "data_type": "R",
        "description": "Enumerated - Soak Action ",
        "read_write": "NV",
        "register": 613,
        "register_hex": "0x0265"
    },
    "SOAK_EVENT": {
        "data_type": "R",
        "description": "SE.ON flag set for current segment",
        "read_write": "NV",
        "register": 617,
        "register_hex": "0x0269"
    },
    "SOAK_LINK": {
        "data_type": "R",
        "description": "Profile to link to after current profile",
        "read_write": "NV",
        "register": 614,
        "register_hex": "0x0266"
    },
    "SOAK_PROCESS_VALUE": {
        "data_type": "F",
        "description": "Target SOAK setpoint for current segment",
        "read_write": "NV",
        "register": 618,
        "register_hex": "0x026a"
    },
    "SOAK_TIME": {
        "data_type": "L",
        "description": "Time (msec) to hold at SOAK setpoint",
        "read_write": "NV",
        "register": 622,
        "register_hex": "0x026e"
    },
    "SYSTEM_STATUS": {
        "data_type": "L",
        "description": "Enumerated Status information",
        "read_write": "R",
        "register": 516,
        "register_hex": "0x0204"
    },
    "TARE_MODE": {
        "data_type": "R",
        "description": "Tare Mode",
        "read_write": "NV",
        "register": 653,
        "register_hex": "0x028d"
    },
    "TARE_RESET": {
        "data_type": "R",
        "description": "Write 1 to force TARE Display Functions",
        "read_write": "W",
        "register": 582,
        "register_hex": "0x0246"
    },
    "TCAL_1_POINT_OFFSET": {
        "data_type": "F",
        "description": "Stored 1 point CAL offset",
        "read_write": "NV",
        "register": 602,
        "register_hex": "0x025a"
    },
    "TCAL_2_POINT_GAIN": {
        "data_type": "F",
        "description": "Stored 2 point CAL gain Ramp & Soak (Sequencer)",
        "read_write": "NV",
        "register": 606,
        "register_hex": "0x025e"
    },
    "TCAL_2_POINT_OFFSET": {
        "data_type": "F",
        "description": "Stored 2 point CAL offset",
        "read_write": "NV",
        "register": 604,
        "register_hex": "0x025c"
    },
    "TCAL_ICE_POINT_OFFSET": {
        "data_type": "F",
        "description": "Stored ICE POINT offset",
        "read_write": "NV",
        "register": 600,
        "register_hex": "0x0258"
    },
    "TCAL_TYPE": {
        "data_type": "R",
        "description": "Enumerated value indicating type of TCAL",
        "read_write": "NV",
        "register": 592,
        "register_hex": "0x0250"
    },
    "TC_TYPE": {
        "data_type": "R",
        "description": "Enumerated Thermocouple type",
        "read_write": "NV",
        "register": 643,
        "register_hex": "0x0283"
    },
    "THERMISTOR_VALUE": {
        "data_type": "R",
        "description": "Enumerated Thermistor type",
        "read_write": "NV",
        "register": 646,
        "register_hex": "0x0286"
    },
    "TIME_FORMAT": {
        "data_type": "R",
        "description": "Enumerated value to indicate time format",
        "read_write": "NV",
        "register": 588,
        "register_hex": "0x024c"
    },
    "TRACKING_TYPE": {
        "data_type": "R",
        "description": "Enumerated - R&S tracking type",
        "read_write": "NV",
        "register": 615,
        "register_hex": "0x0267"
    },
    "USB_CONTINUOUS_DATA_PERIOD": {
        "data_type": "F",
        "description": "Time interval in continuous mode (0.1 sec)",
        "read_write": "NV",
        "register": 1540,
        "register_hex": "0x0604"
    },
    "USB_DATA_FLOW": {
        "data_type": "R",
        "description": "Enumerated Data Flow (Omega mode)",
        "read_write": "NV",
        "register": 1538,
        "register_hex": "0x0602"
    },
    "USB_DATA_FORMAT_PEAK": {
        "data_type": "R",
        "description": "Enumerated Toggle value",
        "read_write": "NV",
        "register": 1544,
        "register_hex": "0x0608"
    },
    "USB_DATA_FORMAT_READING": {
        "data_type": "R",
        "description": "Enumerated Toggle value",
        "read_write": "NV",
        "register": 1543,
        "register_hex": "0x0607"
    },
    "USB_DATA_FORMAT_STATUS": {
        "data_type": "R",
        "description": "Enumerated Toggle value",
        "read_write": "NV",
        "register": 1542,
        "register_hex": "0x0606"
    },
    "USB_DATA_FORMAT_UNIT": {
        "data_type": "R",
        "description": "Enumerated Toggle value",
        "read_write": "NV",
        "register": 1546,
        "register_hex": "0x060a"
    },
    "USB_DATA_FORMAT_VALLEY": {
        "data_type": "R",
        "description": "Enumerated Toggle value",
        "read_write": "NV",
        "register": 1545,
        "register_hex": "0x0609"
    },
    "USB_DEVICE_ADDRESS": {
        "data_type": "R",
        "description": "Byte address (0..255)",
        "read_write": "NV",
        "register": 1549,
        "register_hex": "0x060d"
    },
    "USB_ECHO_MODE": {
        "data_type": "R",
        "description": "Enumerated Toggle value",
        "read_write": "NV",
        "register": 1539,
        "register_hex": "0x0603"
    },
    "USB_LINE_FEED": {
        "data_type": "R",
        "description": "Enumerated Toggle value",
        "read_write": "NV",
        "register": 1548,
        "register_hex": "0x060c"
    },
    "USB_MODBUS_EOL": {
        "data_type": "R",
        "description": "2 character EOL character string (CR/LF)",
        "read_write": "NV",
        "register": 1551,
        "register_hex": "0x060f"
    },
    "USB_MODBUS_MODE": {
        "data_type": "R",
        "description": "Enumerated Modbus mode",
        "read_write": "NV",
        "register": 1550,
        "register_hex": "0x060e"
    },
    "USB_PROTOCOL": {
        "data_type": "R",
        "description": "Enumerated Comm Mode",
        "read_write": "NV",
        "register": 1536,
        "register_hex": "0x0600"
    },
    "USB_RECOGNITION_CHARACTER": {
        "data_type": "R",
        "description": "Recognition character",
        "read_write": "NV",
        "register": 1537,
        "register_hex": "0x0601"
    },
    "USB_SEPARATION_CHAR": {
        "data_type": "R",
        "description": "Enumerated Separation character",
        "read_write": "NV",
        "register": 1547,
        "register_hex": "0x060b"
    },
    "VALLEY_VALUE": {
        "data_type": "F",
        "description": "Minimum Value processed",
        "read_write": "RW",
        "register": 552,
        "register_hex": "0x0228"
    },
    "VERSION_NUMBER": {
        "data_type": "L",
        "description": "Version Number",
        "read_write": "R",
        "register": 514,
        "register_hex": "0x0202"
    }
}
