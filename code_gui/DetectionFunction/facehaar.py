import cv2
import sys
class facehaar:
     def __init__(self):
          self.face_cascade = cv2.CascadeClassifier(sys.path[0]+"\\DetectionFunction\\haarcascades\\haarcascade_frontalface_alt.xml")
     def detect(self,img):
          gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
          gray = cv2.equalizeHist(gray)
          faces=self.face_cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
          print faces
          return faces
