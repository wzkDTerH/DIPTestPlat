#!/usr/bin/env python

import numpy as np
import cv2
import time
import DetectionFunction
import ReadFunction
import wx
import threading

class flowModel:
     def __init__(self):
          pass

class controlPanel(wx.Panel):
     def __init__(self,parent,model):
          wx.Panel.__init__(self, parent)
          grid = wx.GridBagSizer(hgap=5, vgap=5)

          strpre=[["read","Read"],["detection","Detection"]]
          row=0
          for pre in strpre:
               _Model=pre[1]+'Function'
               _Dict=pre[0]+'FunctionDict'
               _Default=pre[0]+'FunctionDefault'
               _Notice='self.'+pre[0]+'FunctionNotice'
               _label='\'Your '+pre[1]+' Function: \''
               _List='self.'+pre[0]+'FunctionList'
               _Combo='self.'+pre[0]+'FunctionComo'
               _Open='self.'+pre[0]+'FunctionOpen'
               _FileName='self.'+pre[0]+'FunctionFileName'
               #du liu xie fa, ni zhi de yong you
               exec(_Notice+'= wx.StaticText(self, label='+_label+')')
               grid.Add(eval(_Notice), pos=(row,0),span=(1,2))

               exec(_List+'= [name for name in '+_Model+'.'+_Dict+']')
               exec(_Combo+' = wx.ComboBox(self, choices='+_List+', style=wx.CB_DROPDOWN)')
               exec(_Combo+'.SetValue('+_Model+'.'+_Default+')')
               grid.Add(eval(_Combo), pos=(row,3))

               exec(_Open+'=wx.Button(self,label=\'Open\',)')
               grid.Add(eval(_Open), pos=(row,4))

               exec(_FileName+'=wx.TextCtrl(self,size=(200,-1))')
               grid.Add(eval(_FileName), pos=(row,5),span=(1,2))

               row=row+1

          topsizer=wx.BoxSizer(wx.HORIZONTAL)
          topsizer.Add(grid,0,wx.ALL, 5)
          self.SetSizerAndFit(topsizer)
#     def onChooseReadFunction(self,event):

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

     model=flowModel()
     app = wx.App(False)
     mainframe = wx.Frame(None)
     mainPanel= controlPanel(mainframe,model)
     mainframe.SetSize((720,200))
     mainframe.Show()
     app.MainLoop()

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
