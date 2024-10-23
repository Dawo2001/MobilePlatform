import RPi.GPIO as GPIO
import readchar
import time

# pins:
PAN_STEP = 13
PAN_DIR = 15
PAN_M0 = 7
PAN_SWITCH = 11

TILT_STEP = 16
TILT_DIR = 12
TILT_SWITCH = 18

LASER = 19


def setup_pins():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(PAN_STEP, GPIO.OUT)
    GPIO.setup(PAN_DIR, GPIO.OUT)
    GPIO.setup(PAN_M0, GPIO.OUT)
    GPIO.setup(PAN_SWITCH, GPIO.IN)
    GPIO.setup(TILT_STEP, GPIO.OUT)
    GPIO.setup(TILT_DIR, GPIO.OUT)
    GPIO.setup(TILT_SWITCH, GPIO.IN)
    GPIO.setup(LASER, GPIO.OUT)

    GPIO.output(PAN_M0, GPIO.HIGH)
    GPIO.output(LASER, GPIO.LOW)


def left():
    GPIO.output(PAN_DIR, GPIO.HIGH)
    GPIO.output(PAN_STEP, GPIO.HIGH)
    time.sleep(0.001)
    GPIO.output(PAN_STEP, GPIO.LOW)
    time.sleep(0.001)


def right():
    GPIO.output(PAN_DIR, GPIO.LOW)
    GPIO.output(PAN_STEP, GPIO.HIGH)
    time.sleep(0.001)
    GPIO.output(PAN_STEP, GPIO.LOW)
    time.sleep(0.001)


def up():
    GPIO.output(TILT_DIR, GPIO.LOW)
    GPIO.output(TILT_STEP, GPIO.HIGH)
    time.sleep(0.001)
    GPIO.output(TILT_STEP, GPIO.LOW)
    time.sleep(0.001)


def down():
    GPIO.output(TILT_DIR, GPIO.HIGH)
    GPIO.output(TILT_STEP, GPIO.HIGH)
    time.sleep(0.001)
    GPIO.output(TILT_STEP, GPIO.LOW)
    time.sleep(0.001)


def laser_on():
    GPIO.output(LASER, GPIO.HIGH)


def laser_off():
    GPIO.output(LASER, GPIO.LOW)


def pan_limit_reached() -> bool:
    return GPIO.input(PAN_SWITCH)


def tilt_limit_reached() -> bool:
    return GPIO.input(TILT_SWITCH)


def basing():
    i = 0
    while not tilt_limit_reached() and i < 3000:
        i += 1
        time.sleep(0.001)
        down()

    for _ in range(1400):
        time.sleep(0.001)
        up()

    i = 0
    while not pan_limit_reached() and i < 1300:
        i += 1
        time.sleep(0.001)
        left()

    for _ in range(590):
        time.sleep(0.001)
        right()
    print("Basing finished")


def main():
    def steer(c: str):
        laser_off()
        if c == 'a':
            for _ in range(50):
                time.sleep(0.001)
                left()
            print("LEFT")
        elif c == 'd':
            for _ in range(50):
                time.sleep(0.001)
                right()
            print("RIGHT")
        elif c == 'w':
            for _ in range(50):
                time.sleep(0.001)
                up()
            print("UP")
        elif c == 's':
            for _ in range(50):
                time.sleep(0.001)
                down()
            print("DOWN")
        elif c == ' ' or c == 'e':
            laser_on()
            print("LASER ON")
        elif c == 'r':
            laser_off()
            print("LASER OFF")    
        elif c == 'q':
            print("Finished")
            exit()
    try:
        while True:
            c = readchar.readchar()
            steer(c)
    except KeyboardInterrupt:
        print("exit")


if __name__ == "__main__":
    setup_pins()
    #basing()
    main()
