import readFuncConfig
class nullReader:
     def __init__(self,name):
          pass
     def end(self):
         return True
     def getImg(self):
          return

nullRead={'filetype':"none",'waitTime':-1,'reader':nullReader}
