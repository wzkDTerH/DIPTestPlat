import os
readFunctionDict={}
filenamelist = os.listdir('.\\ReadFunction')
t=0
for filename in filenamelist:
     if(os.path.splitext(filename)[1]=='.py'):
          name=os.path.splitext(filename)[0]
          if(name!='__init__'):
               exec('import '+name)
               readFunctionDict[name]=eval(name+'.'+name)

readFunctionDefault="null"
