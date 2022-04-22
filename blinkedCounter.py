import cv2
import meshTracker as mt
import measurementMeter as ms


mesh_tracker = mt.MeshDetection()
distance_finder = ms.Measurement()

class BlinkCounter():
    def __init__(self):
        self.left_eye_IDs = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]
        self.ratioList = []
        self.eyeBlinkCounter = 0
        self.counter = 0
        self.color = (255, 0, 255)
    

    def blinkCounter(self,img,face, drawE = True):
        if face:
            for id in self.left_eye_IDs:
                if drawE:
                    cv2.circle(img,face[id],2,self.color,2)

            leftUp = face[159]
            leftDown = face[23]
            leftLeft = face[130]
            leftRight = face[243]
            _,lenghtVer= distance_finder.findDistance(leftUp, leftDown,img, drawL=False)
            _,lenghtHor= distance_finder.findDistance(leftLeft, leftRight,img, drawL=False)
            # print(int(lenghtHor),int(lenghtVer))
            ratio = int((lenghtVer / lenghtHor) * 100)
            # print(ratio)
            self.ratioList.append(ratio)
            if len(self.ratioList) > 3:
                self.ratioList.pop(0)
            ratioAvg = int(sum(self.ratioList) / len(self.ratioList))
            # print(ratioAvg)

            if ratioAvg < 22 and self.counter == 0:
                self.eyeBlinkCounter += 1
                self.color = (0,200,0)
                self.counter = 1
            if self.counter != 0:
                self.counter += 1
                if self.counter > 10:
                    self.counter = 0
                    self.color = (255,0, 255)
        return self.eyeBlinkCounter

def main():
    blink_tracker = BlinkCounter()
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        cv2.rectangle(frame, (10,10), (345,45), (255,255,255), cv2.FILLED)
        cv2.putText(frame, 'Eye Blink Counter', (15,35), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 2)
        if ret:
            faces, img = mesh_tracker.findFaceMesh(frame, draw=False)
            if faces:
                face = faces[0]
                value = blink_tracker.blinkCounter(img,face, drawE=True)
                print(value)
                cv2.rectangle(frame, (10,50), (150,95), (255,255,255), cv2.FILLED)
                cv2.putText(frame, "Count : "+ str(value), (15,80), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,74,186), 2)
            cv2.imshow("Framing", img)
        else:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()