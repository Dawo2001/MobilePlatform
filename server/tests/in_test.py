import RPi.GPIO as GPIO
import time
import sys


def main(PIN):
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(PIN, GPIO.IN)

    while True:
        print(f"pin {PIN}: {GPIO.input(PIN)}")
        time.sleep(0.01)

if __name__ == "__main__":
    arg = int(sys.argv[1])
    main(arg)
