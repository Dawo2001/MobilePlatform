import RTMPVideo.streaming.VideoStreamer as VS
import numpy as np
import numpy.typing as npt
import sys
from picamera2 import Picamera2
# moje
#import libcamera
from PIL import Image
from measuring_disc_detection import detect_disc
from measuring_disc_detection import distance_to_center
import measuring 
import steering
import steering
import time
import cv2
import camera_server
#import camera_control
#import cv2
#from camera_server import steering_mode

def run(steering_mode, resolution: list = (640, 480), camera_choose: str = 'b'):
    left = True
    right = True
    width = resolution[0]
    height = resolution[1]
    #moje
    manual_mode=1
    if camera_choose == 'l':
        right = False
        print(f"Left camera, resolution: {resolution[0]} x {resolution[1]}")
    elif camera_choose == 'r':
        left = False
        print(f"Right camera, resolution: {resolution[0]} x {resolution[1]}")
    else:
        print(f"Both cameras, resolution: {resolution[0]} x {resolution[1]}")
        width = 2*width
    # moje
    cam = Picamera2()
    preview_config = cam.create_preview_configuration(
        {"format": "RGB888", "size": (2*resolution[0], resolution[1])})
    cam.configure(preview_config)
    cam.start()
    streamer_rgb = VS.VideoStreamer('rgb', width=width, height=height)
    streamer_rgb.run()
    try:
        while True:
            try:
                buffer: npt.NDArray = cam.capture_buffer()
            except Exception as e:
                print("Error getting buffer: ", e)
            frame = np.zeros((resolution[1], 2*resolution[0], 3), np.uint8)
            frame[:, :, 0] = np.reshape(    # R
                buffer[0::3], (resolution[1], 2*resolution[0]))
            frame[:, :, 1] = np.reshape(    # G
                buffer[1::3], (resolution[1], 2*resolution[0]))
            frame[:, :, 2] = np.reshape(    # B
                buffer[2::3], (resolution[1], 2*resolution[0]))
            #moje
            
            try:
                if not right:
                    streamer_rgb.publishFrame(frame[:, :resolution[0], :])
                elif not left:
                    streamer_rgb.publishFrame(frame[:, resolution[0]+1:, :])
                else:
                    streamer_rgb.publishFrame(frame)
                    #    camera_control.main()
                if (manual_mode == 1):
                    ret, f_encoded = cv2.imencode('.bmp', frame)
                    frame2 = cam.capture_array()


                    #moje
                    
                    #cv2.imshow('aa', frame2)

                    img = Image.fromarray(frame, 'RGB')
                    #img = Image.fromarray(f_encoded, 'RGB')
                    img.save("server/MPcomms/my.bmp")
                    image = Image.fromarray(frame, 'RGB')
                    #cv2.imshow('a', frame)

                        #sleep(1)

                    #discX, discY = detect_disc()
                    #distance = distance_to_center(discX, discY)
                    #print(distance)
                    out, dist = measuring.detect_disc(image)
                    #cv2.imshow('pokaz2', out)
                    print(dist)
                    #print("Znalezione:")
                    #print(discX)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break  
                    if(dist[0]>5):
                        for _ in range(int(abs(dist[0])/4)):
                            time.sleep(0.005)
                            steering.right()
                    if(dist[0]<-5):
                        for _ in range(int(abs(dist[0])/4)):
                            time.sleep(0.005)
                            steering.left()
                    if(dist[1]>5):
                        for _ in range(int(abs(dist[1])/1)):
                            time.sleep(0.001)
                            steering.down()
                    if(dist[1]<-5):
                        for _ in range(int(abs(dist[1])/1)):
                            time.sleep(0.001)
                            steering.up()
                    time.sleep(1)
            except Exception as e:
                print("Error sending frame: ", e)
    except KeyboardInterrupt:
        print("Finished")
    except Exception as e:
        print("Something is wrong:", e)
    finally:
        streamer_rgb.close()


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
