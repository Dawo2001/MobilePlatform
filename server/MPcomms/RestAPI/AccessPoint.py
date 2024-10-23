import requests
import json
from flask import Flask, Blueprint
from flask_restx import Api
from waitress import serve
from RestAPI.synchronized.SMode import *
from RestAPI.synchronized.SControl import *
from RestAPI.synchronized.SEmergencyAction import *
from RestAPI.synchronized.SConnection import *
from RestAPI.messaging.Messages import *

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# AccessPoint class:
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---


class AccessPoint(object):
    app = Flask(__name__)
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api = Api(blueprint, doc='/doc/')
# ---

    def __init__(self):
        self._mode = SMode()
        self._control = SControl()
        self._emergencyAction = SEmergencyAction()
        self._connection = SConnection()
        self._th = None
# ---

    def run(self) -> None:
        serve(AccessPoint.app, host='0.0.0.0', port=5000)
# ---

    def run_async(self) -> None:
        self._th = threading.Thread(target=self.run)
        self._th.daemon = True
        self._th.start()
# ---

    def stop_async(self) -> None:
        self._th.join()
# ---
# --- Connection specyfic: ---

    def getVehicleID(self) -> int:
        return self._connection.getID()
# ---

    def getConnectionStatus(self) -> ConnectionStatus:
        return self._connection.getStatus()
# ---

    def isOnline(self) -> bool:
        return self._connection.isOnline()
# ---

    def isActive(self) -> bool:
        return self._connection.isActive()
# ---

    def isOffline(self) -> bool:
        return self._connection.isOffline()
# ---

    def connect(self, address: str, port: int, vid: int) -> None:
        self._connection.connect(address, port, vid)
# ---

    def disconnect(self) -> None:
        self._connection.disconnect()
# ---

    def identifyConnection(self, address: str, port: int, vid: int) -> bool:
        return self._connection.identify(address, port, vid)
# ---

    def activate(self, toggle: bool) -> None:
        if toggle:
            self._connection.enable()
        else:
            self._connection.disable()
# ---
# --- Messaging specyfic ---

    def send(self, msg: Message) -> bool:
        data = self._connection.getMsgData()
        if(data.isActive):
            endpt = data.url + msg._url_dir
            try:
                response = requests.post(endpt, json=msg.getMsg(data.vid))
                ok = response.ok
            except requests.exceptions.RequestException as e:  # error occured
                self._connection.registerError()
                ok = False
#            print("Message sent to " + endpt)
#            print("\tReceived code " + str(response.status_code))
#            print("\tmsg body: " + json.dumps(msg.getMsg(data.vid)))
#            print("delay: " + str(response.elapsed))
            if ok:
                self._connection.registerSuccess()
                return True
            return False
        else:
            return False
# ---
# --- Mode specyfic: ---

    def modeChanged(self) -> bool:
        return self._mode.isChanged()
# ---

    def getMode(self) -> SMode:
        return self._mode
# ---

    def pollMode(self) -> Modes:
        return self._mode.pollMode()
# ---

    def lookupMode(self) -> Modes:
        return self._mode.lookupMode()
# ---

    def postMode(self, code) -> None:
        newMode = modeSwitch.get(code, Modes.INVALID)
        if(newMode != Modes.INVALID):
            self._mode.postMode(newMode)
# ---

    def setMode(self, mode: Modes) -> None:
        if(mode != Modes.INVALID):
            self._mode.setMode(mode)
# ---
# --- EmergencyAction specyfic: ---

    def emergencyActionChanged(self) -> bool:
        return self._emergencyAction.isChanged()
# ---

    def getEmergencyAction(self) -> SEmergencyAction:
        return self._emergencyAction
# ---

    def pollEmergencyAction(self) -> EmergencyActions:
        return self._emergencyAction.pollAction()
# ---

    def lookupEmergencyAction(self) -> EmergencyActions:
        return self._emergencyAction.lookupAction()
# ---

    def postEmergencyAction(self, code) -> None:
        newEA = emergencyActionsSwitch.get(code, EmergencyActions.INVALID)
        if(newEA != EmergencyActions.INVALID):
            self._emergencyAction.postAction(newEA)
# ---

    def setEmergencyAction(self, action: EmergencyActions) -> None:
        if(action != EmergencyActions.INVALID):
            self._emergencyAction.setAction(action)
# ---
# --- Control specyfic: ---

    def controlChanged(self) -> bool:
        return self._control.isChanged()
# ---

    def getControl(self) -> SControl:
        return self._control
# ---

    def pollControl(self) -> Control:
        return self._control.pollControl()
# ---

    def lookupControl(self) -> Control:
        return self._control.lookupControl()
# ---

    def postControl(self, pan: float, tilt: float, laser: bool) -> None:
        self._control.postControl(pan, tilt, laser)
# ---

    def updateControl(self, pan: float, tilt: float):
        self._control.updateControl(pan, tilt)
# --- AccessPoint ends here: ---


AccessPoint.app.register_blueprint(AccessPoint.blueprint)
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
