import RPi.GPIO as GPIO
import time
import sys


def main(PIN):
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(PIN, GPIO.OUT)

    while True:
        print(f"pin {PIN} is low")
        GPIO.output(PIN, GPIO.LOW)
        time.sleep(2)
        print(f"pin  {PIN} is high")
        GPIO.output(PIN, GPIO.HIGH)
        time.sleep(2)

if __name__ == "__main__":
    arg = int(sys.argv[1])
    main(arg)
