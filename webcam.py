import cv2
from flask import Response

def generate_frames():
    cam = cv2.VideoCapture(0)

    while True:
        ret, frame = cam.read()
        if ret:
            frame = cv2.imencode('.jpg', frame)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            break

def video_streaming():

    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')
        

    