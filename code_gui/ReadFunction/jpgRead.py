import cv2
import os
class jpgRead:
     def __init__(self,name):
          self.filename=name
          self.filesnamenum=1;
          self.readflag=1
     def end(self):
         return self.readflag>self.filesnamenum
     def getImg(self):
          self.readflag=self.readflag+1
          return cv2.imread(self.filename)
     def waitTime(self):
          return -1
