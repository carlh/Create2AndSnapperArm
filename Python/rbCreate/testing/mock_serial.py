import serial


class MockSerial(serial.Serial):
    def __init__(self, port, parity, stopbits, bytesize, baudrate):
        print("Initialized MockSerial")

    is_open = True

    def close(self):
        print("Closed connection")

    def write(self, data):
        # print("Writing data: ")
        # print data
        return None

    def read(self, size=1):
        print "Reading data"

