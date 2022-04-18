from flask import Flask, Response, render_template
import cv2
import faceTracker as ft


app = Flask(__name__)

@app.route("/")
def index_page():
    return render_template('index.html')

@app.route("/face_detection")
def face():
    return render_template('facetracking.html')

def face_detection():
    tracker = ft.faceDetector()
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        if ret:
            _ , frame = tracker.findFaces(frame, drawP=False)
            frame = cv2.imencode('.jpg', frame)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            break
def original_face():
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        if ret:
            frame = cv2.imencode('.jpg', frame)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            break
        
@app.route("/faceTracking")
def faceTracking_streaming():
    return Response(face_detection(),mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route("/originalface")
def originalFace_streaming():
    return Response(original_face(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug = True)
    