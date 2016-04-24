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
import argparse
import atexit
import json
import sys
from time import sleep

from rbCreate import Create
from rbSnapper import Snapper
from rbSnapper import Joints

# This configuration places the gripper on the floor 4 inches in front of the Create
front_floor_position = {
    Joints.WAIST: 0,
    Joints.SHOULDER: 80,
    Joints.ELBOW: 20,
    Joints.WRIST: 0,
}

home_position = {
    Joints.WAIST: 0,
    Joints.SHOULDER: 0,
    Joints.ELBOW: 0,
    Joints.WRIST: 0
}

gripper = {
    'closed': 40,
    'open': 99
}


def close_connection(robot, arm):
    """
    Ensure that we close the connection to the create when the script exits.  This should prevent us from leaving
    the Create in Safe or Full mode, which prevent sleeping and charging and allow the battery to drain completely.
    :param robot:
    :return:
    """
    if robot is not None:
        robot.stop_motion()
        robot.stop()
        robot.disconnect()

    if arm is not None:
        arm.stow()


def pick_up_brick(arm):
    position = front_floor_position
    position[Joints.GRIPPER] = gripper['open']
    arm.set_joints(position)
    sleep(2)
    arm.set_gripper(gripper['closed'])
    arm.stow()


def put_down_brick(arm):
    position = front_floor_position
    position[Joints.GRIPPER] = gripper['closed']
    arm.set_joints(front_floor_position)
    sleep(1)
    arm.set_gripper(gripper['open'])
    sleep(1)
    arm.stow()


def build_wall(create, arm):
    """
    This is the main method that is called to drive the create between the source and target locations
    :param create: The instance of the Create that will be controlled
    :param arm: The instance of the Snapper arm
    :return: None
    """

    # We assume that we start right in front of the first brick
    forward_speed = 100  # The speed with which to drive forward
    forward_drive_duration = 2  # The amount of time to drive in a straight line
    iteration_delta = 0.3  # The amount to increase the forward drive time per iteration
    iteration_buffer = 0.0  # The total amount of time to add to the base forward drive time
    rotation_speed = 124  # The speed with which to rotate in place (mm/s)
    rotation_duration = 3.18  # The amount of time to spin
    
    for _ in range(3):
        pick_up_brick(arm)

        create.drive_direct(rotation_speed, -rotation_speed)
        sleep(rotation_duration)

        create.drive_direct(forward_speed, forward_speed)
        sleep(forward_drive_duration + iteration_buffer)

        create.stop_motion()
        put_down_brick(arm)

        create.drive_direct(-rotation_speed, rotation_speed)
        sleep(rotation_duration)

        create.drive_direct(forward_speed, forward_speed)
        iteration_buffer += iteration_delta
        sleep(forward_drive_duration + iteration_buffer)

        create.stop_motion()
        iteration_buffer += iteration_delta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--config", help="the path to the JSON formatted config file specifying the serial port to use")
    ap.add_argument("-s", "--serial", help="the serial port to use")
    ap.add_argument("-t", "--test", help="Use a mocked serial connection to debug or test locally")
    args = vars(ap.parse_args())

    if not (args["config"] or args["serial"]) and not args["test"]:
        print "You must specify either the config file or the serial port to use"
        return -1

    port = {}
    test = False
    if args["serial"]:
        port = args["serial"]
    elif args["test"]:
        port = -1
        test = True
    elif args["config"]:
        try:
            conf = json.load(open(args["config"]))
            port = conf["port"]
        except IOError as err:
            print "An IO Exception occurred: {0}".format(err)
            return -1

    # Initialize the Create robot and arm
    try:
        robot = Create(port)
        robot.connect(test)
        robot.set_safe_mode()

        arm = Snapper()

        atexit.register(close_connection, robot, arm)

        build_wall(robot, arm)

    except RuntimeError as err:
        print "A RuntimeError occurred while communicating with the Connect 2: {0}".format(err)
        return -1

    return 0

if __name__ == "__main__":
    sys.exit(main())
