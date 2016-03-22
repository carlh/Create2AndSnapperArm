# README

## Description

rbCreate is a Python 2.7 based interface to the iRobot Create 2.  Using this library, you can
send commands to or read the sensors of the Create 2.  For example, you could create a program that
lets you drive the Create 2 from your keyboard, or you could create a program that uses the Create 2's
sensors to take autonomous actions.

## Environment Setup

Install Python 2.7 and Pip in the usual way, then pip install the following packages:

- numpy
- pyserial
- requests
- urllib
- wheel
- enum

## Executing

Begin by importing the Create package

    from rbCreate import Create

Next, determine the serial port that your Create2 is connected to, then instantiate an instance of the Create

    # Initialize the Create robot
    robot = Create("YOUR TTY PATH")
    robot.connect()

(WIP) This will connect your robot instance to your Create 2.  Now you can send it commands.  For example,

    robot.send('128 131 143')

will start your Create 2, set it to Safe mode, and send it the Seek Dock command.  Note that this functionality will
be enhanced greatly in the near future.
