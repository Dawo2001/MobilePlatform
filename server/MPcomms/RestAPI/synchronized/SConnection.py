import threading
from enum import Enum

import requests

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# ConnectionStatus - status enumerator:
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
class ConnectionStatus(Enum):
    UNKNOWN           = 0b001
    DISCONNECTED      = 0b000
    PENDING           = 0b011
    CONNECTED_STANDBY = 0b010
    CONNECTED_ACTIVE  = 0b110
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# ConnectionStatusSwitch - status enumerator switch:
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
connectionStatusSwitch = {
    0b000: ConnectionStatus.DISCONNECTED,
    0b011: ConnectionStatus.PENDING,
    0b010: ConnectionStatus.CONNECTED_STANDBY,
    0b110: ConnectionStatus.CONNECTED_ACTIVE
}
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# MsgData container class:
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

class MsgData(object):
    def __init__(self, isActive:bool = False, vid:int = None, url:str = None) -> None:
        self.isActive = isActive
        self.vid = vid
        self.url = url

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# SConnection - synchronized connection class:
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
class SConnection(object):
    _MAX_EC = 10
    _MAX_PND = 2

    def __init__(self) -> None:
        self._mutex = threading.Lock()
        self._address = "-1"
        self._port = -1
        self._vehicleID = -1
        self._status = ConnectionStatus.UNKNOWN
        self._errorCounter = 0
        self._pendingCounter = 0

    def identify(self, address:str, port:int, vid:int) -> bool:
        self._mutex.acquire()
        # ---
        retval = (address == self._address and\
                port == self._port and\
                vid == self._vehicleID)
        # ---
        self._mutex.release()
        return retval

    def connect(self, address:str, port:int, vid:int) -> None:
        self._mutex.acquire()
        # ---
        self._address = address
        self._port = port
        self._vehicleID = vid
        self._status = ConnectionStatus.CONNECTED_ACTIVE
        print("[i] Connected to http://" + self._address + ":" + str(self._port) + " .")
        # ---
        self._mutex.release()

    def disconnect(self) -> None:
        self._mutex.acquire()
        # ---
        self._status = ConnectionStatus.DISCONNECTED
        print("[i] http://" + self._address + ":" + str(self._port) + " disconnected.")
        # ---
        self._mutex.release()

    def enable(self) -> None:
        self._mutex.acquire()
        # ---
        self._status = ConnectionStatus.CONNECTED_ACTIVE
        # ---
        self._mutex.release()

    def disable(self) -> None:
        self._mutex.acquire()
        # ---
        self._status = ConnectionStatus.CONNECTED_STANDBY
        # ---
        self._mutex.release()

    def getStatus(self) -> ConnectionStatus:
        self._mutex.acquire()
        # ---
        retval = self._status
        # ---
        self._mutex.release()
        return retval

    def getID(self) -> int:
        self._mutex.acquire()
        # ---
        retval = self._vehicleID
        # ---
        self._mutex.release()
        return retval

    def getMsgData(self) -> MsgData:
        self._mutex.acquire()
        # ---
        if self._status == ConnectionStatus.CONNECTED_ACTIVE:
            retval = MsgData(
                isActive = True,
                vid = self._vehicleID,
                url = "http://" + self._address + ":" + str(self._port)
            )
        else:
            retval = MsgData(
                isActive = False
            )
        # ---
        self._mutex.release()
        return retval

    def isOnline(self) -> bool:
        self._mutex.acquire()
        # ---
        retval = self._status.value & ConnectionStatus.CONNECTED_STANDBY.value\
             == ConnectionStatus.CONNECTED_STANDBY.value
        # ---
        self._mutex.release()
        return retval

    def isOffline(self) -> bool:
        self._mutex.acquire()
        # ---
        retval = self._status.value & ConnectionStatus.CONNECTED_STANDBY.value\
             == 0
        # ---
        self._mutex.release()
        return retval

    def isActive(self) -> bool:
        self._mutex.acquire()
        # ---
        status = self._status
        # ---
        self._mutex.release()
        if status == ConnectionStatus.PENDING:
            self.tryConnection()
        return status == ConnectionStatus.CONNECTED_ACTIVE

    def registerError(self) -> None:
        self._mutex.acquire()
        # ---
        self._errorCounter += 1
        if self._errorCounter > SConnection._MAX_EC:
            self._status = ConnectionStatus.PENDING
            print("[w] Lost connection!")
        # ---
        self._mutex.release()

    def registerSuccess(self) -> None:
        online = self.isOnline()
        self._mutex.acquire()
        # ---
        self._errorCounter = 0
        if online:
            self._status = ConnectionStatus.CONNECTED_ACTIVE
        # ---
        self._mutex.release()

    def tryConnection(self) -> bool:
        if self.isOnline():
            self._mutex.acquire()
            # ---
            self._pendingCounter += 1
            if self._pendingCounter > SConnection._MAX_PND:
                print("[i] Trying to reconnect...")
                self._pendingCounter = 0
                url = self._address + str(self._port) + "/vehicle/" + str(self._vehicleID)
                try:
                    response = requests.get(url)
                    ok = response.ok
                except requests.exceptions.RequestException as e: # error occured
                    ok = False
            
                # ---
                self._mutex.release()

                if ok:
                    self.registerSuccess()
                    print("[i] Reconnected!")
                    return True
            else:
                # ---
                self._mutex.release()
        return False

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---