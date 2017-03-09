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
          self.rdf_name=ReadFunction.readFunctionDefault
          self.rdf=ReadFunction.readFunctionDict[self.rdf_name]
          self.dttf_name=DetectionFunction.detectionFunctionDefault
          self.dttf=DetectionFunction.detectionFunctionDict[self.dttf_name]
          self.rdf_filename=''
          self.running=False
          pass
     def Run(self):
          rdf_reader=self.rdf['reader'](self.rdf_filename)
          dttfer=self.dttf()
          while((not rdf_reader.end() ) and self.running):
               try:
                    img=rdf_reader.getImg()
               except:
                    print "Read img fail!"
                    continue
               found=dttfer.detect(img)
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
               ch = 0xFF & cv2.waitKey(self.rdf['waitTime'])
               if ch == 27:
                    break
          cv2.destroyAllWindows()
          pass

class controlPanel(wx.Panel):
     def __init__(self,parent):
          wx.Panel.__init__(self, parent)
          grid = wx.GridBagSizer(hgap=5, vgap=5)
          row=0
          self.model=flowModel()
          
          #du liu xie fa, ni zhi de yong you
          #readFunctionNotice
          self.readFunctionNotice= wx.StaticText(self, label='Your read Function: ')
          grid.Add(self.readFunctionNotice, pos=(row,0),span=(1,2))
          
          #readFunctionComo
          self.readFunctionList = [name for name in ReadFunction.readFunctionDict ]
          self.readFunctionComo = wx.ComboBox(self, choices=self.readFunctionList, style=wx.CB_DROPDOWN)
          grid.Add(self.readFunctionComo, pos=(row,3))
          self.Bind(wx.EVT_COMBOBOX, self.changeReadFunction, self.readFunctionComo)
          self.readFunctionComo.SetValue(ReadFunction.readFunctionDefault)

          #readFunctionOpen
          self.readFunctionOpen =wx.Button(self,label='Open')
          self.Bind(wx.EVT_BUTTON,self.clickOpen,self.readFunctionOpen)
          grid.Add(self.readFunctionOpen, pos=(row,4))

          #readFunctionFileName
          self.readFunctionFileName =wx.TextCtrl(self,size=(200,-1))
          grid.Add(self.readFunctionFileName, pos=(row,5),span=(1,2))
          
          row=row+1
          #detectionFunctionNotice
          self.detectionFunctionNotice= wx.StaticText(self, label='Your Detection Function: ')
          grid.Add(self.detectionFunctionNotice, pos=(row,0),span=(1,2))

          #detectionFunctionList
          self.detectionFunctionList = [name for name in DetectionFunction.detectionFunctionDict ]
          self.detectionFunctionComo = wx.ComboBox(self, choices=self.detectionFunctionList, style=wx.CB_DROPDOWN)
          grid.Add(self.detectionFunctionComo, pos=(row,3))
          self.Bind(wx.EVT_COMBOBOX, self.changeDetectionFunction, self.detectionFunctionComo)
          self.detectionFunctionComo.SetValue(DetectionFunction.detectionFunctionDefault)

          row=row+1
          #runButton
          self.runButton =wx.ToggleButton(self,label='Run')
          grid.Add(self.runButton, pos=(row,3))
          self.runButton.Bind(wx.EVT_TOGGLEBUTTON,self.buttonRun)

          #sizer
          topsizer=wx.BoxSizer(wx.HORIZONTAL)
          topsizer.Add(grid,0,wx.ALL, 5)
          self.SetSizerAndFit(topsizer)
     def changeReadFunction(self,event):
          print "ReadFunction ",event.GetString()
          self.model.rdf_name=event.GetString()
          self.model.rdf=ReadFunction.readFunctionDict[self.model.rdf_name]

     def changeDetectionFunction(self,event):
          print "DetectionFunction ",event.GetString()
          self.model.dttf_name=event.GetString()
          self.model.dttf=DetectionFunction.detectionFunctionDict[self.model.dttf_name]

     def clickOpen(self,event):
          print "clickOpen"
          if(self.model.rdf['filetype']=='dir'):
               dlg = wx.DirDialog(self, "Open file...",os.getcwd(),style=wx.DD_DEFAULT_STYLE)
               if dlg.ShowModal() == wx.ID_OK:
                    dirname=dlg.GetPath()
                    self.readFunctionFileName.SetValue(dirname)
                    print "open dir",dirname
               dlg.Destroy()
          elif(self.model.rdf['filetype']=='file'):
               dlg = wx.FileDialog(self, "Open file...",os.getcwd(), style = wx.OPEN)
               if dlg.ShowModal() == wx.ID_OK:
                    filename=dlg.GetPath()
                    self.readFunctionFileName.SetValue(filename)
                    print "open file",filename
               dlg.Destroy()
          elif(self.model.rdf['filetype']=='num'):
               self.readFunctionFileName.SetValue('0')
          
     def buttonRun(self,event):
          state=self.runButton.GetValue()
          self.model.rdf_filename=self.readFunctionFileName.GetValue()
          if(state):
               self.runButton.SetLabel('Stop')
               self.model.running=True
               self.model.Run()
          else:
               self.runButton.SetLabel('Run')
               self.model.running=False
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

     app = wx.App(False)
     mainframe = wx.Frame(None)
     mainPanel= controlPanel(mainframe)
     mainframe.SetSize((720,200))
     mainframe.Show()
     app.MainLoop()


