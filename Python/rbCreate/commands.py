"""
    The MIT License (MIT)
    Copyright (c) 2016 Carl Hinkle <cghinkle427@gmail.com>

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
    documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
    rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
    permit persons to whom the Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial portions of
    the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
    THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
    TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""
# This file contains the constants that will be used to send and receive commands from the Connect 2



# States
STATE_START = '128'  # [Passive, Save, Full]
STATE_RESET = '7'  # [All]
STATE_STOP = '173'  # [Passive, Safe, Full]

# Modes
MODE_SAFE = '131'
MODE_FULL = '132'
MODE_PASSIVE = STATE_START  # For API coherence

# Baud - Must wait 100ms after sending this before issuing new commands
BAUD = '129'  # + Baud code [Passive, Safe, Full]
BAUD_300 = '0'
BAUD_600 = '1'
BAUD_1200 = '2'
BAUD_2400 = '3'
BAUD_4800 = '4'
BAUD_9600 = '5'
BAUD_14400 = '6'
BAUD_19200 = '7'
BAUD_28800 = '8'
BAUD_38400 = '9'
BAUD_57600 = '10'
BAUD_115200 = '11'

BAUDRATE_CONNECTION_DEFAULT = 115200  # Default startup baudrate
BAUDRATE_CONNECTION_SLOW = 19200  # For slower connections

# Commands
RETURN_TO_DOCK = '143'  # Seek the home base and begin charging, setting mode to Passive
