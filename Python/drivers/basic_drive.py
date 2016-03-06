from time import sleep
from Python.rbCreate.create import DriveDirection
from Python.rbCreate.create import TurnDirection

def run(create):
    print "Begin basic test drive routine"
    create.set_safe_mode()

    create.drive(direction=DriveDirection.Reverse, speed=500, turn_direction=TurnDirection.Left, turn_radius=500)

    sleep(3)

    create.drive(direction=DriveDirection.Forward, speed=300, turn_direction=TurnDirection.Right, turn_radius=500)
    sleep(4)

    create.stop_motion()
    create.stop()

    print "End basic test drive routine"
