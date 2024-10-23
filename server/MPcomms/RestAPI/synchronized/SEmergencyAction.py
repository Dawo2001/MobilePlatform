import threading
from enum import Enum

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# EmergencyActions - emergency action enumerator:
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
class EmergencyActions(Enum):
    INVALID = -1
    NOTASK = 0b00
    STOP = 0b01
    RETURN = 0b10
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# EmergencyActionSwitch - emergency action enumerator switch:
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
emergencyActionsSwitch = {
    0b00: EmergencyActions.NOTASK,
    0b01: EmergencyActions.STOP,
    0b10: EmergencyActions.RETURN
}
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# SEmergencyAction - synchronized emergency action class:
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
class SEmergencyAction(object):
    def __init__(self) -> None:
        self._changed = False
        self._action = EmergencyActions.NOTASK
        self._mutex = threading.Lock()
    
    def isChanged(self) -> bool:
        self._mutex.acquire()
        retval = self._changed
        self._mutex.release()
        return retval

    def pollAction(self) -> EmergencyActions: # clears _changed flag
        self._mutex.acquire()
        retval = self._action
        self._changed = False
        self._mutex.release()
        return retval

    def lookupAction(self) -> EmergencyActions: # leaves _changed flag unchanged
        self._mutex.acquire()
        retval = self._action
        self._mutex.release()
        return retval

    def postAction(self, action: EmergencyActions) -> None: # sets _changed flag
        self._mutex.acquire()
        self._action = action
        self._changed = True
        self._mutex.release()

    def setAction(self, action: EmergencyActions) -> None: # leaves _changed flag unchanged
        self._mutex.acquire()
        self._action = action
        self._mutex.release()
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---