from flask import Flask, Response, render_template
import cv2


app = Flask(__name__)

@app.route("/")
def index_page():
    return render_template('index.html')

@app.route("/face_detection")
def face_detection():
    return render_template('face.html')

def generate_frames():
    cam = cv2.VideoCapture(0)

    while True:
        ret, frame = cam.read()
        if ret:
            frame = cv2.imencode('.jpg', frame)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            break
        
@app.route("/video")
def video_streaming():

    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug = True)
    