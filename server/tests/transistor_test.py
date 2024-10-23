import RPi.GPIO as GPIO
import time


def main():
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(19, GPIO.OUT)
    GPIO.setup(8, GPIO.IN)

    while True:
        GPIO.output(19, GPIO.LOW)
        time.sleep(1)
        print("low:", GPIO.input(8))
        time.sleep(1)
        GPIO.output(19, GPIO.HIGH)
        time.sleep(1)
        print("high:", GPIO.input(8))
        time.sleep(1)

if __name__ == "__main__":
    main()
