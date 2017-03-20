import cv2
import numpy as np
class harris:
     def __init__(self):
          pass
     def detect(self,img):
          gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
          gray = np.float32(gray)
          dst = cv2.cornerHarris(gray,2,3,0.04)
          dst = cv2.dilate(dst,None)
          found=[]
          dstmax=dst.max()
          for xi,x in enumerate(dst):
               for yi,p in enumerate(x):
                    if(p>dstmax*0.05):
                         found.append([yi,xi,1,1])
          print "found:",len(found)
          return found
