import math, numpy as np, cv2

class DummyCap(object):
    T_MAX = 300
    def __init__(self) -> None:
        self.t = 0

    def incrementT(self) -> None:
        self.t += 1
        if self.t > DummyCap.T_MAX:
            self.t -= DummyCap.T_MAX

    def read(self):
        r = 127 + 127 * math.sin(self.t * math.pi / 150)
        b = 127 + 127 * math.cos(self.t * math.pi / 150)
        g = 100

        self.incrementT()

        img = np.zeros((480, 640, 3), np.uint8)
        img[120:360, 160:480] = (b, g, r)

        return True, img
