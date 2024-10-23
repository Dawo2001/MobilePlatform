import serial
import time
import numpy as np

ser = serial.Serial(
    port="/dev/ttyAMA0",
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1)


def read():
    while True:
        counter = ser.in_waiting  # count the number of bytes of the serial port
        if counter > 0:
            bytes_serial = ser.read()
            print(bytes_serial)


if ser.isOpen() == False:
    ser.open()  # open serial port if not open
    print("serial opened")
    try:
        read()
    except Exception as e:
        print(e)
        ser.close()
else:
    print("Closed")
    ser.close()
    ser.open()
    print("serial opened")
    print(ser.write(b'\x5a\x05\x07\x01\x67'))
    try:
        read()
    except Exception as e:
        print(e)
        ser.close()