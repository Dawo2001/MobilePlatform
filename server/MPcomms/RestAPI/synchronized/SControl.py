import threading

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# Control - control container:
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---


class Control:
    control_table = {
        #     0  1  2  3  4  5  6  7  8  9
        0.0: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        0.1: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        0.2: [1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        0.3: [1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
        0.4: [1, 0, 1, 0, 0, 1, 0, 1, 0, 0],
        0.5: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        0.6: [1, 1, 0, 1, 0, 1, 1, 0, 1, 0],
        0.7: [1, 1, 1, 0, 1, 1, 0, 1, 1, 0],
        0.8: [1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
        0.9: [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        1.0: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    }
    max_pan = 170
    min_pan = -170

    max_tilt = 8
    min_tilt = -8

    def __init__(self) -> None:
        self.current_pan: float = 0
        self.current_tilt: float = 0
        self.set_pan: float = 0
        self.set_tilt: float = 0
        self.laser: bool = False

    def __str__(self) -> str:
        return f'Current: pan {self.current_pan}°, tilt {self.current_tilt}°, laser {"yes" if self.laser else "no"}\n \
                 Goal   : pan {self.set_pan}°, tilt {self.set_tilt}°'

    def add(self, pan: float, tilt: float, laser: bool):
        self.set_pan += pan
        self.set_pan = min(max(Control.min_pan, self.set_pan), Control.max_pan)
        self.set_tilt += tilt
        self.set_tilt = min(
            max(Control.min_tilt, self.set_tilt), Control.max_tilt)
        self.laser = (self.laser != laser)

    def update(self, pan: float, tilt: float):
        self.current_pan += pan
        self.current_tilt += tilt


# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# SControl - synchronized control class:
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---


class SControl(object):
    def __init__(self) -> None:
        self._changed = False
        self._control = Control()
        self._mutex = threading.Lock()

    def isChanged(self) -> bool:
        self._mutex.acquire()
        retval = self._changed
        self._mutex.release()
        return retval

    def pollControl(self) -> Control:  # clears _changed flag
        self._mutex.acquire()
        retval = self._control
        self._changed = False
        self._mutex.release()
        return retval

    def lookupControl(self) -> Control:  # leaves _changed flag unchanged
        self._mutex.acquire()
        retval = self._control
        self._mutex.release()
        return retval

    def postControl(self, pan: float, tilt: float, laser: bool) -> None:  # sets _changed flag
        self._mutex.acquire()
        self._control.add(pan, tilt, laser)
        self._changed = True
        self._mutex.release()

    def updateControl(self, pan: float, tilt: float) -> None:
        self._mutex.acquire()
        self._control.update(pan, tilt)
        self._mutex.release()
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
