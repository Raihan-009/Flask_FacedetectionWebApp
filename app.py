from flask import Flask, Response, render_template, jsonify
import cv2
import threading
import faceTracker as ft
from queue import Queue
import logging

app = Flask(__name__)

# Global variables for camera management
camera_lock = threading.Lock()
active_camera = None
frame_queue = Queue(maxsize=10)
stop_event = threading.Event()

class CameraManager:
    def __init__(self):
        self.face_tracker = ft.faceDetector()
        self.camera = None
        self.is_running = False
    
    def start(self):
        if self.camera is None:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                raise RuntimeError("Could not start camera")
        self.is_running = True
        
    def stop(self):
        self.is_running = False
        if self.camera is not None:
            self.camera.release()
            self.camera = None
    
    def get_frame(self):
        if not self.is_running or self.camera is None:
            return None
            
        success, frame = self.camera.read()
        if not success:
            return None
            
        # Process frame with face detection
        _, processed_frame = self.face_tracker.findFaces(frame, drawP=True)
        return processed_frame

def camera_stream():
    global active_camera
    
    with camera_lock:
        if active_camera is None:
            active_camera = CameraManager()
        
        try:
            active_camera.start()
        except RuntimeError as e:
            logging.error(f"Camera error: {str(e)}")
            return
    
    while not stop_event.is_set():
        frame = active_camera.get_frame()
        if frame is not None:
            # Encode frame to JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            if ret:
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        
        # Small delay to prevent excessive CPU usage
        cv2.waitKey(1)

@app.route("/")
def index_page():
    return render_template('index.html')

@app.route("/about")
def about_page():
    return render_template("about.html")

@app.route("/face_detection")
def face_tracking():
    return render_template('facetracking.html')

@app.route("/faceTracking")
def faceTracking_streaming():
    stop_event.clear()
    return Response(camera_stream(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/stop_camera")
def stop_camera():
    global active_camera
    
    stop_event.set()
    
    with camera_lock:
        if active_camera is not None:
            active_camera.stop()
            active_camera = None
    
    return jsonify({"status": "success"})

# Cleanup when the flask app stops
def cleanup():
    global active_camera
    if active_camera is not None:
        active_camera.stop()

import atexit
atexit.register(cleanup)

if __name__ == "__main__":
    app.run(debug=True)