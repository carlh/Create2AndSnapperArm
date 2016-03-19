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
try:
    from Adafruit_PWM_Servo_Driver import PWM
except ImportError:
    from FakePWM import PWM

from numpy import interp

WAIST = 0
SHOULDER = 1
ELBOW = 2
WRIST = 3
GRIPPER = 4

PWM_FREQ = 50.0

PULSE_LENGTH = 1000000.0 / PWM_FREQ / 4096

ARM_MIN = 600   # Minimum pulse width for the lower joints, fully counter-clockwise
ARM_MAX = 2400  # Maximum pulse width for the lower joints, fully clockwise

GRIPPER_MIN = 750  # Minimum pulse width for the gripper.  Very important that the gripper servo does NOT go below this or we risk breakage
GRIPPER_MAX = 2400  # Maximum pulse width for the gripper.

CENTER = 1500  # Pulse with for zeroed position


class Snapper:

    def __init__(self):
        print "Creating Snapper interface"
        self.pwm = PWM()
        self.pwm.setPWMFreq(PWM_FREQ)

        print "Pulse Length: {0}".format(PULSE_LENGTH)

        self.center()

    def center(self):
        """
        Sets all servos to their centered positions
        :return: None
        """
        self.pwm.setPWM(WAIST, 0, int(CENTER / PULSE_LENGTH))
        self.pwm.setPWM(SHOULDER, 0, int(CENTER / PULSE_LENGTH))
        self.pwm.setPWM(ELBOW, 0, int(CENTER / PULSE_LENGTH))
        self.pwm.setPWM(WRIST, 0, int(CENTER / PULSE_LENGTH))
        self.pwm.setPWM(GRIPPER, 0, int(CENTER / PULSE_LENGTH))

    def stow(self):
        """
        Sets all servos to a compact position suitable for unpowered movement
        :return: None
        """
        self.set_waist(0)
        self.set_shoulder(-80)
        self.set_elbow(-65)
        self.set_wrist(-30)

    def set_waist(self, degrees=0):
        """
        Rotates the waist joint to the specified angle
        :param degrees: clamped to [-90, 90]
        :return: None
        """
        value = _interpolate_arm(degrees)
        self.pwm.setPWM(WAIST, 0, value)

    def set_shoulder(self, degrees=0):
        """
        Rotates the shoulder joint to the specified angle
        :param degrees: clamped to [-90, 90]
        :return: None
        """
        value = _interpolate_arm(degrees)
        self.pwm.setPWM(SHOULDER, 0, value)

    def set_elbow(self, degrees=0):
        """
        Rotates the elbow joint to the specified angle
        :param degrees: clamped to [-90. 90]
        :return: None
        """
        value = _interpolate_arm(degrees)
        print "Setting Elbow to {0} degrees, PWM {1}".format(degrees, value)
        self.pwm.setPWM(ELBOW, 0, value)

    def set_wrist(self, degrees=0):
        """
        Rotates the wrist joint to the specified angle
        :param degrees: clamped to [-90, 90]
        :return: None
        """
        value = _interpolate_arm(degrees)
        self.pwm.setPWM(WRIST, 0, value)

    def set_gripper(self, percentage):
        """
        Sets the gripper to the specified open percentage
        :param percentage: clamped [0, 100] where 0 is completely closed and 100 is completely open
        :return:
        """
        value = _interpolate_gripper(percentage)
        self.pwm.setPWM(GRIPPER, 0, value)


def _interpolate_arm(degrees):
    if degrees < -90:
        degrees = -90
    elif degrees > 90:
        degrees = 90

    return int(interp(degrees, [-90, 90], [ARM_MIN, ARM_MAX]) / PULSE_LENGTH)


def _interpolate_gripper(percentage):
    if percentage < 0:
        percentage = 0
    elif percentage > 100:
        percentage = 100

    return int(interp(percentage, [0, 100], [GRIPPER_MIN, GRIPPER_MAX]) / PULSE_LENGTH)
