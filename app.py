from flask import Flask, Response, render_template
import cv2
import faceTracker as ft
import handTracker as ht
import meshTracker as mt
import fingerCounter as fc
import fingerIdentifier as fi
import blinkedCounter as bc


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

#mesh detection module
def mesh_detection():
    mesh_tracker = mt.MeshDetection()
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        if ret:
            _, img = mesh_tracker.findFaceMesh(frame)
            frame = cv2.imencode('.jpg', frame)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            break

#mesh detection streaming
@app.route("/meshtracking")
def meshtracking_streaming():
    return Response(mesh_detection(),mimetype='multipart/x-mixed-replace; boundary=frame')    

#finger Counter front end
@app.route("/finger_counter")
def counted_finger_tracking():
    return render_template("fingercounter.html")

#finger counting module
def finger_counting():
    hand_tracker = ht.handTracker()
    finger_counter = fc.FingerCounter()
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        cv2.rectangle(frame, (10,10), (250,30), (255,255,255), cv2.FILLED)
        cv2.putText(frame, 'Project Finger Counting', (15,25), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,0,0), 1)
        if ret:
            hands = hand_tracker.findHands(frame)
            
            if hands:
                oneHand = hands[0]
                first_five = finger_counter.fingerOrientation(oneHand)

                if (len(hands) == 2):
                    secondHand = hands[1]
                    second_five = finger_counter.fingerOrientation(secondHand)
                    cv2.rectangle(frame, (10,50), (245,200), (55,245,10), cv2.FILLED)
                    cv2.putText(frame, str(first_five + second_five), (65,175), cv2.FONT_HERSHEY_COMPLEX, 4, (0,0,0), 20)
                else:
                    cv2.rectangle(frame, (40,50), (200,200), (55,245,10), cv2.FILLED)
                    cv2.putText(frame, str(first_five), (75,175), cv2.FONT_HERSHEY_COMPLEX, 4, (0,0,0), 20)
            frame = cv2.imencode('.jpg', frame)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            break

#counted finger streaming
@app.route("/countedfingerStreaming")
def fingerCounting_streaming():
    return Response(finger_counting(),mimetype='multipart/x-mixed-replace; boundary=frame')   
    
#finger Identifier front end
@app.route("/finger_identifier")
def identified_finger_tracking():
    return render_template("fingeridentifier.html")

#finger Identification module
def finger_identification():
    cam = cv2.VideoCapture(0)
    hand_tracker = ht.handTracker()
    finger_identifier = fi.fingerIdentifier()
    while True:
        ret, frame = cam.read()
        cv2.rectangle(frame, (10,10), (525,45), (255,255,255), cv2.FILLED)
        cv2.putText(frame, 'Project Finger Identification', (15,35), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 2)
        if ret:
            hands = hand_tracker.findHands(frame)
            if hands:
                oneHand = hands[0]
                finger_1 = finger_identifier.fingerOrientation(oneHand)
                context = finger_identifier.fingerIdentification(finger_1)
                cv2.rectangle(frame, (10,50), (325,95), (255,255,255), cv2.FILLED)
                cv2.putText(frame, context, (15,75), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,74,186), 2)
            frame = cv2.imencode('.jpg', frame)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            break

#identified finger streaming
@app.route("/identifiedfingerStreaming")
def fingerIdentification_streaming():
    return Response(finger_identification(),mimetype='multipart/x-mixed-replace; boundary=frame')

#blinked counter front end
@app.route("/blinked_counter")
def blinked_counter_tracking():
    return render_template("blinkedcounter.html")

#blinked counter module
def blinked_detection():
    mesh_tracker = mt.MeshDetection()
    cam = cv2.VideoCapture(0)
    tracker = bc.BlinkCounter()
    while True:
        ret, frame = cam.read()
        cv2.rectangle(frame, (10,10), (345,45), (255,255,255), cv2.FILLED)
        cv2.putText(frame, 'Eye Blink Counter', (15,35), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 2)
        if ret:
            faces, img = mesh_tracker.findFaceMesh(frame, draw=False)
            if faces:
                face = faces[0]
                #print(face)
                value = tracker.blinkCounter(img,face, drawE=True)
                # print(value)
                cv2.rectangle(frame, (10,50), (150,95), (255,255,255), cv2.FILLED)
                cv2.putText(frame, "Count : "+ str(value), (15,80), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,74,186), 2)
                frame = cv2.imencode('.jpg', frame)[1].tobytes()
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            break

#blinked counter streaming
@app.route("/blinkedcounterStreaming")
def blinkedcounter_streaming():
    return Response(blinked_detection(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug = True)
    