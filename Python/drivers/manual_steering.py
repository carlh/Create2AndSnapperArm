from time import sleep

def run(create):
    print "Beginning Manual steering routine"

    # TODO - Actually steer manually

    create.drive_straight_forward(100)

    sleep(3)
    create.stop_motion()
    print "End Manual steering routine"
