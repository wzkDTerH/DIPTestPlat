import cv2
import os
class videoReader:
     def __init__(self,name):
          self.cap = cv2.VideoCapture(name) 
     def end(self):
         return not self.cap.isOpened()
     def getImg(self):
          ret, frame = self.cap.read()
          return frame

videoRead={'filetype':"file",'waitTime':20,'reader':videoReader}
