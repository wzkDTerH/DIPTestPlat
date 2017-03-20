import cv2
import os
import readFuncConfig

class captureReader:
     def __init__(self,name):
          self.cap = cv2.VideoCapture(int(name)) 
     def end(self):
         return not self.cap.isOpened()
     def getImg(self):
          ret, frame = self.cap.read()
          return frame

captureRead={'filetype':"num",'waitTime':20,'reader':captureReader}
