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
from time import sleep
from enum import Enum


class Joints(Enum):
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

UPDATE_TIME_DELAY = 0.007


class Snapper:

    def __init__(self):
        print "Creating Snapper interface"
        self.pwm = PWM()
        self.pwm.setPWMFreq(PWM_FREQ)

        print "Pulse Length: {0}".format(PULSE_LENGTH)

        self.waist_position = 0
        self.shoulder_position = 0
        self.elbow_position = 0
        self.wrist_position = 0
        self.gripper_position = 50

        self.initialize_position()

    def initialize_position(self):
        self.center()
        sleep(1)

    def center(self):
        """
        Sets all servos to their centered positions
        :return: None
        """
        self.pwm.setPWM(Joints.WAIST, 0, int(CENTER / PULSE_LENGTH))
        self.pwm.setPWM(Joints.SHOULDER, 0, int(CENTER / PULSE_LENGTH))
        self.pwm.setPWM(Joints.ELBOW, 0, int(CENTER / PULSE_LENGTH))
        self.pwm.setPWM(Joints.WRIST, 0, int(CENTER / PULSE_LENGTH))
        self.pwm.setPWM(Joints.GRIPPER, 0, int(CENTER / PULSE_LENGTH))

    def stow(self):
        """
        Sets all servos to a compact position suitable for unpowered movement
        :return: None
        """
        self.set_joints({
            Joints.WAIST: 0,
            Joints.SHOULDER: -80,
            Joints.ELBOW: -65,
            Joints.WRIST: -30,
            Joints.GRIPPER: 40
        })

    def _query_duration(self, current_joint_position, target_position):
        step = 1 if current_joint_position > target_position else -1
        rng = range(current_joint_position, target_position, step)
        # Total move time is the number of steps * the time per step, plus an extra step time as a buffer
        return len(rng) * UPDATE_TIME_DELAY + UPDATE_TIME_DELAY

    def waist_move_duration(self, degrees):
        return self._query_duration(self.waist_position, degrees)

    def shoulder_move_duration(self, degrees):
        return self._query_duration(self.shoulder_position, degrees)

    def elbow_move_duration(self, degrees):
        return self._query_duration(self.elbow_position, degrees)

    def wrist_move_duration(self, degrees):
        return self._query_duration(self.wrist_position, degrees)

    def gripper_move_duration(self, percentage):
        return self._query_duration(self.gripper_position, percentage)

    def set_waist(self, degrees=0):
        """
        Rotates the waist joint to the specified angle
        :param degrees: clamped to [-90, 90]
        :return: Duration of the commanded motion, in seconds
        """
        start_position = self.waist_position
        step = 1 if degrees > start_position else -1
        travel = range(start_position, degrees, step)

        print "Moving waist from {0} to {1}".format(start_position, degrees)
        for i in travel:
            value = _interpolate_arm(i)
            self.pwm.setPWM(Joints.WAIST, 0, value)
            self.waist_position = i
            print "Update waist to {0} degrees".format(self.waist_position)
            sleep(UPDATE_TIME_DELAY)

    def set_shoulder(self, degrees=0):
        """
        Rotates the shoulder joint to the specified angle
        :param degrees: clamped to [-90, 90]
        :return: None
        """
        start_position = self.shoulder_position
        step = 1 if degrees > start_position else -1
        travel = range(start_position, degrees, step)

        print "Moving shoulder from {0} to {1}".format(start_position, degrees)
        for i in travel:
            value = _interpolate_arm(i)
            self.pwm.setPWM(Joints.SHOULDER, 0, value)
            self.shoulder_position = i
            print "Update waist to {0} degrees".format(self.shoulder_position)
            sleep(UPDATE_TIME_DELAY)

    def set_elbow(self, degrees=0):
        """
        Rotates the elbow joint to the specified angle
        :param degrees: clamped to [-90. 90]
        :return: None
        """
        start_position = self.elbow_position
        step = 1 if degrees > start_position else -1
        travel = range(start_position, degrees, step)

        print "Moving elbow from {0} to {1}".format(start_position, degrees)
        for i in travel:
            value = _interpolate_arm(i)
            self.pwm.setPWM(Joints.ELBOW, 0, value)
            self.elbow_position = i
            print "Update elbow to {0} degrees".format(self.elbow_position)
            sleep(UPDATE_TIME_DELAY)

    def set_wrist(self, degrees=0):
        """
        Rotates the wrist joint to the specified angle
        :param degrees: clamped to [-90, 90]
        :return: None
        """
        start_position = self.wrist_position
        step = 1 if degrees > start_position else -1
        travel = range(start_position, degrees, step)

        print "Moving wrist from {0} to {1}".format(start_position, degrees)
        for i in travel:
            value = _interpolate_arm(i)
            self.pwm.setPWM(Joints.WRIST, 0, value)
            self.wrist_position = i
            print "Update waist to {0} degrees".format(self.wrist_position)
            sleep(UPDATE_TIME_DELAY)

    def set_gripper(self, percentage):
        """
        Sets the gripper to the specified open percentage
        :param percentage: clamped [0, 100] where 0 is completely closed and 100 is completely open
        :return:
        """
        start_position = self.gripper_position
        step = 1 if percentage > start_position else -1
        travel = range(start_position, percentage, step)

        print "Moving gripper from {0} to {1}".format(start_position, percentage)
        for i in travel:
            value = _interpolate_arm(i)
            self.pwm.setPWM(Joints.GRIPPER, 0, value)
            self.gripper_position = i
            print "Update gripper to {0} degrees".format(self.gripper_position)
            sleep(UPDATE_TIME_DELAY)

    def set_joints(self, joint_values):
        """
        Set multiple joints at once in a batch.
        :param joint_values: Dictionary of values from Joints enum
        :return: None
        """
        desired_waist = joint_values.get(Joints.WAIST, self.waist_position)
        desired_wrist = joint_values.get(Joints.WRIST, self.wrist_position)
        desired_shoulder = joint_values.get(Joints.SHOULDER, self.shoulder_position)
        desired_elbow = joint_values.get(Joints.ELBOW, self.elbow_position)
        desired_gripper = joint_values.get(Joints.GRIPPER, self.gripper_position)

        waist_step = 1 if desired_waist > self.waist_position else -1
        wrist_step = 1 if desired_wrist > self.wrist_position else -1
        shoulder_step = 1 if desired_shoulder > self.shoulder_position else -1
        elbow_step = 1 if desired_elbow > self.elbow_position else -1
        gripper_step = 1 if desired_gripper > self.gripper_position else -1

        waist_range = range(self.waist_position, desired_waist, waist_step)
        wrist_range = range(self.wrist_position, desired_wrist, wrist_step)
        shoulder_range = range(self.shoulder_position, desired_shoulder, shoulder_step)
        elbow_range = range(self.elbow_position, desired_elbow, elbow_step)
        gripper_range = range(self.gripper_position, desired_gripper, gripper_step)

        max_steps = max(len(waist_range), len(wrist_range), len(shoulder_range), len(elbow_range), len(gripper_range))

        # Normalize number of steps and recalculate ranges
        interp_waist_range = []
        waist_order = [self.waist_position, desired_waist] if waist_step == 1 else [desired_waist, self.waist_position]

        interp_wrist_range = []
        wrist_order = [self.wrist_position, desired_wrist] if wrist_step == 1 else [desired_wrist, self.wrist_position]

        interp_elbow_range = []
        elbow_order = [self.elbow_position, desired_elbow] if elbow_step == 1 else [desired_elbow, self.elbow_position]

        interp_shoulder_range = []
        shoulder_order = [self.shoulder_position, desired_shoulder] if shoulder_step == 1 else [desired_shoulder, self.shoulder_position]

        interp_gripper_range = []
        gripper_order = [self.gripper_position, desired_gripper] if gripper_step == 1 else [desired_gripper, self.gripper_position]

        for i in range(max_steps):
            interp_waist_range.append(int(interp(i, [0, max_steps], waist_order)))
            interp_wrist_range.append(int(interp(i, [0, max_steps], wrist_order)))
            interp_elbow_range.append(int(interp(i, [0, max_steps], elbow_order)))
            interp_shoulder_range.append(int(interp(i, [0, max_steps], shoulder_order)))
            interp_gripper_range.append(int(interp(i, [0, max_steps], gripper_order)))

        # Now, if we were in reversed order for the interpolation we flip back
        if wrist_step == -1:
            interp_wrist_range.reverse()

        if waist_step == -1:
            interp_waist_range.reverse()

        if elbow_step == -1:
            interp_elbow_range.reverse()

        if shoulder_step == -1:
            interp_shoulder_range.reverse()

        if gripper_step == -1:
            interp_gripper_range.reverse()

        # Finally, send each joint a PWM command and delay
        for i in range(max_steps):
            waist = interp_waist_range[i]
            update = _interpolate_arm(waist)
            self.pwm.setPWM(Joints.WAIST, 0, update)
            self.waist_position = waist

            wrist = interp_wrist_range[i]
            update = _interpolate_arm(wrist)
            self.pwm.setPWM(Joints.WRIST, 0, update)
            self.wrist_position = wrist

            shoulder = interp_shoulder_range[i]
            update = _interpolate_arm(shoulder)
            self.pwm.setPWM(Joints.SHOULDER, 0, update)
            self.shoulder_position = shoulder

            elbow = interp_elbow_range[i]
            update = _interpolate_arm(elbow)
            self.pwm.setPWM(Joints.ELBOW, 0, update)
            self.elbow_position = elbow

            gripper = interp_gripper_range[i]
            update = _interpolate_gripper(gripper)
            self.pwm.setPWM(Joints.GRIPPER, 0, update)
            self.gripper_position = gripper

            sleep(UPDATE_TIME_DELAY)

        # Normalize the number of steps and recompute ranges

        print "Setting desired_waist to {0}, desired_wrist to {1}".format(desired_waist, desired_wrist)


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
