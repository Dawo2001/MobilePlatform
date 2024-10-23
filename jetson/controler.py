import struct
from tkinter import Image
import cv2
import numpy as np
import socket
from regulator import PID
import measuring_disc_detection
from PIL import Image
from InterruptibleLoop import InterruptibleLoop
import csv
import time
import struct
from inputs import get_gamepad
import math, socket, threading
from time import sleep
from InterruptibleLoop import InterruptibleLoop


CAMERA_IP = '192.168.68.102'
CAMERA_C_PORT = 5734

PLATFORM_IP = '192.168.68.109'
PLATFORM_C_PORT = 5733
STEER_BASE=5.



def deadzone(inPut:float, deadzone) -> float:
    if inPut > 0:
        return max(0, (inPut - deadzone) / (1. - deadzone))
    else:
        return min(0, (inPut + deadzone) / (1. - deadzone))

def scaleTrigg(inPut:float, low:float, high:float) -> float:
    if inPut > 0:
        return inPut * (high - low) + low
    elif inPut < 0:
        return inPut * 20 + 40
    else:
        return 50
    
def scaleSteer(inPut:float, base=STEER_BASE) -> float:
    if inPut > 0:
        return (base ** inPut - 1) / (base - 1)
    elif inPut < 0:
        return -(base ** (-inPut) - 1) / (base - 1)
    else:
        return 0



class XboxController:
    # XboxController class by Brian Zier and Kevin Hughes. (2017 MIT-license)
    # https://github.com/bzier/TensorKart/blob/master/utils.py
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):

        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        '''
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0
        '''
        self.HorizontalDPad = 0
        self.VerticalDPad = 0

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()


    def read_camera(self):
        horizontal_dpad = self.HorizontalDPad
        vertical_dpad = self.VerticalDPad
        x_button = self.X
        b_button = self.B
        y_button = self.Y
        a_button = self.A
        left_bumper = self.LeftBumper
        right_bumper = self.RightBumper
        return [horizontal_dpad, vertical_dpad, x_button, b_button, y_button, a_button, left_bumper, right_bumper]
    

    def read_platform(self):
        xL = scaleSteer(-deadzone(self.LeftJoystickX, 0.2))
        yL = deadzone(self.LeftJoystickY, 0.2)
        xR = deadzone(self.RightJoystickX, 0.2)
        yR = deadzone(self.RightJoystickY, 0.2)
        trig = deadzone(self.RightTrigger, 0.07) - deadzone(self.LeftTrigger, 0.07)

        maxTrig = 65
        if self.A == 1:
            maxTrig = 60
        elif self.B == 1:
            maxTrig = 61
        elif self.Y == 1:
            maxTrig = 63

        # translate to mobile base control signals:
        throttle = round(scaleTrigg(trig, 58, maxTrig), 1)
        steering = round(xL*50 + 50, 1)

        updown = round(yL * 50, 1)
        xAxis = round(xR * 50, 1)
        yAxis = round(yR * 50, 1)

        uFL = min(100, max(0, 50 + updown + xAxis - yAxis))
        uFR = min(100, max(0, 50 + updown - xAxis - yAxis))
        uBL = min(100, max(0, 50 + updown + xAxis + yAxis))
        uBR = min(100, max(0, 50 + updown - xAxis + yAxis))

        return [throttle, steering, uFL, uFR, uBL, uBR]


    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self.LeftJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_X':
                    self.LeftJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RY':
                    self.RightJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RX':
                    self.RightJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_Z':
                    self.LeftTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'ABS_RZ':
                    self.RightTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'BTN_TL':
                    self.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    self.RightBumper = event.state
                elif event.code == 'BTN_SOUTH':
                    self.A = event.state
                elif event.code == 'BTN_NORTH':
                    self.Y = event.state #previously switched with X
                elif event.code == 'BTN_WEST':
                    self.X = event.state #previously switched with Y
                elif event.code == 'BTN_EAST':
                    self.B = event.state
                elif event.code == 'BTN_THUMBL':
                    self.LeftThumb = event.statez
                elif event.code == 'BTN_THUMBR':
                    self.RightThumb = event.state
                elif event.code == 'BTN_SELECT':
                    self.Back = event.state
                elif event.code == 'BTN_START':
                    self.Start = event.state

                elif event.code == 'ABS_HAT0X':
                    self.HorizontalDPad = event.state
                elif event.code == 'ABS_HAT0Y':
                    self.VerticalDPad = event.state
                    

                    
                '''#elif event.code == 'BTN_TRIGGER_HAPPY1':
                #    self.LeftDPad = event.state
                elif event.code == 'ABS_HAT0X':
                    self.RightDPad = event.state
                    print(self.RightDPad)
                #elif event.code == 'ABS_HAT0Y':
                #    self.UpDPad = event.state
                elif event.code == 'ABS_HAT0Y':
                    self.DownDPad = event.state
                    print(self.DownDPad)
                #elif event.code == 'ABS_HAT0Y':
                #    self.UpDPad = event.state
                '''



def run():
    joy = XboxController()
    loop = InterruptibleLoop()
    sc = None
    sp = None
    try:
        sc:socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc.settimeout(0.5)
        sc.connect((CAMERA_IP, CAMERA_C_PORT))
        sp:socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sp.settimeout(0.5)
        sp.connect((PLATFORM_IP, PLATFORM_C_PORT))
    except socket.error:
        print('Lost connection or could not connect.')
    while loop.loop_again:
            time.sleep(0.1)
            data_camera = joy.read_camera()
            data_platform = joy.read_platform()
            byte_data_camera = struct.pack('!%sf' % len(data_camera), *data_camera)
            byte_data_platform = struct.pack('!%sf' % len(data_platform), *data_platform)
            sc.send(byte_data_camera)
            sp.send(byte_data_platform)
    sc.close()
    sp.close()





if __name__=='__main__':
    run()
    