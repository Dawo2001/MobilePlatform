import random


class LidarReadings:
    _READINGS = (
        "[300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 252.25780463644728, 246.56439321199645, 241.6795398870165, 237.53947040439405, 233.1222855069845, 230.32585612562042, 244.6752950340512, 261.9637379485947, 300.0, 300.0, 78.44743462982075, 77.88452991448301, 77.12976079309465, 76.68767828015137, 76.11832893594026, 75.8023746329889, 75.4254598925323, 75.23961722390672, 75.1065909225016, 75.0066663703967, 75.0, 75.0066663703967, 75.1065909225016, 75.23961722390672, 75.53806987208503, 75.8023746329889, 76.11832893594026, 76.68767828015137, 77.12976079309465, 77.88452991448301, 78.74642849044012, 300.0, 300.0, 263.2812184718082, 245.10609947530887, 230.7834482799839, 233.60008561642266, 237.53947040439405, 242.21065211918324, 247.1214276423637, 252.84184780213894, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 141.12760183606892, 106.16967551989597, 106.38138934982942, 106.6770828247567, 107.20074626605917, 107.68936809174804, 108.4665847162157, 109.14210919713803, 110.16351483136329, 111.01801655587259, 112.27199116431488, 113.65298060323803, 115.15641536623133, 116.77756633874505, 118.51160280748886, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 117.17081547894082, 115.45128842936315, 113.84638773364749, 112.36102527122117, 111.32834320154055, 110.06361796706484, 109.20164833920778, 108.17116066678771, 107.28000745712129, 106.70520137275409, 106.21205204683694, 105.68348972285122, 105.38500842150178, 105.17128885774862, 141.12760183606892]"
    )

    def getNext():
        return LidarReadings._READINGS[0]


class PointCloudReading:
    _READINGS = (
        "Dummy point cloud reading: [0, 0, 0, 0, 0, 0, 100, 100, 100, 100, 100, 0, 0, 0, 0, 100, 100, 0, 0, 0, 100, 0, 100]"
    )

    def getNext():
        return PointCloudReading._READINGS[0]


class LocationReadings:
    _MAX_IDX = 10
    _idx = random.randint(0, 9)

    _READINGS = (
        {
            "slamXCoordinate": 0.00001249999986979166,
            "slamYCoordinate": 0.04999999843750002,
            "slamRotation": 0.0005000000000000003,
            "realXCoordinate": 0.04999999843750001,
            "realYCoordinate": -99.99998750000013
        },
        {
            "slamXCoordinate": 0.09462996819559619,
            "slamYCoordinate": 4.3493743975400285,
            "slamRotation": 0.04350740630296774,
            "realXCoordinate": 4.349374397540019,
            "realYCoordinate": -99.90537003180441
        },
        {
            "slamXCoordinate": 0.9392820363481934,
            "slamYCoordinate": 13.67386743352836,
            "slamRotation": 0.13716790498877,
            "realXCoordinate": 13.67386743352836,
            "realYCoordinate": -99.06071796365181
        },
        {
            "slamXCoordinate": 3.4321544737958845,
            "slamYCoordinate": 25.97410570708251,
            "slamRotation": 0.2627524852495792,
            "realXCoordinate": 25.974105707082522,
            "realYCoordinate": -96.56784552620412
        },
        {
            "slamXCoordinate": 8.22660756287783,
            "slamYCoordinate": 39.71969316384545,
            "slamRotation": 0.40845719907903805,
            "realXCoordinate": 39.71969316384537,
            "realYCoordinate": -91.77339243712217
        },
        {
            "slamXCoordinate": 15.640114022811753,
            "slamYCoordinate": 53.69759742828163,
            "slamRotation": 0.5668426152137174, 
            "realXCoordinate": 53.69759742828163,
            "realYCoordinate": -84.35988597718827
        },
        {
            "slamXCoordinate": 25.697997844102748,
            "slamYCoordinate": 66.92723616469715,
            "slamRotation": 0.7332200364911564,
            "realXCoordinate": 66.92723616469708,
            "realYCoordinate": -74.3020021558972
        },
        {
            "slamXCoordinate": 39.729474276300046,
            "slamYCoordinate": 79.7968533216388,
            "slamRotation": 0.9239026935777171,
            "realXCoordinate": 79.79685332163875,
            "realYCoordinate": -60.27052572370003
        },
        {
            "slamXCoordinate": 54.5308691190909,
            "slamYCoordinate": 89.0655304627534,
            "slamRotation": 1.0987621644209369,
            "realXCoordinate": 89.06553046275337,
            "realYCoordinate": -45.46913088090913
        },
        {
            "slamXCoordinate": 70.90082825030797,
            "slamYCoordinate": 95.6733616131351,
            "slamRotation": 1.2755223489542085,
            "realXCoordinate": 95.67336161313519,
            "realYCoordinate": -29.099171749692175
        }
    )

    def getNext():
        LocationReadings._idx += 1
        if LocationReadings._idx >= LocationReadings._MAX_IDX:
            LocationReadings._idx -= LocationReadings._MAX_IDX
        return LocationReadings._READINGS[LocationReadings._idx]


class ImuReading:
    _MAX_IDX = 10
    _idx = random.randint(0, 9)

    _READINGS = (
        {
            "accelerationX": 0.009999999999999998,
            "accelerationY": 9.5,
            "accelerationZ": -9.81,
            "angularVelocityX": 0,
            "angularVelocityY": 0,
            "angularVelocityZ": 0.005,
            "magneticFieldX": 0.9999998750000026,
            "magneticFieldY": 0.0004999999791666669,
            "magneticFieldZ": 0
        },
        {
            "accelerationX": 0.6440481757271377,
            "accelerationY": 5.987369392383789,
            "accelerationZ": -9.81,
            "angularVelocityX": 0,
            "angularVelocityY": 0,
            "angularVelocityZ": 0.07710136510370116,
            "magneticFieldX": 0.9990537020826922,
            "magneticFieldY": 0.04349368178100419,
            "magneticFieldZ": 0
        },
        {
            "accelerationX": 1.5507541451030387,
            "accelerationY": 3.773536025353076,
            "accelerationZ": -9.81,
            "angularVelocityX": 0,
            "angularVelocityY": 0,
            "angularVelocityZ": 0.12254320790064736,
            "magneticFieldX": 0.9906072239023345,
            "magneticFieldY": 0.136738172989514,
            "magneticFieldZ": 0
        },
        {
            "accelerationX": 2.323631427358352,
            "accelerationY": 2.378268852553325,
            "accelerationZ": -9.81,
            "angularVelocityX": 0,
            "angularVelocityY": 0,
            "angularVelocityZ": 0.1511829025002212,
            "magneticFieldX": 0.9656787078334639,
            "magneticFieldY": 0.2597395488505584,
            "magneticFieldZ": 0
        },
        {
            "accelerationX": 2.8907463206447486,
            "accelerationY": 1.4989025404881566,
            "accelerationZ": -9.81,
            "angularVelocityX": 0,
            "angularVelocityY": 0,
            "angularVelocityZ": 0.1692330531162957,
            "magneticFieldX": 0.917734705929781,
            "magneticFieldY": 0.3971939193038816,
            "magneticFieldZ": 0
        },
        {
            "accelerationX": 3.2799510434999664,
            "accelerationY": 0.9446824413773776,
            "accelerationZ": -9.81,
            "angularVelocityX": 0,
            "angularVelocityY": 0,
            "angularVelocityZ": 0.18060914988751695,
            "magneticFieldX": 0.8436006018671552,
            "magneticFieldY": 0.5369711580051328,
            "magneticFieldZ": 0
        },
        {
            "accelerationX": 3.5378709173319782,
            "accelerationY": 0.5953855510552977,
            "accelerationZ": -9.81,
            "angularVelocityX": 0,
            "angularVelocityY": 0,
            "angularVelocityZ": 0.18777892816254915,
            "magneticFieldX": 0.7430231982787926,
            "magneticFieldY": 0.6692656623640227,
            "magneticFieldZ": 0
        },
        {
            "accelerationX": 3.719899642290478,
            "accelerationY": 0.35647932250560466,
            "accelerationZ": -9.81,
            "angularVelocityX": 0,
            "angularVelocityY": 0,
            "angularVelocityZ": 0.1926827928538323,
            "magneticFieldX": 0.6027105615697972,
            "magneticFieldY": 0.797959885565822,
            "magneticFieldZ": 0
        },
        {
            "accelerationX": 3.8222823741487697,
            "accelerationY": 0.22467088258818535,
            "accelerationZ": -9.81,
            "angularVelocityX": 0,
            "angularVelocityY": 0,
            "angularVelocityZ": 0.19538833451529508,
            "magneticFieldX": 0.4546989418141456,
            "magneticFieldY": 0.8906452000168733,
            "magneticFieldZ": 0
        },
        {
            "accelerationX": 3.8875230546664206,
            "accelerationY": 0.14159869113350965,
            "accelerationZ": -9.81,
            "angularVelocityX": 0,
            "angularVelocityY": 0,
            "angularVelocityZ": 0.19709350055041738,
            "magneticFieldX": 0.29100198179325676,
            "magneticFieldY": 0.9567224501350415,
            "magneticFieldZ": 0
        }
    )

    def getNext():
        ImuReading._idx += 1
        if ImuReading._idx >= ImuReading._MAX_IDX:
            ImuReading._idx -= ImuReading._MAX_IDX
        return ImuReading._READINGS[ImuReading._idx]


class EncoderReading:
    _MAX_IDX = 10
    _idx = random.randint(0, 9)

    _READINGS = (
        {
            "leftFrontWheelSpeed": 4.91127171875,
            "rightFrontWheelSpeed": 4.91127171875,
            "leftRearWheelSpeed": 4.91127171875,
            "rightRearWheelSpeed": 4.91127171875
        },
        {
            "leftFrontWheelSpeed": 10.49033790724717,
            "rightFrontWheelSpeed": 10.49033790724717,
            "leftRearWheelSpeed": 10.49033790724717,
            "rightRearWheelSpeed": 10.49033790724717
        },
        {
            "leftFrontWheelSpeed": 14.006541079362036,
            "rightFrontWheelSpeed": 14.006541079362036,
            "leftRearWheelSpeed": 14.006541079362036,
            "rightRearWheelSpeed": 14.006541079362036
        },
        {
            "leftFrontWheelSpeed": 16.22262605305923,
            "rightFrontWheelSpeed": 16.22262605305923,
            "leftRearWheelSpeed": 16.22262605305923,
            "rightRearWheelSpeed": 16.22262605305923
        },
        {
            "leftFrontWheelSpeed": 17.73834668464989,
            "rightFrontWheelSpeed": 17.73834668464989,
            "leftRearWheelSpeed": 17.73834668464989,
            "rightRearWheelSpeed": 17.73834668464989
        },
        {
            "leftFrontWheelSpeed": 18.574594332998885,
            "rightFrontWheelSpeed": 18.574594332998885,
            "leftRearWheelSpeed": 18.574594332998885,
            "rightRearWheelSpeed": 18.574594332998885
        },
        {
            "leftFrontWheelSpeed": 19.10163891975443,
            "rightFrontWheelSpeed": 19.10163891975443,
            "leftRearWheelSpeed": 19.10163891975443,
            "rightRearWheelSpeed": 19.10163891975443
        },
        {
            "leftFrontWheelSpeed": 19.43380845945567,
            "rightFrontWheelSpeed": 19.43380845945567,
            "leftRearWheelSpeed": 19.43380845945567,
            "rightRearWheelSpeed": 19.43380845945567
        },
        {
            "leftFrontWheelSpeed": 19.64315811578087,
            "rightFrontWheelSpeed": 19.64315811578087,
            "leftRearWheelSpeed": 19.64315811578087,
            "rightRearWheelSpeed": 19.64315811578087
        },
        {
            "leftFrontWheelSpeed": 19.775100613105877,
            "rightFrontWheelSpeed": 19.775100613105877,
            "leftRearWheelSpeed": 19.775100613105877,
            "rightRearWheelSpeed": 19.775100613105877
        }
    )

    def getNext():
        EncoderReading._idx += 1
        if EncoderReading._idx >= EncoderReading._MAX_IDX:
            EncoderReading._idx -= EncoderReading._MAX_IDX
        return EncoderReading._READINGS[EncoderReading._idx]

class DiagnosticReading:
    _MAX_IDX = 10
    _idx = random.randint(0, 9)

    _READINGS = (
        {
            "wheelsTurnMeasure": 0.7853982,
            "cameraTurnAngle": 0,
            "batteryChargeStatus": 0.98358804
        },
        {
            "wheelsTurnMeasure": 0.7853982,
            "cameraTurnAngle": 0,
            "batteryChargeStatus": 0.91685617
        },
        {
            "wheelsTurnMeasure": 0.7853982,
            "cameraTurnAngle": 0,
            "batteryChargeStatus": 0.8306505
        },
        {
            "wheelsTurnMeasure": 0.7853982,
            "cameraTurnAngle": 0,
            "batteryChargeStatus": 0.74528414
        },
        {
            "wheelsTurnMeasure": 0.7853982,
            "cameraTurnAngle": 0,
            "batteryChargeStatus": 0.660951
        },
        {
            "wheelsTurnMeasure": 0.7853982,
            "cameraTurnAngle": 0,
            "batteryChargeStatus": 0.59627354
        },
        {
            "wheelsTurnMeasure": 0.7853982,
            "cameraTurnAngle": 0,
            "batteryChargeStatus": 0.54139835
        },
        {
            "wheelsTurnMeasure": 0.7853982,
            "cameraTurnAngle": 0,
            "batteryChargeStatus": 0.4948639
        },
        {
            "wheelsTurnMeasure": 0.7853982,
            "cameraTurnAngle": 0,
            "batteryChargeStatus": 0.45521173
        },
        {
            "wheelsTurnMeasure": 0.7853982,
            "cameraTurnAngle": 0,
            "batteryChargeStatus": 0.42118153
        }
    )

    def getNext():
        DiagnosticReading._idx += 1
        if DiagnosticReading._idx >= DiagnosticReading._MAX_IDX:
            DiagnosticReading._idx -= DiagnosticReading._MAX_IDX
        return DiagnosticReading._READINGS[DiagnosticReading._idx]