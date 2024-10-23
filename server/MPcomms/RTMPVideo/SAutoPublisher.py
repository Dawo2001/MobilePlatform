from RTMPVideo.streaming.VideoStreamer import VideoStreamer as VS
import threading

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# SAutoPublisher - synchronized frame publisher, that 
# automaticly sends latest frame to rtmp server
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
class SAutoPublisher(object):

    def __init__(self, streamKey:str, width:int = 640, height:int = 480, fps:int = 30) -> None:
        self._streamer = VS(streamKey, width, height, fps)
        self._fps = fps

        self._timer = None
        self._running = False
        self._interval = 1 / self._fps

        self._nextFrame = None
        self._frameMutex = threading.Lock()
# ---
    def _run(self) -> None:
        frame = self.getFrame()
        self._running = False
        self.start()
        if frame is not None:
            self._streamer.publishFrame(frame)
# ---
    def run_async(self) -> None:
        self._streamer.run()
        self.start()
# ---
    def close(self) -> None:
        self.stop()
        self._streamer.close()
# ---
    def start(self) -> None:
        if not self._running:
            self._timer = threading.Timer(self._interval, self._run)
            self._timer.start()
            self._running = True
# ---
    def stop(self) -> None:
        self._timer.cancel()
        self._running = False
# ---
    def postFrame(self, frame) -> None:
        self._frameMutex.acquire()
        # ---
        self._nextFrame = frame
        # ---
        self._frameMutex.release()
# ---
    def getFrame(self):
        self._frameMutex.acquire()
        # ---
        frame = self._nextFrame
        # ---
        self._frameMutex.release()
        return frame
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---