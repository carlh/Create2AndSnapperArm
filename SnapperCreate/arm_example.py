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
import atexit
import os
import sys

from time import sleep

from rbSnapper import Snapper
from rbSnapper import Joints

# This configuration places the gripper on the floor 4 inches in front of the Create
front_floor_position = {
    Joints.WAIST: 0,
    Joints.SHOULDER: 80,
    Joints.ELBOW: 20,
    Joints.WRIST: 0,
}


def close_connection(arm):
    """
    Ensure that we close the connection to the create when the script exits.  This should prevent us from leaving
    the Create in Safe or Full mode, which prevent sleeping and charging and allow the battery to drain completely.
    :param arm:
    :return:
    """
    if arm is not None:
        arm.stow()


def pick_up_in_front(arm):
    arm.set_gripper(99)
    sleep(0.5)
    arm.set_joints(front_floor_position)
    sleep(20)
    arm.set_gripper(40)
    sleep(1)
    arm.stow()


def put_down_in_front(arm):
    arm.set_joints(front_floor_position)
    sleep(1)
    arm.set_gripper(99)
    sleep(0.5)
    arm.stow()


def test_arm_motions(arm):
    arm.center()
    sleep(1)

    arm.set_waist(45)
    sleep(1)

    arm.set_waist(-45)
    sleep(1)

    arm.set_waist(0)
    sleep(1)

    arm.set_elbow(45)
    sleep(2)
    arm.set_elbow(-45)
    sleep(2)
    arm.set_elbow(0)
    sleep(2)

    arm.set_gripper(10)
    sleep(2)
    arm.set_gripper(90)
    sleep(2)
    arm.set_gripper(50)
    sleep(2)

    arm.set_shoulder(45)
    sleep(2)
    arm.set_shoulder(-45)
    sleep(2)
    arm.set_shoulder(0)
    sleep(2)

    arm.set_wrist(45)
    sleep(2)
    arm.set_wrist(-45)
    sleep(2)
    arm.set_wrist(0)
    sleep(2)
    joints = {
        Joints.WAIST: 40,
        Joints.SHOULDER: 65,
        Joints.ELBOW: -20,
        Joints.WRIST: 70,
        Joints.GRIPPER: 65,
    }

    arm.set_joints(joints)


def main():
    try:
        arm = Snapper()
        atexit.register(close_connection, arm)
        pick_up_in_front(arm)

    except RuntimeError as err:
        print "A RuntimeError occurred while testing the Snapper motion {0}".format(err)
        return -1
    return 0

if __name__ == "__main__":
    sys.exit(main())
