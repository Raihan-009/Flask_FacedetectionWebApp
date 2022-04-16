import fractions
from flask import Flask, Response, render_template
from webcam import WebCam

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/video")

def video():
    return Response(infiniteLoop(WebCam()), mimetype='multipart/x-mixed-replace; boundary = frame')

def infiniteLoop(webcam):
    while True:
        frame = WebCam.get_frame()
        yield(b'--frame\r\n'
                    b'Content-type: image/jpeg\r\n\r\n' + frame +b'\r\n\r\n')

if __name__ == "__main__":
    app.run(debug = True)
    