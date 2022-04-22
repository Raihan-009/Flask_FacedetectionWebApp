
   
import math
import cv2
class Measurement():
    def __init__(self):
        pass
    
    def findDistance(self,p1 ,p2, img = None, drawL = True):
        x1,y1 = p1
        x2,y2 = p2
        cx,cy = (x1+x2)//2 , (y1+y2)//2
        distance = math.hypot(x2-x1, y2-y1)
        if img is not None:
            if drawL:
                cv2.circle(img,(x1,y1),5,(0,0,255),2)
                cv2.circle(img,(x2,y2),5,(0,0,255),2)
                cv2.line(img,p1,p2,(0,255,0),2)
            return img,distance
        else:
            return distance

def main():
    p1 = (0,0)
    p2 = (0,6)
    tracker = Measurement()
    distance = tracker.findDistance(p1, p2)
    return print(distance)

if __name__ == "__main__":
    main()