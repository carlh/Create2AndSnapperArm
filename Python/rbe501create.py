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
from rbCreate import Create
import argparse
import json
import atexit
import sys
from time import sleep

def close_connection(robot):
    """
    Ensure that we close the connection to the create when the script exits.  This should prevent us from leaving
    the Create in Safe or Full mode, which prevent sleeping and charging and allow the battery to drain completely.
    :param robot:
    :return:
    """
    if robot is not None:
        robot.disconnect()


def test_sequence(robot):
    """
    Define movement routines here for testing

    :param robot: The Create object
    :return: None
    """
    robot.stop()
    sleep(4)
    robot.start()
    robot.return_to_dock()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--config", help="the path to the JSON formatted config file specifying the serial port to use")
    ap.add_argument("-s", "--serial", help="the serial port to use")
    args = vars(ap.parse_args())

    if not (args["config"] or args["serial"]):
        print "You must specify either the config file or the serial port to use"
        return -1

    port = {}
    if args["serial"]:
        port = args["serial"]
    elif args["config"]:
        try:
            conf = json.load(open(args["config"]))
            port = conf["port"]
        except IOError as err:
            print "An IO Exception occurred: {0}".format(err)
            return -1

    # Initialize the Create robot
    try:
        robot = Create(port)
        robot.connect()
        atexit.register(close_connection, robot)
        test_sequence(robot)
    except RuntimeError as err:
        print "A RuntimeError occurred while communicating with the Connect 2: {0}".format(err)
        return -1

    return 0

if __name__ == "__main__":
    sys.exit(main())
