import cv2
import handTracker as ht

class fingerIdentifier():
    def __init__(self):
        self.tipIds = [4,8,12,16,20]

    def fingerOrientation(self,myhand):
    
        hand_type = myhand['hand_type']
        finger_landmarks = myhand['landmarksList']

        if myhand:
            finger_orientation = []
            if hand_type == "Right Hand":
                if finger_landmarks[self.tipIds[0]][1] > finger_landmarks[self.tipIds[0]-1][1]:
                    finger_orientation.append(1)
                else:
                    finger_orientation.append(0)
            else:
                if finger_landmarks[self.tipIds[0]][1] < finger_landmarks[self.tipIds[0]-1][1]:
                    finger_orientation.append(1)
                else:
                    finger_orientation.append(0)

            for id in range (1,5):
                if finger_landmarks[self.tipIds[id]][2] < finger_landmarks[self.tipIds[id]-2][2]:
                    finger_orientation.append(1)
                else:
                    finger_orientation.append(0)
        return (finger_orientation)

    def fingerIdentification(self,orientation):
        if ((orientation.count(1)) == 5):
            #print("All Fingers are showing")
            context = "All Fingers are showing"
            return context
        elif((orientation.count(0)) == 5):
            #print("All Finger Tapped")
            context = "All Finger Tapped"
            return context

        elif ((orientation[0] == 0) & (orientation[1] == 1) & (orientation[2] == 1) & (orientation[3] == 1) & (orientation[4] == 1)):
            #print("Thumb Finger Tapped")
            context = "Thumb Finger Tapped"
            return context
        elif ((orientation[0] == 1) & (orientation[1] == 0) & (orientation[2] == 0) & (orientation[3] == 0) & (orientation[4] == 0)):
            #print("Thumb Finger")
            context = "Thumb Finger"
            return context
        elif ((orientation[0] == 1) & (orientation[1] == 0) & (orientation[2] == 1) & (orientation[3] == 1) & (orientation[4] == 1)):
            #print("Index Finger Tapped")
            context = "Index Finger Tapped"
            return context
        elif ((orientation[0] == 0) & (orientation[1] == 1) & (orientation[2] == 0) & (orientation[3] == 0) & (orientation[4] == 0)):
            #print("Index Finger")
            context = "Index Finger"
            return context
        elif ((orientation[0] == 1) & (orientation[1] == 1) & (orientation[2] == 0) & (orientation[3] == 1) & (orientation[4] == 1)):
            #print("Middle Finger Tapped")
            context = "Middle Finger Tapped"
            return context
        elif ((orientation[0] == 0) & (orientation[1] == 0) & (orientation[2] == 1) & (orientation[3] == 0) & (orientation[4] == 0)):
            #print("Middle Finger")
            context = "Middle Finger"
            return context
        elif ((orientation[0] == 1) & (orientation[1] == 1) & (orientation[2] == 1) & (orientation[3] == 0) & (orientation[4] == 1)):
            #print("Ring Finger Tapped")
            context = "Ring Finger Tapped"
            return context
        elif ((orientation[0] == 0) & (orientation[1] == 0) & (orientation[2] == 0) & (orientation[3] == 1) & (orientation[4] == 0)):
            #print("Ring Finger")
            context = "Ring Finger"
            return context
        elif ((orientation[0] == 1) & (orientation[1] == 1) & (orientation[2] == 1) & (orientation[3] == 1) & (orientation[4] == 0)):
            #print("Little Finger Tapped")
            context = "Little Finger Tapped"
            return context
        elif ((orientation[0] == 0) & (orientation[1] == 0) & (orientation[2] == 0) & (orientation[3] == 0) & (orientation[4] == 1)):
            #print("Little Finger")
            context = "Little Finger"
            return context

def main():

    cam = cv2.VideoCapture(0)
    hand_tracker = ht.handTracker()
    finger_identifier = fingerIdentifier()
    while True:
        ret, frame = cam.read()
        if ret:
            hands = hand_tracker.findHands(frame)
            if hands:
                oneHand = hands[0]
                finger_1 = finger_identifier.fingerOrientation(oneHand)
                print(finger_1)
                context = finger_identifier.fingerIdentification(finger_1)
                print(context)

            cv2.imshow("Framing", frame)
        else:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()