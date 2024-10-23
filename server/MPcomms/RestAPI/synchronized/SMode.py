import threading
from enum import Enum

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# Modes - mode enumerator:
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
class Modes(Enum):
    INVALID = -1
    STANDBY = 0b00
    AUTOMATIC = 0b01
    MANUAL = 0b10
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# ModeSwitch - mode enumerator switch:
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
modeSwitch = {
    0b00: Modes.STANDBY,
    0b01: Modes.AUTOMATIC,
    0b10: Modes.MANUAL
}
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# SMode - synchronized mode class:
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
class SMode(object):
    def __init__(self) -> None:
        self._changed = False
        self._mode = Modes.STANDBY
        self._mutex = threading.Lock()
    
    def isChanged(self) -> bool:
        self._mutex.acquire()
        retval = self._changed
        self._mutex.release()
        return retval

    def pollMode(self) -> Modes: # clears _changed flag
        self._mutex.acquire()
        retval = self._mode
        self._changed = False
        self._mutex.release()
        return retval

    def lookupMode(self) -> Modes: # leaves _changed flag unchanged
        self._mutex.acquire()
        retval = self._mode
        self._mutex.release()
        return retval

    def postMode(self, mode: Modes) -> None: # sets _changed flag 
        self._mutex.acquire()
        self._mode = mode
        self._changed = True
        self._mutex.release()

    def setMode(self, mode: Modes) -> None: # leaves _changed flag unchanged
        self._mutex.acquire()
        self._mode = mode
        self._mutex.release()
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---