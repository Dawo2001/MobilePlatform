


# Receive steering inputs from WiFi and set actuator outputs for:
#  - Main brushed motor
#  - Steering servo
#  - Four suspension servos
import time
from misc.InterruptibleLoop import InterruptibleLoop
import socket, struct
import MPcomms.steering as steering
HOST='0.0.0.0'
PORT=5734




def main():
    connected = False
    loop = InterruptibleLoop()
    steering.setup_pins()



    # setup radio server:
    ss:socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss.bind((HOST, PORT))
    ss.listen(1)
    ss.settimeout(1)

    print('Radio server started! Waiting for connection on: ' + HOST +':' + str(PORT))

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

        s.settimeout(0.5)
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
            if len(byte_data) < 24:
                continue

            data = struct.unpack('!6f', byte_data)
            byte_data = b''

            inputs = [round(data[i],1) for i in range(6)]
            print(inputs)
            if(inputs[0]==1):
                for _ in range(30):
                    time.sleep(0.001)
                    steering.left()
            if(inputs[1]==1):
                for _ in range(30):
                    time.sleep(0.001)
                    steering.right()   
            if(inputs[2]==1):
                for _ in range(30):
                    time.sleep(0.001)
                    steering.up()
            if(inputs[3]==1):
                for _ in range(30):
                    time.sleep(0.001)
                    steering.down() 
            if(inputs[4]==1):
                steering.laser_on()     
            if(inputs[5]==1):
                steering.laser_off()
            # set inputs:
            
    

    # clean up after steering:
    if connected:
        s.close()
        connected = False
    ss.close()


if __name__ == '__main__':
    main()
