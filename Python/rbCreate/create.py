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

import thread
import serial
import serial.tools.list_ports
import time
import commands
from options import *
import numpy as np
from testing.mock_serial import MockSerial


class Create:
    """
    Create encapsulates the communication between client code and the iRobot Create 2 robot.
    We don't attempt to provide a full API interface, but we implement functions as needed for
    our project.

    Inspired by http://www.rose-hulman.edu/Users/faculty/young/CS-Classes/binaries/Python/FIXME/create.py,
    a library designed for the iRobot Create 1
    """

#region Construction and Initialization
    def __init__(self, port):
        """
        Construct a new instance of the Create robot.

        Args:
            port (String):  The serial port that the Create is connected to. On Windows this should be of the
                            form 'COMX', while on Unix based platforms it should be the full path descriptor.
                            The path descriptor can be found by running 'ls /dev/tty.*'
        """
        if port is None:
            raise RuntimeError("Must provide the identifier of the serial port used to communicate with the Create 2")
        self.port = port
        self.connected = False
        self.connection = None
        self.portLock = thread.allocate_lock()

    def connect(self, test=False):
        """
        Open the connection to the iRobot Create 2 and put in Safe mode.

        :param test: If true, the connection will be faked.  This allows running the code in testing and debugging without actually
                        plugging into the Connect 2
        :return: None
        """
        if self.connected is True:
            return True  # Return early if we're already connected

        with self.portLock:
            try:
                if test:
                    self.connection = MockSerial(
                        port=self.port,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        baudrate=commands.BAUDRATE_CONNECTION_DEFAULT)
                else:
                    self.connection = serial.Serial(
                        port=self.port,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        baudrate=commands.BAUDRATE_CONNECTION_DEFAULT,
                    )
            except serial.SerialException as msg:
                print msg
                print "Please choose from the list below: "
                print [port.device for port in serial.tools.list_ports.comports()]
                raise RuntimeError("Must select valid serial port")

        self.connected = True
        self.start()
        return self.connection.is_open

    def disconnect(self):
        """
        If the connection is open, close it
        :return: None
        """
        if self.connected is not True:
            return

        self._send(commands.MODE_PASSIVE)
        self.connection.close()
#endregion

#region Modes
    def set_safe_mode(self):
        """
        Sets the Create 2 to Safe mode.

        In Safe mode you have full control of the Create 2, except as follows:
            - Cliff sensors
            - Charger plugged in
            - Wheel drop
        If any of these conditions occur, the Create 2 stops motion and returns to Passive mode.
        """
        self._send(commands.MODE_SAFE)

    def set_full_mode(self):
        """
        Sets the Create 2 to Full mode.

        This is complete control over the Create 2, and it will not respond to the safety related sensors that
        are active in Safe mode.

        To exit Full mode, call :setSafeMode:
        """
        self._send(commands.MODE_FULL)
#endregion

#region Lifecycle Methods

    def start(self):
        """
        Starts the Create 2's Open Interface.  This is called automatically on connecting, and must be called manually
        after calling reset.
        """
        self._send(commands.STATE_START)

    def reset(self):
        """
        Resets the robot, as if the battery had been removed.  You must call @ref(start) to resume sending commands.
        """
        self._send(commands.STATE_RESET)

    def stop(self):
        """
        Stops the robot and changes mode to OFF.  Create plays a tone.  You must call @ref(start) to resume sending commands.
        :return:
        """
        self._send(commands.STATE_STOP)

#endregion

#region Predefined Routines

    def return_to_dock(self):
        """
        Exit the current command and seek the dock.  This changes the mode to Passive.
        """
        self._send(commands.RETURN_TO_DOCK)

#endregion

#region Actuation
    def drive(self, direction=DriveDirection.Standstill, speed=0, turn_direction=TurnDirection.Straight, turn_radius=0):
        """
        This method gives you direct control over the Create's wheel actuators.
        :param direction: Use value from DriveDirection enum
        :param speed: (mm/s) The average velocity of the Create2. Clamped to [0, 500]
        :param turn_direction: Use value from TurnDirection
        :param turn_radius: (mm) The radius through which the Create will turn. Clamped to [0, 2000]
        :return:
        """

        print "Testing"

    def drive_straight_forward(self, speed=0):
        """
        Drives straight forward
        :param speed: (mm/s) The average velocity of the Create2.  Clamped to [0, 500]
        :return: None
        """
        self.drive(direction=DriveDirection.Forward, speed=speed, turn_direction=TurnDirection.Straight, turn_radius=0)

    def drive_straight_reverse(self, speed=0):
        """
        Drives straight in reverse
        :param speed: (mm/s) The average velocity of the Create2.  Clamped to [0, 500]
        :return: None
        """
        self.drive(direction=DriveDirection.Reverse, speed=speed, turn_direction=TurnDirection.Straight, turn_radius=0)

    def stop_motion(self):
        """
        Command the Create2 to stop in place
        :return: None
        """
        self.drive(direction=DriveDirection.Standstill, speed=0, turn_direction=TurnDirection.Straight, turn_radius=0)
#endregion

#region Private Methods
    def _send(self, command, parambytes=None):
        """
        Send a command to the iRobot Create 2.

        :param command: The command to send.  Use an entry from the Commands dictionary.
        :param parambytes: If the command requires additional bytes, you MUST pass them here or else the Create will hang
        """
        if self.connected is not True:
            raise RuntimeError("You must call connect before sending commands to to Create 2")
        cmd = command
        if parambytes is not None:
            cmd += parambytes
        self._send_command_ascii(cmd)

    def _send_command_ascii(self, command):
        cmd = ""
        for v in command.split():
            cmd += chr(int(v))
        self._send_command_raw(cmd)

    def _send_command_raw(self, cmd):
        try:
            if self.connection is not None:
                with self.portLock:
                    self.connection.write(cmd)
            else:
                print "Not Connected"
        except serial.SerialException:
            print "Lost Connection"
            self.connection = None
#endregion
