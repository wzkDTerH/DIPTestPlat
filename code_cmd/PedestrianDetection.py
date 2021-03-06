#!/usr/bin/env python

import numpy as np
import cv2
import time
import DetectionFunction
import ReadFunction

help_message = '''
USAGE: PedestrianDetection.py <readfunction> <Detectionfunction> <image_names> ...

Press any key to continue, ESC to stop.
'''
def inside(r, q):
     rx, ry, rw, rh = r
     qx, qy, qw, qh = q
     return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh

def draw_detections(img, rects, thickness = 1):
     for x, y, w, h in rects:
          pad_w, pad_h = int(0.15*w), int(0.05*h)
          cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)

if __name__ == '__main__':
     import sys
     import os
     from glob import glob
     import itertools as it
     print help_message

     try:
          readFunction=ReadFunction.readFunctionDict[sys.argv[1]]
     except:
          print "No such read-function!"
          exit()
     try:
          detectionFunction=DetectionFunction.detectionFunctionDict[sys.argv[2]]
     except:
          print "No such detection-function!"
          exit()
     try:
          filename=sys.argv[3]
     except:
          print "No file name!"
          exit()
     rdf=readFunction(filename)
     dttf=detectionFunction()
     while(not rdf.end()):
          try:
               img=rdf.getImg()
          except:
               print "Read img fail!"
               continue
          found=dttf.detect(img)
          found_filtered = []
          for ri, r in enumerate(found):
               for qi, q in enumerate(found):
                    if ri != qi and inside(r, q):
                         break
                    else:
                         found_filtered.append(r)
          draw_detections(img, found)
          draw_detections(img, found_filtered, 3)
          print '%d (%d) found' % (len(found_filtered), len(found))
          cv2.imshow('img', img)
          ch = 0xFF & cv2.waitKey(rdf.waitTime())
          if ch == 27:
               break
     cv2.destroyAllWindows()
