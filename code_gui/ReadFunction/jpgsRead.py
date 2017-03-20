import cv2
import os

class jpgsReader:
     def __init__(self,name):
          self.rootdir=name
          self.filesname=[]
          self.filesnamenum=0;
          for parent,dirnames,self.filenames in os.walk(self.rootdir):
               self.filesnamenum=len(self.filenames)
          for i in range(1,self.filesnamenum+1):
               self.filesname.append(self.rootdir+"\\"+str(i)+".jpg")
          self.readflag=1
     def end(self):
         return self.readflag>self.filesnamenum
     def getImg(self):
          self.readflag=self.readflag+1
          return cv2.imread(self.filesname[self.readflag-1])

jpgsRead={'filetype':"dir",'waitTime':20,'reader':jpgsReader}
