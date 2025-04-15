# -*- coding: utf-8 -*-
# -------------------------------
# @项目：hksdk
# @文件：hksdk.py
# @时间：2025/4/15 12:10
# @作者：AI1
# @简介：
# -------------------------------
import cv2
import queue
import threading
from pathlib import Path

from process.video_control import HKCam



def base_dir():
    """
    返回当前文件路径
    """
    FILE = Path(__file__).resolve()
    base_dir = FILE.parents[0]  # YOLOv5 root directory
    base_dir_srt = str(base_dir).replace('\\', '/')
    return base_dir_srt


class VideoCapture:

    def __init__(self, ip, user, pwd):
        # self.cap = cv2.VideoCapture(rtsp)
        self.cap = HKCam(ip, user, pwd, 8000, base_dir() + "/lib/win")
        self.q = queue.Queue()
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    # read frames as soon as they are available, keeping only most recent one
    def _reader(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()  # discard previous (unprocessed) frame
                except queue.Empty:
                    pass
            self.q.put(frame)

    def read(self):
        return self.q.get()



if __name__ == "__main__":

    cap = VideoCapture('192.168.10.170', 'admin', 'ryzh123456')
    while True:
        frame = cap.read()
        # process()
        cv2.imshow("frame", frame)
        if chr(cv2.waitKey(1) & 255) == 'q':
            break