from flask import abort
from flask_restx import Resource, fields
from RestAPI.authorization.magics import Magic
from RestAPI.synchronized.SMode import *
from RestAPI.synchronized.SEmergencyAction import *
from RestAPI.synchronized.SConnection import *
from RestAPI.AccessPoint import *

# AccessPoint variable 'restAP' to communicate with server
restAP = AccessPoint()

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# Models used in communication:
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
connectInModel = AccessPoint.api.model('ConnectRequest', {
    'addr': fields.String(required=True, description='IPv4 address of communication endpoint'),
    'port': fields.Integer(required=True, description='Port used for communication'),
    'vid': fields.Integer(required=True, description='Vehicle ID set for the purpose of identification'),
    'mgc': fields.Integer(required=True, description='Magic number for verification, add: 60949; delete: 15061')
})
# ---
connectOutModel = AccessPoint.api.model('ConnectResponse', {
    'vid': fields.Integer(required=True, description='Vehicle ID'),
})
# ---
activateInModel = AccessPoint.api.model('ConnectToggleRequest', {
    'activ': fields.Boolean(required=True, description='Activation flag'),
    'vid': fields.Integer(required=True, description='Vehicle ID'),
    'mgc': fields.Integer(required=True, default=Magic.CONNECTION_TOGGLE.value, description='Magic number for verification')
})
# ---
activateOutModel = AccessPoint.api.model('ConnectToggleResponse', {
    'vid': fields.Integer(required=True, description='Vehicle ID'),
    'activ': fields.Boolean(required=True, description='Activation flag'),
})
# ---
modeInModel = AccessPoint.api.model('ModeRequest', {
    'mode': fields.Integer(required=True, description='Mode code for vehicle to switch to'),
    'vid': fields.Integer(required=True, description='Vehicle ID'),
    'mgc': fields.Integer(required=True, default=Magic.MODE_CHANGE.value, description='Magic number for verification')
})
# ---
modeOutModel = AccessPoint.api.model('ModeResponse', {
    'vid': fields.Integer(description='Vehicle ID'),
    'mode': fields.Integer(description='Mode code, the vehicle is currently in')
})
# ---
emergencyInModel = AccessPoint.api.model('EmergencyActionRequest', {
    'ea': fields.Integer(required=True, description='Code for emergency action for vehicle to perform'),
    'vid': fields.Integer(required=True, description='Vehicle ID'),
    'mgc': fields.Integer(required=True, default=Magic.EMERGENCY_ACTION_SET.value, description='Magic number for verification')
})
# ---
emergencyOutModel = AccessPoint.api.model('EmergencyActionResponse', {
    'vid': fields.Integer(description='Vehicle ID'),
    'ea': fields.Integer(description='Emergency action that will be performed')
})
# ---
controlInModel = AccessPoint.api.model('ControlTowerRequest', {
    'vid': fields.Integer(required=True, description='Vehicle ID'),
    'pan': fields.Float(required=True, description='Pan angle diff'),
    'tilt': fields.Float(required=True, description='Tilt angle diff'),
    'laser': fields.Boolean(required=True, description='Switch laser state'),
    'mgc': fields.Integer(required=True, default=Magic.TOWER_CONTROL.value, description='Magic number for verification')
})
# ---
controlOutModel = AccessPoint.api.model('ControlTowerResponse', {
    'vid': fields.Integer(required=True, description='Vehicle ID'),
    'pan': fields.Float(required=True, description='Pan angle requested position'),
    'tilt': fields.Float(required=True, description='Tilt angle requested position'),
    'laser': fields.Boolean(required=True, description='Switch laser state'),
})
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# Parsers used in communication:
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
connectInParser = AccessPoint.api.parser()
connectInParser.add_argument(
    'addr', type=str, required=True, help='IPv4 address of communication endpoint'
)
connectInParser.add_argument(
    'port', type=int, required=True, help='Port used for communication'
)
connectInParser.add_argument(
    'vid', type=int, required=True, help='Vehicle ID set for the purpose of identification'
)
connectInParser.add_argument(
    'mgc', type=int, required=True, help='Magic number for verification'
)
# ---
activateInParser = AccessPoint.api.parser()
activateInParser.add_argument(
    'activ', type=bool, required=True, help='Activation flag'
)
activateInParser.add_argument(
    'vid', type=int, required=True, help='Vehicle ID'
)
activateInParser.add_argument(
    'mgc', type=int, required=True, help='Magic number for verification'
)
# ---
modeInParser = AccessPoint.api.parser()
modeInParser.add_argument(
    'mode', type=int, required=True, help='Mode code for vehicle to switch to'
)
modeInParser.add_argument(
    'vid', type=int, required=True, help='Vehicle ID'
)
modeInParser.add_argument(
    'mgc', type=int, required=True, help='Magic number for verification'
)
# ---
emergencyInParser = AccessPoint.api.parser()
emergencyInParser.add_argument(
    'ea', type=int, required=True, help='Code for emergency action for vehicle to perform'
)
emergencyInParser.add_argument(
    'vid', type=int, required=True, help='Vehicle ID'
)
emergencyInParser.add_argument(
    'mgc', type=int, required=True, help='Magic number for verification'
)
# ---
controlInParser = AccessPoint.api.parser()
controlInParser.add_argument(
    'vid', type=int, required=True, help='Vehicle ID'
)
controlInParser.add_argument(
    'pan', type=float, required=True, help='Pan angle diff'
)
controlInParser.add_argument(
    'tilt', type=float, required=True, help='Tilt angle diff'
)
controlInParser.add_argument(
    'laser', type=bool, required=True, help='Switch laser state'
)
controlInParser.add_argument(
    'mgc', type=int, required=True, help='Magic number for verification'
)
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# REST Access Points:
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---


@AccessPoint.api.route('/connect')
class Connection(Resource):
    @AccessPoint.api.expect(connectInModel)
    @AccessPoint.api.marshal_with(connectOutModel)
    def post(self):
        if(restAP.isOffline()):
            args = connectInParser.parse_args()
            if(args['mgc'] == Magic.CONNECTION_ADD.value):
                restAP._connection.connect(args['addr'], args['port'], args['vid'])
                return {'vid': restAP.getVehicleID()}
            else:
                abort(406, "Wrong operation code number")
        else:
            abort(409, "Vehicle is already connected to another base")

    @AccessPoint.api.expect(connectInModel)
    @AccessPoint.api.marshal_with(connectOutModel)
    def delete(self):
        if(restAP.isOnline()):
            args = connectInParser.parse_args()
            if(args['mgc'] == Magic.CONNECTION_DELETE.value):
                if(restAP.identifyConnection(args['addr'], args['port'], args['vid'])):
                    restAP.disconnect()
                    return {'vid': restAP.getVehicleID()}
                else:
                    abort(404, "There is no active connection with specified values")
            else:
                abort(406, "Wrong operation code number")
        else:
            abort(409, "There is no active connection")


@AccessPoint.api.route('/connect/activate')
class ConnectionActivate(Resource):
    @AccessPoint.api.expect(activateInModel)
    @AccessPoint.api.marshal_with(activateOutModel)
    def post(self):
        if(restAP.isOnline()):
            args = activateInParser.parse_args()
            if(args['mgc'] == Magic.CONNECTION_TOGGLE.value):
                if(args['vid'] == restAP.getVehicleID()):
                    restAP.activate(args['activ'])
                    return {'vid': restAP.getVehicleID(),
                            'activ': args['activ']}
                else:
                    abort(404, "There is no active connection with passed ID")
            else:
                abort(406, "Wrong operation code number")
        else:
            abort(409, "There is no active connection")


@AccessPoint.api.route('/mode/<int:vid>')
class GetMode(Resource):
    @AccessPoint.api.marshal_with(modeOutModel)
    def get(self, vid):
        if(restAP.isOnline()):
            if(vid == restAP.getVehicleID()):
                return {
                    'vid': vid,
                    'mode': restAP.lookupMode().value
                }
            else:
                abort(404, "Not an active vehicle")
        else:
            abort(409, "There is no active connection")


@AccessPoint.api.route('/mode')
class SetMode(Resource):
    @AccessPoint.api.expect(modeInModel)
    @AccessPoint.api.marshal_with(modeOutModel)
    def post(self):
        if(restAP.isOnline()):
            args = modeInParser.parse_args()
            if(args['mgc'] == Magic.MODE_CHANGE.value):
                if(args['vid'] == restAP.getVehicleID()):
                    restAP.postMode(args['mode'])
                    return {
                        'vid': restAP.getVehicleID(),
                        'mode': restAP.lookupMode().value
                    }
                else:
                    abort(404, "There is no active connection with passed ID")
            else:
                abort(406, "Wrong operation code number")
        else:
            abort(409, "There is no active connection")


@AccessPoint.api.route('/emergency/<int:vid>')
class GetEmergencyAction(Resource):
    @AccessPoint.api.marshal_with(emergencyOutModel)
    def get(self, vid):
        if(restAP.isOnline()):
            if(vid == restAP.getVehicleID()):
                return {
                    'vid': vid,
                    'ea': restAP.lookupEmergencyAction().value
                }
            else:
                abort(404, "Not an active vehicle")
        else:
            abort(409, "There is no active connection")


@AccessPoint.api.route('/emergency')
class SetEmergencyAction(Resource):
    @AccessPoint.api.expect(emergencyInModel)
    @AccessPoint.api.marshal_with(emergencyOutModel)
    def post(self):
        if(restAP.isOnline()):
            args = emergencyInParser.parse_args()
            if(args['mgc'] == Magic.EMERGENCY_ACTION_SET.value):
                if(args['vid'] == restAP.getVehicleID()):
                    restAP.postEmergencyAction(args['ea'])
                    return {
                        'vid': restAP.getVehicleID(),
                        'ea': restAP.lookupEmergencyAction().value
                    }
                else:
                    abort(404, "There is no active connection with passed ID")
            else:
                abort(406, "Wrong operation code number")
        else:
            abort(409, "There is no active connection")


@AccessPoint.api.route('/control')
class SetTowerControl(Resource):
    @AccessPoint.api.expect(controlInModel)
    @AccessPoint.api.marshal_with(controlOutModel)
    def post(self):
        if(restAP.isOnline()):
            args = controlInParser.parse_args()
            if(args['mgc'] == Magic.TOWER_CONTROL.value):
                if(args['vid'] == restAP.getVehicleID()):
                    restAP.postControl(
                        args['pan'], args['tilt'], args['laser'])
                    return {
                        'vid': restAP.getVehicleID(),
                        'pan': restAP.lookupControl().set_pan,
                        'tilt': restAP.lookupControl().set_tilt,
                        'laser': restAP.lookupControl().laser
                    }
                else:
                    abort(404, "There is no active \
connection with passed ID")
            else:
                abort(406, "Wrong operation code number")
        else:
            abort(409, "There is no active connection")

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---


# test run server:
if __name__ == '__main__':
    print("Starting server on localhost:5000")
    print("Swagger UI accessible at http://localhost:5000/api/doc")
    restAP.run()
