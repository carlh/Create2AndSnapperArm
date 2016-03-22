from time import sleep
from SnapperCreate.rbCreate import DriveDirection
from SnapperCreate.rbCreate import TurnDirection
from SnapperCreate.rbCreate import SpecialRadii


class BasicDrive:
    def __init__(self, create):
        print "Starting basic drive"
        self.create = create
        return

    def run(self):
        print "Begin basic test drive routine"
        self.create.set_safe_mode()

        self.create.drive(direction=DriveDirection.Forward, speed=100, turn_direction=TurnDirection.Left, turn_radius=SpecialRadii.straight())

        sleep(1)

        self.create.drive(direction=DriveDirection.Forward, speed=200, turn_direction=TurnDirection.Left, turn_radius=500)
        sleep(2)

        self.create.drive(direction=DriveDirection.Forward, speed=300, turn_direction=TurnDirection.Right, turn_radius=500)
        sleep(1)

        self.create.drive(direction=DriveDirection.Forward, speed=200, turn_direction=TurnDirection.Straight, turn_radius=SpecialRadii.straight())
        sleep(2)

        self.create.drive(direction=DriveDirection.Forward, speed=200, turn_direction=TurnDirection.Left, turn_radius=0)
        sleep(5)
        # self.create.stop_motion()

        print "End basic test drive routine"
        return
