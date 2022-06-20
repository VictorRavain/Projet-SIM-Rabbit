# coding: utf-8

import serial
import serial.tools.list_ports
import time


class Arduino:

    def __init__(self, channels, port, baudrate, coeur, poumon):
        self.ser = serial.Serial(port=port, baudrate=baudrate)
        ch = next(filter(lambda c: c['name'] == coeur, channels), None)
        self.fc = ch['id']
        ch = next(filter(lambda c: c['name'] == poumon, channels), None)
        self.fr = ch['id']
        time.sleep(1)

    def arduino_communication(self, csts):
        msg = str(csts[self.fc]) + 'c' + str(csts[self.fr]) + 'r' #+ str(75) +'f'
        # print(msg)
        self.ser.write(msg.encode())

    def close(self):
        self.ser.close()


if __name__ == "__main__":
    robot = Arduino('COM7', 20000)
    while True:
        robot.arduino_communication({'FC': 180.4, 'FR': 67.2})
