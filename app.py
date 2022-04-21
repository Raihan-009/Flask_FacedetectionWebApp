from flask import Flask, Response, render_template
import cv2
import faceTracker as ft
import handTracker as ht


app = Flask(__name__)

@app.route("/")
def index_page():
    return render_template('index.html')

#Face detection front end
@app.route("/face_detection")
def face_tracking():
    return render_template('facetracking.html')

#face detetcion module
def face_detection():
    face_tracker = ft.faceDetector()
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        if ret:
            _ , frame = face_tracker.findFaces(frame, drawP=False)
            frame = cv2.imencode('.jpg', frame)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            break

#face detection streaming
@app.route("/faceTracking")
def faceTracking_streaming():
    return Response(face_detection(),mimetype='multipart/x-mixed-replace; boundary=frame')

#Hand detection front end
@app.route("/hand_detection")
def hand_tracking():
    return render_template("handtracking.html")
#face detection module
def hand_detection():
    hand_tracker = ht.handTracker()
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        if ret:
            hands = hand_tracker.findHands(frame)
            frame = cv2.imencode('.jpg', frame)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            break
#hand detection streaming
@app.route("/handtracking")
def handTracking_streaming():
    return Response(hand_detection(),mimetype='multipart/x-mixed-replace; boundary=frame')

#Mesh Detection front end
@app.route("/mesh_detection")
def mesh_tracking():
    return render_template("meshtracking.html")


#original video streaming
def original_face():
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        if ret:
            frame = cv2.imencode('.jpg', frame)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            break
        

@app.route("/originalface")
def originalFace_streaming():
    return Response(original_face(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug = True)
    