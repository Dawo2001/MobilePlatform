#!/usr/bin/env python3
import ffmpeg
import cv2

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# VideoStreamer - rtmp video provider class:
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
class VideoStreamer:
    __RTMP_ADDRESS = "rtmp://localhost/live" # for provided nginx settings it stays the same
# ---
    def __init__(self, streamKey:str, width:int = 640, height:int = 480, fps:int = 10):
        self._streamKey = streamKey
        self._running = False
        self._width = width
        self._height = height
        self._fps = fps
# ---
    def getRTMPAddress(self) -> str:
        return VideoStreamer.__RTMP_ADDRESS + '/' + self._streamKey
# ---
    def getResolution(self) -> str:
        return str(self._width) + 'x' + str(self._height)
# ---
    def getFPS(self) -> int:
        return self._fps
# ---
    def run(self):
        if not self._running:
            if self._fps is None:
                self.stream = (
                    ffmpeg
                    .input('pipe:')
                    .output(self.getRTMPAddress(),
                    vcodec='libx264',
                    pix_fmt='yuv420p', 
                    preset='ultrafast',
                    tune='zerolatency',
                    s=self.getResolution(),
                    format='flv',
                    loglevel="panic")
                )
            else:
                self.stream = (
                    ffmpeg
                    .input('pipe:')
                    .output(self.getRTMPAddress(),
                    vcodec='libx264',
                    pix_fmt='yuv420p', 
                    preset='ultrafast',
                    tune='zerolatency',
                    s=self.getResolution(),
                    r=self.getFPS(),
                    format='flv',
                    loglevel="panic")
                )
            self.process = ffmpeg.run_async(self.stream, pipe_stdin=True)
            self._running = True
# ---
    def publishFrame(self, frame) -> None:
        ret, f_encoded = cv2.imencode('.bmp', frame)
        if ret:
            self.write_bytes(f_encoded.tobytes())
# ---
    def write_bytes(self, bytes):
        self.process.stdin.write(bytes)
# ---
    def close(self):
        if self._running:
            self.process.stdin.close()
            self.process.terminate()
            self._running = False
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
