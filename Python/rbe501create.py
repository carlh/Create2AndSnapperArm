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

from drivers import BasicDrive
from drivers import ManualSteering

from rbCreate import Create


def close_connection(robot):
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--config", help="the path to the JSON formatted config file specifying the serial port to use")
    ap.add_argument("-s", "--serial", help="the serial port to use")
    ap.add_argument("-t", "--test", help="Use a mocked serial connection to debug or test locally")
    ap.add_argument("-m", "--mode", help="The mode that the create will run in.  <basic, manual>", default="basic")
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

    if args["mode"]:
        mode = args["mode"]
    else:
        mode = "basic"

    # Initialize the Create robot
    try:
        robot = Create(port)
        robot.connect(test)

        atexit.register(close_connection, robot)

        if mode == "basic":
            driver = BasicDrive(robot)
        elif mode == "manual":
            driver = ManualSteering(robot)
        else:
            print "Valid modes are basic and manual"
            return -1

        driver.run()
    except RuntimeError as err:
        print "A RuntimeError occurred while communicating with the Connect 2: {0}".format(err)
        return -1

    return 0

if __name__ == "__main__":
    sys.exit(main())
