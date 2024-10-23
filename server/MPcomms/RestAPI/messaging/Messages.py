from datetime import datetime

def formatTime(t:datetime) -> str:
    return t.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


class Message(object):
    _url_dir = '/'
    def __init__(self, readingDate:str = formatTime(datetime.now())):
        self.readingDate = readingDate

    def getMsg(self, vid:int) -> dict:
        return {
            'vehicleId': vid,
            'readingDate': self.readingDate
        }


class PointCloudMsg(Message):
    _url_dir = '/point-cloud'
    def __init__(self, readingDate:str = formatTime(datetime.now()),\
        pointCloudReading:str = None):

        super().__init__(readingDate=readingDate)
        self.pointCloudReading = pointCloudReading

    def getMsg(self, vid:int) -> dict:
        msg = super().getMsg(vid)
        if self.pointCloudReading is not None:
            msg['pointCloudReading'] = self.pointCloudReading
        return msg


class LocationMsg(Message):
    _url_dir = '/location'
    def __init__(self, readingDate:str = formatTime(datetime.now()),\
        slamXCoordinate:float = None, slamYCoordinate:float = None,\
        slamRotation:float = None, realXCoordinate:float = None,\
        realYCoordinate:float = None):

        super().__init__(readingDate=readingDate)
        self.slamXCoordinate = slamXCoordinate
        self.slamYCoordinate = slamYCoordinate
        self.slamRotation = slamRotation
        self.realXCoordinate = realXCoordinate
        self.realYCoordinate = realYCoordinate

    def getMsg(self, vid:int) -> dict:
        msg = super().getMsg(vid)
        if self.slamXCoordinate is not None:
            msg['slamXCoordinate'] = self.slamXCoordinate
        if self.slamYCoordinate is not None:
            msg['slamYCoordinate'] = self.slamYCoordinate
        if self.slamRotation is not None:
            msg['slamRotation'] = self.slamRotation
        if self.realXCoordinate is not None:
            msg['realXCoordinate'] = self.realXCoordinate
        if self.realYCoordinate is not None:
            msg['realYCoordinate'] = self.realYCoordinate
        return msg


class LidarReadingMsg(Message):
    _url_dir = '/lidar-reading'
    def __init__(self, readingDate:str = formatTime(datetime.now()),\
        lidarDistancesReading:str = None):

        super().__init__(readingDate=readingDate)
        self.lidarDistancesReading = lidarDistancesReading

    def getMsg(self, vid:int) -> dict:
        msg = super().getMsg(vid)
        if self.lidarDistancesReading is not None:
            msg['lidarDistancesReading'] = self.lidarDistancesReading
        return msg


class ImuReadingMsg(Message):
    _url_dir = '/imu-reading'
    def __init__(self, readingDate:str = formatTime(datetime.now()),\
        accelerationX:float = None, accelerationY:float = None, accelerationZ:float = None,\
        angularVelocityX:float = None, angularVelocityY:float = None, angularVelocityZ:float = None,\
        magneticFieldX:float = None, magneticFieldY:float = None, magneticFieldZ:float = None):

        super().__init__(readingDate=readingDate)
        self.accelerationX = accelerationX
        self.accelerationY = accelerationY
        self.accelerationZ = accelerationZ
        self.angularVelocityX = angularVelocityX
        self.angularVelocityY = angularVelocityY
        self.angularVelocityZ = angularVelocityZ
        self.magneticFieldX = magneticFieldX
        self.magneticFieldY = magneticFieldY
        self.magneticFieldZ = magneticFieldZ

    def getMsg(self, vid:int) -> dict:
        msg = super().getMsg(vid)
        if self.accelerationX is not None:
            msg['accelerationX'] = self.accelerationX
        if self.accelerationY is not None:
            msg['accelerationY'] = self.accelerationY
        if self.accelerationZ is not None:
            msg['accelerationZ'] = self.accelerationZ
        if self.angularVelocityX is not None:
            msg['angularVelocityX'] = self.angularVelocityX
        if self.angularVelocityY is not None:
            msg['angularVelocityY'] = self.angularVelocityY
        if self.angularVelocityZ is not None:
            msg['angularVelocityZ'] = self.angularVelocityZ
        if self.magneticFieldX is not None:
            msg['magneticFieldX'] = self.magneticFieldX
        if self.magneticFieldY is not None:
            msg['magneticFieldY'] = self.magneticFieldY
        if self.magneticFieldZ is not None:
            msg['magneticFieldZ'] = self.magneticFieldZ
        return msg


class EncoderReadingMsg(Message):
    _url_dir = '/encoder-reading'
    def __init__(self, readingDate:str = formatTime(datetime.now()),\
        leftFrontWheelSpeed:float = None, rightFrontWheelSpeed:float = None,\
        leftRearWheelSpeed:float = None, rightRearWheelSpeed:float = None):

        super().__init__(readingDate=readingDate)
        self.leftFrontWheelSpeed = leftFrontWheelSpeed
        self.rightFrontWheelSpeed = rightFrontWheelSpeed
        self.leftRearWheelSpeed = leftRearWheelSpeed
        self.rightRearWheelSpeed = rightRearWheelSpeed

    def getMsg(self, vid:int) -> dict:
        msg = super().getMsg(vid)
        if self.leftFrontWheelSpeed is not None:
            msg['leftFrontWheelSpeed'] = self.leftFrontWheelSpeed
        if self.rightFrontWheelSpeed is not None:
            msg['rightFrontWheelSpeed'] = self.rightFrontWheelSpeed
        if self.leftRearWheelSpeed is not None:
            msg['leftRearWheelSpeed'] = self.leftRearWheelSpeed
        if self.rightRearWheelSpeed is not None:
            msg['rightRearWheelSpeed'] = self.rightRearWheelSpeed
        return msg


class DiagnosticDataMsg(Message):
    _url_dir = '/diagnostic-data'
    def __init__(self, readingDate:str = formatTime(datetime.now()),\
        wheelsTurnMeasure:float = None, cameraTurnAngle:float = None,\
        batteryChargeStatus:float = None):

        super().__init__(readingDate=readingDate)
        self.wheelsTurnMeasure = wheelsTurnMeasure
        self.cameraTurnAngle = cameraTurnAngle
        self.batteryChargeStatus = batteryChargeStatus

    def getMsg(self, vid:int) -> dict:
        msg = super().getMsg(vid)
        if self.wheelsTurnMeasure is not None:
            msg['wheelsTurnMeasure'] = self.wheelsTurnMeasure
        if self.cameraTurnAngle is not None:
            msg['cameraTurnAngle'] = self.cameraTurnAngle
        if self.batteryChargeStatus is not None:
            msg['batteryChargeStatus'] = self.batteryChargeStatus
        return msg


if __name__ == '__main__':
    print(LocationMsg(\
        slamRotation=5.0,\
        slamYCoordinate=10.0
        ).getMsg(5))
