import cv2
import mediapipe as mp

class faceDetector():
    def __init__(self,
                min_detection_confidence=0.5):
        self.min_detection_confidence= min_detection_confidence
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_draw = mp.solutions.drawing_utils

        self.faceDetection = self.mp_face_detection.FaceDetection(self.min_detection_confidence)

    def findFaces(self,img, draw = True, drawP = True):
        rgbImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceDetection.process(rgbImg)
        face_info = []

        if self.results.detections:
            for id,detection in enumerate(self.results.detections):
                _bbox = detection.location_data.relative_bounding_box

                h,w,c = img.shape
                bbox = int(_bbox.xmin*w), int(_bbox.ymin*h), int(_bbox.width*w), int(_bbox.height*h)
                face_info.append([bbox,detection.score])

                if draw:
                    cv2.rectangle(img, bbox, (0,255,0), 2)
                    if drawP:
                        cv2.putText(img,f'{int(detection.score[0]*100)}%',(bbox[0], bbox[1]-25), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,255),2)

        return face_info, img

def main():
    cap = cv2.VideoCapture(0)
    tracker = faceDetector()
    while True:
        ret, frame = cap.read()
        if ret:
            _ , img = tracker.findFaces(frame, drawP=False)
            cv2.imshow("Framing", img)
        else:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()