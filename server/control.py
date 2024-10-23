from pynput.keyboard import Key, Listener
import requests
import sys
import random


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
    print(f"Sending commands to vehicle {vid} on {address}")

    def send_control(pan: int, tilt: int, laser: bool):
        url = f'http://{address}:5000/api/control'

        try:
            content = {
                'vid': vid,
                'pan': pan,
                'tilt': tilt,
                'laser': laser,
                'mgc': 43795
            }
            result = requests.post(url, json=content).json()
            print(result)
            print(f"Control send: pan {pan}°, tilt {tilt}°, laser {laser}")
            print(f"Goal set: pan {result['pan']}°, \
tilt {result['tilt']}°, laser {result['laser']}")
        except Exception as e:
            print("Cannot send request:", e)

    def on_press(key):
        if key == Key.right:
            send_control(10, 0, False)
        if key == Key.left:
            send_control(-10, 0, False)
        if key == Key.up:
            send_control(0, 1, False)
        if key == Key.down:
            send_control(0, -1, False)
        if key == Key.space:
            send_control(0, 0, True)

    def on_release(key):
        if key == Key.esc:
            return False

    try:
        with Listener(
                on_press=on_press,
                on_release=on_release) as listener:
            listener.join()
    except:
        print("Finished")


if __name__ == "__main__":
    address = "192.168.68.105"
    args = sys.argv
    if len(args) == 1:
        vid = connect(address)
    else:
        vid = int(args[1])
    main(address, vid)

    if len(args) == 1:
        disconnect(address, vid)
