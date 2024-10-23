# --- --- --- --- --- --- --- --- --- --- --- --- ---
# Example shows how to communicate with control 
# station using API
# --- --- --- --- --- --- --- --- --- --- --- --- ---

# Import used messages from messaging package:
from RestAPI.messaging.Messages import formatTime, ImuReadingMsg, DiagnosticDataMsg

# Import enums used in state variables:
from RestAPI.synchronized.SEmergencyAction import EmergencyActions
from RestAPI.synchronized.SMode import Modes

# Import AccessPoint variable form server package:
from RestAPI.server import restAP 

# Other imports:
import time
import random
from datetime import datetime

if __name__ == "__main__":
    # Start server as daemon:
    restAP.run_async()

    print("Server started on address localhost:5000/api")
    print("Documentation accessible at http://localhost:5000/api/doc")

    while True:
        try:
            # --- --- --- --- --- --- ---
            # --- GENERAL OPERATIONS: ---
            # --- --- --- --- --- --- ---

            # example measurement:
            m_battery = random.uniform(3.2, 4.2)
            m_battery_time = datetime.now()

            time.sleep(1)

            # --- --- --- --- --- --- ---
            
            # --- --- --- --- --- --- ---
            # ---   SEND READINGS:    ---
            # --- --- --- --- --- --- ---

            if(restAP.isActive()): # <- Active state means that there is
                                   #    existing connection that waits for data
            
                # send data with default time (time of creating the message)
                # and all fields provided
                restAP.send(
                    ImuReadingMsg(
                        accelerationX=1.7,
                        accelerationY=1.8,
                        accelerationZ=1.9,
                        angularVelocityX=0.2,
                        angularVelocityY=0.0,
                        angularVelocityZ=0.0,
                        magneticFieldX=0.0,
                        magneticFieldY=0.0,
                        magneticFieldZ=-9.98
                    )
                )

                # send data with time of measurement, but only some fields
                # check if succeded
                f = restAP.send(
                    DiagnosticDataMsg(
                        readingDate=formatTime(m_battery_time),
                        batteryChargeStatus=m_battery
                    )
                )
                print("Message send: " + str(f))

            # --- --- --- --- --- --- ---

            # --- --- --- --- --- --- ---
            # ---   POLL CHANGES:     ---
            # --- --- --- --- --- --- ---

            # Mode changed:
            if(restAP.modeChanged()):
                mode = restAP.pollMode() # <- poll resets _changed flag
                # mode changed routine goes here:
                print("Received new mode: " + str(mode))

            # Emergency changed:
            if(restAP.emergencyActionChanged()):
                ea = restAP.pollEmergencyAction() # <- poll resets _changed flag
                # mode changed routine goes here:
                print("Received new emergency action: " + str(ea))

            # --- --- --- --- --- --- ---

            # --- --- --- --- --- --- ---
            # --- SET API VARIABLES:  ---
            # --- --- --- --- --- --- ---

            if(restAP.lookupEmergencyAction() == EmergencyActions.STOP):
                restAP.setMode(Modes.STANDBY)

            # --- --- --- --- --- --- ---
        except KeyboardInterrupt:
            break
