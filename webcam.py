import cv2

class WebCam():
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    def __del__(self):
        self.video.release()
    def get_frame(self):
        ret, frame = self.video.read()
        if ret:
            ret, jpg = cv2.imencode('.jpg',frame)
            
        return jpg.tobytes()
        