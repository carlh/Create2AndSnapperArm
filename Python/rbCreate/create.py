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


class Create:
    """
    Create encapsulates the communication between client code and the iRobot Create 2 robot.
    We don't attempt to provide a full API interface, but we implement functions as needed for
    our project.

    Inspired by http://www.rose-hulman.edu/Users/faculty/young/CS-Classes/binaries/Python/FIXME/create.py,
    a library designed for the iRobot Create 1
    """
    BAUDRATE = 115200

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

    def connect(self):
        """
        Open the connection to the iRobot Create 2 and put in Safe mode.

        :return: None
        """
        if self.connected is True:
            return True  # Return early if we're already connected

        with self.portLock:
            try:
                self.connection = serial.Serial(
                    port=self.port,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    baudrate=self.BAUDRATE
                )
            except serial.SerialException as msg:
                print msg
                print "Please choose from the list below: "
                print [port.device for port in serial.tools.list_ports.comports()]
                return

            self.connected = True
            return self.connection.is_open

    def disconnect(self):
        """
        If the connection is open, close it

        :return: None
        """

        if self.connected is not True:
            return

        self.connection.close()

    def send(self, command, parambytes=None):
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
                # tkMessageBox.showerror('Not connected!', 'Not connected to robot')
                print "Not Connected"
        except serial.SerialException:
            print "Lost Connection"
            # tkMessageBox.showinfo('Uh-oh', "Lost connection to the robot!")
            self.connection = None
