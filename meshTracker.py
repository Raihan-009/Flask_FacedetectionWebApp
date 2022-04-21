import cv2
import mediapipe as mp


class MeshDetection():

    def __init__(self, 
                static_image_mode = True, 
                max_num_faces = 2, 
                refine_landmarks = True,
                min_detection_confidence = 0.5,
                min_tracking_confidence = 0.5):

                self.static_image_mode = static_image_mode
                self.max_num_faces = max_num_faces
                self.refine_landmarks = refine_landmarks
                self.min_detection_confidence = min_detection_confidence
                self.min_tracking_confidence = min_tracking_confidence


                self.mpDraw = mp.solutions.drawing_utils
                self.mp_facemesh = mp.solutions.face_mesh
                self.faceMesh = self.mp_facemesh.FaceMesh(self.static_image_mode,self.max_num_faces,refine_landmarks,self.min_detection_confidence,self.min_tracking_confidence)
                self.landmarks_drawing_Spec = self.mpDraw.DrawingSpec(color=(237, 71, 5),thickness = 1, circle_radius = 1)
                self.connection_drawing_spec = self.mpDraw.DrawingSpec(color=(0,0,0), thickness = 1)

    def findFaceMesh(self, img, draw = True):
        self.rgbImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceMesh.process(self.rgbImg)
        faces = []
        if self.results.multi_face_landmarks:
            for faceialLandmarks in self.results.multi_face_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, faceialLandmarks, self.mp_facemesh.FACEMESH_CONTOURS,self.landmarks_drawing_Spec, self.connection_drawing_spec)
                    face = []
                    for id, lm in enumerate(faceialLandmarks.landmark):
                        h,w,c = img.shape
                        x,y = int(lm.x*w), int(lm.y*h)
                        face.append([x,y])
                    faces.append(face)
        return faces,img
        

def main():
    cap = cv2.VideoCapture(0)

    tracker = MeshDetection()
    while True:
        ret, frame = cap.read()
        if ret:
            _, img = tracker.findFaceMesh(frame)
            cv2.imshow("Framing", img)
        else:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()