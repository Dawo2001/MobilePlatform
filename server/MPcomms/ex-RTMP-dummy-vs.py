import cv2
import RTMPVideo.streaming.VideoStreamer as VS
from RTMPVideo.DummyCap import DummyCap as DCap


if __name__ == "__main__":

    cap = DCap()

    streamer_rgb = VS.VideoStreamer('rgb')

    streamer_rgb.run()

    while True:
        ret, img_rgb = cap.read()
        if ret:
            img_gs = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

            streamer_rgb.publishFrame(img_rgb)

            cv2.imshow('streamer', img_rgb)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    streamer_rgb.close()
