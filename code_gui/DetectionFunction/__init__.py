import os
detectionFunctionDict={}
filenamelist = os.listdir('.\\DetectionFunction')
t=0
for filename in filenamelist:
     if(os.path.splitext(filename)[1]=='.py'):
          name=os.path.splitext(filename)[0]
          if(name!='__init__'):
               exec('import '+name)
               detectionFunctionDict[name]=eval(name+'.'+name)

detectionFunctionDefault="none"
