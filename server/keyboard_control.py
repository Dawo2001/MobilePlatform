from pynput.keyboard import Key, Listener
import requests
import threading
import sys
import time
import random


class Keyboard(object):
    def __init__(self) -> None:
        self._controls = {
            'pan': 0,
            'tilt': 0,
            'laser': 0
        }
        self._speed = 1
        self._changed = False
        self._mutex = threading.Lock()

    def setControl(self, control_name: str, control) -> None:
        self._mutex.acquire()
        if self._controls[control_name] != control:
            print(f"Set control {control_name} to {control}")
            self._controls[control_name] = control
            self._changed = True
        self._mutex.release()

    def setSpeed(self, speed: float) -> None:
        self._mutex.acquire()
        self._speed = speed
        print(f"Set speed to {speed}")
        self._mutex.release()

    def isChanged(self) -> bool:
        self._mutex.acquire()
        retval = self._changed
        self._mutex.release()
        return retval

    def pollControl(self) -> dict:
        self._mutex.acquire()
        retval = self._controls
        self._changed = False
        self._mutex.release()
        return retval

    def getSpeed(self) -> dict:
        self._mutex.acquire()
        retval = self._speed
        self._mutex.release()
        return retval


def connect(address: str) -> int:
    url = f'http://{address}:5000/api/connect'
    try:
        content = {
            'addr': 'localhost',
            'port': '8000',
            'vid': random.randint(0, 100),
            'mgc': 60949
        }
        result = requests.post(url, json=content)
        vid = int(result.json()['vid'])
        print(f"Connected to vehicle number: {vid}")
        return vid
    except Exception as e:
        print("Cannot establish connection", result)
        raise e


def disconnect(address: str, vid: int) -> int:
    url = f'http://{address}:5000/api/connect'
    try:
        content = {
            'addr': 'localhost',
            'port': '8000',
            'vid': vid,
            'mgc': 15061
        }
        result = requests.delete(url, json=content)
        vid = int(result.json()['vid'])
        print(f"Disconnected from vehicle number: {vid}")
        return vid
    except Exception as e:
        print(result.content)
        print("Cannot delete connection", result)
        raise e


def main(address: str, vid: int):
    keyboard = Keyboard()

    def on_press(key):
        speed = keyboard.getSpeed()
        if key == Key.right:
            keyboard.setControl('pan', speed)
        if key == Key.left:
            keyboard.setControl('pan', -1*speed)
        if key == Key.up:
            keyboard.setControl('tilt', speed)
        if key == Key.down:
            keyboard.setControl('tilt', -1*speed)
        if key == Key.space:
            keyboard.setControl('laser', True)

        key = str(key)
        if key == "'1'":
            keyboard.setSpeed(0.1)
        if key == "'2'":
            keyboard.setSpeed(0.2)
        if key == "'3'":
            keyboard.setSpeed(0.3)
        if key == "'4'":
            keyboard.setSpeed(0.4)
        if key == "'5'":
            keyboard.setSpeed(0.5)
        if key == "'6'":
            keyboard.setSpeed(0.6)
        if key == "'7'":
            keyboard.setSpeed(0.7)
        if key == "'8'":
            keyboard.setSpeed(0.8)
        if key == "'9'":
            keyboard.setSpeed(0.9)
        if key == "'0'":
            keyboard.setSpeed(1)

    def on_release(key):
        previous_control = keyboard.pollControl()
        if key == Key.right:
            keyboard.setControl('pan', min(0, previous_control['pan']))
        if key == Key.left:
            keyboard.setControl('pan', max(0, previous_control['pan']))
        if key == Key.up:
            keyboard.setControl('tilt', min(0, previous_control['tilt']))
        if key == Key.down:
            keyboard.setControl('tilt', max(0, previous_control['tilt']))
        if key == Key.space:
            keyboard.setControl('laser', False)
        if key == Key.esc:
            return False

    try:
        def listen():
            with Listener(
                    on_press=on_press,
                    on_release=on_release) as listener:
                listener.join()

        l = threading.Thread(target=listen)
        l.daemon = True
        l.start()
    except:
        print("Error starting key listener")

    url = f'http://{address}:5000/api/control'

    print(f"Sending commands to vehicle {vid} on {address}")
    try:
        while True:
            time.sleep(0.01)
            if keyboard.isChanged():
                control = keyboard.pollControl()

                content = {
                    'vid': vid,
                    'pan': control['pan'],
                    'tilt': control['tilt'],
                    'laser': control['laser'],
                    'mgc': 43795
                }
                requests.post(url, json=content)
    except KeyboardInterrupt:
        print("Finished")


if __name__ == "__main__":
    address = "192.168.68.101"
    args = sys.argv
    if len(args) == 1:
        vid = connect(address)
    else:
        vid = int(args[1])
    main(address, vid)

    if len(args) == 1:
        disconnect(address, vid)
