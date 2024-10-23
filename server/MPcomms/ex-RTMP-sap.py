import cv2
from RTMPVideo import SAutoPublisher as SAP

if __name__ == "__main__":

    cap = cv2.VideoCapture(0)

    streamer_rgb = SAP.SAutoPublisher('rgb', fps=20)
    streamer_gs = SAP.SAutoPublisher('gs', fps=20)

    streamer_rgb.run_async()
    streamer_gs.run_async()

    while True:
        ret, img_rgb = cap.read()
        if ret:
            img_gs = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

            streamer_rgb.postFrame(img_rgb)
            streamer_gs.postFrame(img_gs)

            cv2.imshow('streamer', img_rgb)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    streamer_rgb.close()
    streamer_gs.close()