from enum import Enum

class Magic(Enum):
    MODE_CHANGE             = 0x7D81 # 32129
    EMERGENCY_ACTION_SET    = 0x7AE4 # 31460
    CONNECTION_ADD          = 0xEE15 # 60949
    CONNECTION_DELETE       = 0x3AD5 # 15061
    CONNECTION_TOGGLE       = 0x5C25 # 23589
    TOWER_CONTROL           = 0xAB13 # 43795