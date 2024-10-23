from RestAPI.server import restAP
import time
import threading
import CameraRead
import sys
import steering
# moje
import libcamera
from misc.InterruptibleLoop import InterruptibleLoop
import socket, struct
from measuring_disc_detection import detect_disc
from measuring_disc_detection import distance_to_center

from RestAPI.synchronized.SControl import Control
HOST='0.0.0.0'
PORT=5734



def run(resolution: list = (640, 480), camera_choose: str = 'b'):
    #moje   
    steering_mode = 0
    def run_camera():
        CameraRead.run(steering_mode, resolution, camera_choose)
    cameras_thread = threading.Thread(target=run_camera)
    cameras_thread.daemon = True
    cameras_thread.start()
        
    steering.setup_pins()

    #moje
    #steering.basing()
    connected = False
    loop = InterruptibleLoop()
    steering.setup_pins()
    steering.laser_on()
    # setup radio server:
    ss:socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss.bind((HOST, PORT))
    ss.setblocking(False)
    ss.listen(1)
    #ss.setblocking(False)
    ss.settimeout(5)
    print('Radio server started! Waiting for connection on: ' + HOST +':' + str(PORT))
    # Start server as daemon:
    restAP.run_async()
    print("Server started on address localhost:5000/api")
    print("Documentation accessible at http://localhost:5000/api/doc")

    control = Control()
    while loop.loop_again:

        # accept client:
        try:
            s, address = ss.accept()
            connected = True
        except socket.error:
            # timeout on accept, loop again
            continue
        print("Accepted connection from " + str(address))
        print("Radio receiving...")

        s.settimeout(10)
        byte_data:bytes = b''
        while loop.loop_again:
            try:
                byte = s.recv(1)
            except socket.error:
                # Failed receiving data, reconnect socket
                print("Socket disconnected!")
                s.close()
                connected = False
                break

            if len(byte) == 0:
                print("Socket disconnected!")
                s.close()
                connected = False
                break
            byte_data += bytes(byte)
            
            if len(byte_data) < 32:
                continue
            data = struct.unpack('!8f', byte_data)
            byte_data = b''

            inputs = [round(data[i],1) for i in range(8)]
            #distance = [0, 0]

            print(inputs)
            '''
            if(steering_mode == 1):
                try:
                    if(inputs[0]>5):
                        for _ in range(int(abs(inputs[0])/2)):
                            time.sleep(0.005)
                            steering.left()
                    if(inputs[0]<-5):
                        for _ in range(int(abs(inputs[0])/2)):
                            time.sleep(0.005)
                            steering.right()
                    if(inputs[1]>5):
                        for _ in range(int(abs(inputs[1]))*4):
                            time.sleep(0.001)
                            steering.up()
                    if(inputs[1]<-5):
                        for _ in range(int(abs(inputs[1]))*4):
                            time.sleep(0.001)
                            steering.down()
                    
                except Exception as e:    
                    pass
'''
                    
                    
            if(steering_mode == 0):    
                if(inputs[5]==1):
                    angle2 = 15
                    if(inputs[0]==-1):
                        for _ in range(angle2):
                            if(inputs[0]!=-1):
                                break
                            time.sleep(0.005)
                            steering.left()
                    if(inputs[0]==1):
                        for _ in range(angle2):
                            if(inputs[0]!=1):
                                break
                            time.sleep(0.005)
                            steering.right()   
                    if(inputs[1]==-1):
                        for _ in range(angle2):
                            if(inputs[1]!=-1):
                                break
                            time.sleep(0.005)
                            steering.up()
                    if(inputs[1]==1):
                        for _ in range(angle2):
                            if(inputs[1]!=1):
                                break
                            time.sleep(0.005)
                            steering.down() 
      
                if(inputs[5]==0):  
                    angle = 30      
                    if(inputs[0]==-1):
                        for _ in range(angle):
                            if(inputs[0]!=-1):
                                break
                            time.sleep(0.001)
                            steering.left()
                    if(inputs[0]==1):
                        for _ in range(angle):
                            if(inputs[0]!=1):
                                break
                            time.sleep(0.001)
                            steering.right()   
                    if(inputs[1]==-1):
                        for _ in range(angle):
                            if(inputs[1]!=-1):
                                break
                            time.sleep(0.001)
                            steering.up()
                    if(inputs[1]==1):
                        for _ in range(angle):
                            if (inputs[1]!=1):
                                break
                            time.sleep(0.001)
                            steering.down()                     
                  
            if(inputs[6]==1):
                steering_mode = 0
                print("manual")     
            if(inputs[7]==1):
                steering_mode = 1
                print("automatic")
                
                
            if(inputs[4]==1):
                kat = 65
                for _ in range(kat):
                    time.sleep(0.001)
                    steering.left()
                time.sleep(10)
                for _ in range(kat):
                    time.sleep(0.001)
                    steering.right()
                time.sleep(10)    
                for _ in range(2*kat):
                    time.sleep(0.001)
                    steering.left()
                time.sleep(10)
                for _ in range(2*kat):
                    time.sleep(0.001)
                    steering.right()
                time.sleep(10)   
                for _ in range(3*kat):
                    time.sleep(0.001)
                    steering.left()
                time.sleep(10)
                for _ in range(3*kat):
                    time.sleep(0.001)
                    steering.right()
                time.sleep(10)   
                for _ in range(4*kat):
                    time.sleep(0.001)
                    steering.left()
                time.sleep(10)
                for _ in range(4*kat):
                    time.sleep(0.001)
                    steering.right()
                time.sleep(10)        
                for _ in range(5*kat):
                    time.sleep(0.001)
                    steering.left()
                time.sleep(10)
                for _ in range(5*kat):
                    time.sleep(0.001)
                    steering.right()
                time.sleep(10)   
                for _ in range(6*kat):
                    time.sleep(0.001)
                    steering.left()
                time.sleep(10)
                for _ in range(6*kat):
                    time.sleep(0.001)
                    steering.right()
                time.sleep(10)   
                for _ in range(7*kat):
                    time.sleep(0.001)
                    steering.left()
                time.sleep(10)
                for _ in range(7*kat):
                    time.sleep(0.001)
                    steering.right()
                time.sleep(10) 
                for _ in range(8*kat):
                    time.sleep(0.001)
                    steering.left()
                time.sleep(10)
                for _ in range(8*kat):
                    time.sleep(0.001)
                    steering.right()
                time.sleep(10) 
            
            if(inputs[3]==1):
                kat=200

                for _ in range(kat):
                    time.sleep(0.001)
                    steering.down()
                time.sleep(10)    
                for _ in range(kat):
                    time.sleep(0.001)
                    steering.up()
                time.sleep(10)
                for _ in range(2*kat):
                    time.sleep(0.001)
                    steering.down()
                time.sleep(10)   
                for _ in range(2*kat):
                    time.sleep(0.001)
                    steering.up()
                time.sleep(10)
                for _ in range(3*kat):
                    time.sleep(0.001)
                    steering.down()
                time.sleep(10)   
                for _ in range(3*kat):
                    time.sleep(0.001)
                    steering.up()
                time.sleep(10)
                for _ in range(4*kat):
                    time.sleep(0.001)
                    steering.down()
                time.sleep(10)   
                for _ in range(4*kat):
                    time.sleep(0.001)
                    steering.up()
                time.sleep(10)
                for _ in range(5*kat):
                    time.sleep(0.001)
                    steering.down()
                time.sleep(10)    
                for _ in range(5*kat):
                    time.sleep(0.001)
                    steering.up()
                time.sleep(10)
                for _ in range(6*kat):
                    time.sleep(0.001)
                    steering.down()
                time.sleep(10)   
                for _ in range(6*kat):
                    time.sleep(0.001)
                    steering.up()
                time.sleep(10)
                for _ in range(7*kat):
                    time.sleep(0.001)
                    steering.down()
                time.sleep(10)   
                for _ in range(7*kat):
                    time.sleep(0.001)
                    steering.up()
                time.sleep(10)
           
           
            # set inputs:
            
'''    try:
        while True:
            time.sleep(0.001)
				#if(restAP.isActive()):
				#	if(restAP.controlChanged()):
				#		control = restAP.pollControl()
				#		print("Received new control: " + str(control))
				#	control = perform_control(control)

    except KeyboardInterrupt:
        exit()
'''

def perform_control(control: Control) -> Control:
    if control.laser:
        steering.laser_on()
    else:
        steering.laser_off()

    pan_steps_per_degree = 1240/360
    tilt_steps_per_degree = 1400/8

    pan_degrees_per_step = 1/pan_steps_per_degree
    tilt_degrees_per_step = 1/tilt_steps_per_degree

    pan_diff = control.set_pan-control.current_pan
    pan_angle = 0
    if pan_diff <= -pan_degrees_per_step:
        steering.left()
        pan_angle = -pan_degrees_per_step
    if pan_diff >= pan_degrees_per_step:
        steering.right()
        pan_angle = pan_degrees_per_step

    tilt_diff = control.set_tilt-control.current_tilt
    tilt_angle = 0
    if tilt_diff <= -tilt_degrees_per_step:
        steering.down()
        tilt_angle = -tilt_degrees_per_step
    if tilt_diff >= tilt_degrees_per_step:
        steering.up()
        tilt_angle = tilt_degrees_per_step

    restAP.updateControl(pan_angle, tilt_angle)
    return restAP.lookupControl()


if __name__ == "__main__":
    args = sys.argv
    nums = [int(arg) for arg in args if arg.isdecimal()]

    if "-r" in args and "-l" not in args:
        if len(nums) == 2:
            run(nums, 'r')
        else:
            run(camera_choose='r')
    elif "-r" not in args and "-l" in args:
        if len(nums) == 2:
            run(nums, 'l')
        else:
            run(camera_choose='l')
    else:
        if len(nums) == 2:
            run(nums)
        else:
            run()
