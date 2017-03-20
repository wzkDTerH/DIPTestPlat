import cv2
class hogsvm:
     def __init__(self):
          self.hog = cv2.HOGDescriptor()
          self.hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )
     def detect(self,img):
          found, w = self.hog.detectMultiScale(img, winStride=(8,8), padding=(32,32), scale=1.05)
          return found
