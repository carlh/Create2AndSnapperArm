from time import sleep
import curses
import atexit

from rbCreate import DriveDirection
from rbCreate import Create
from rbCreate import TurnDirection
from rbCreate import SpecialRadii

class ManualSteering:

    _MAX_SPEED = 500
    _MAX_RADUIS = 2000

    _turn_radius = SpecialRadii.straight()
    _turn_radius_delta = 5

    _current_direction_key = -1
    _current_turn_key = -1

    def __init__(self, create):
        self.create = create

        self._left_speed = 0  # The current speed of the left wheel [-500, 500]
        self._right_speed = 0  # The current speed of the right wheel [-500, 500]
        self._speed_delta = 100  # The amount to change the speed each time a keypress is detected

        self._turn_speed = 20  # Gradual turn speed

        self.stdscr = curses.initscr()
        self.stdscr.nodelay(1)
        self.stdscr.keypad(1)

        curses.cbreak()
        curses.noecho()

        atexit.register(self.cleanup, self.stdscr)

    def run(self):
        print "Beginning Manual steering routine"

        self.create.set_safe_mode()
        self.stdscr.addstr(0, 0, "Enter W, A, S, D: ")

        # TODO - Actually steer manually
        while True:
            c = self.stdscr.getch()

            if c == curses.ERR:  # No key is pressed
                continue

            self.stdscr.addch(0, 18, c)
            self.stdscr.refresh()
            display_string = ""
            if c == ord('q'):
                self.stdscr.addstr(0, 18, "Quitting...")
                self.stdscr.clrtoeol()
                self.stdscr.refresh()

                break
            elif c == ord('x'):
                self.stdscr.addstr(0, 18, "Stopping...")
                self.stdscr.clrtoeol()
                self.stdscr.refresh()
                self.create.drive_straight_forward(0)
                self._left_speed = 0
                self._right_speed = 0
                # while self._speed > 0.0:
                #     self._speed -= self._speed_delta
                #     self.create.drive_straight_forward(self._speed)
                #     stop_string = "Slowing...{0}".format(self._speed)
                #     self.stdscr.addstr(0, 18, stop_string)
                #     self.stdscr.clrtoeol()
                #     self.stdscr.refresh()
                self.create.stop_motion()
                self.stdscr.addstr(0, 18, "Stopped...")
                self.stdscr.clrtoeol()
                self.stdscr.refresh()
            elif c == ord('w'):
                if self._left_speed < self._MAX_SPEED:
                    self._left_speed += self._speed_delta
                if self._right_speed < self._MAX_SPEED:
                    self._right_speed += self._speed_delta

                if self._left_speed == 0 and self._right_speed == 0:
                    self.create.stop_motion()
                else:
                    self.create.drive_direct(right_speed=self._right_speed, left_speed=self._left_speed)

                display_string = "Left wheel moving at {0} mm/s.  Right wheel moving at {1} mm/s".format(self._left_speed, self._right_speed)
                self.stdscr.addstr(0, 18, display_string)
                self.stdscr.clrtoeol()
                self.stdscr.refresh()
            elif c == ord('a'):
                if self._right_speed < self._MAX_SPEED:
                    self._right_speed += int(self._turn_speed / 2)
                    self._left_speed -= int(self._turn_speed / 2)
                    self.create.drive_direct(right_speed=self._right_speed, left_speed=self._left_speed)

                display_string = "Left wheel moving at {0} mm/s.  Right wheel moving at {1} mm/s".format(self._left_speed, self._right_speed)
                self.stdscr.addstr(0, 18, display_string)
                self.stdscr.clrtoeol()
                self.stdscr.refresh()
            elif c == ord('s'):
                if self._left_speed > -self._MAX_SPEED:
                    self._left_speed -= self._speed_delta
                if self._right_speed > -self._MAX_SPEED:
                    self._right_speed -= self._speed_delta

                if self._right_speed == 0 and self._left_speed == 0:
                    self.create.stop_motion()
                else:
                    self.create.drive_direct(right_speed=self._right_speed, left_speed=self._left_speed)

                display_string = "Left wheel moving at {0} mm/s.  Right wheel moving at {1} mm/s".format(self._left_speed, self._right_speed)
                self.stdscr.addstr(0, 18, display_string)
                self.stdscr.clrtoeol()
                self.stdscr.refresh()
            elif c == ord('d'):
                if self._left_speed < self._MAX_SPEED:
                    self._right_speed -= int(self._turn_speed / 2)
                    self._left_speed += int(self._turn_speed / 2)
                    self.create.drive_direct(right_speed=self._right_speed, left_speed=self._left_speed)

                display_string = "Left wheel moving at {0} mm/s.  Right wheel moving at {1} mm/s".format(self._left_speed, self._right_speed)
                self.stdscr.addstr(0, 18, display_string)
                self.stdscr.clrtoeol()
                self.stdscr.refresh()

        sleep(3)
        print "End Manual steering routine"


    def cleanup(self, stdscr):
        curses.nocbreak()
        curses.echo()
        stdscr.keypad(0)
        curses.endwin()