#!/usr/bin/env python3
import sys
import os

if(len(sys.argv) < 3):
    print("usage: local/split_rename.py <start-num> <end-num> <list-of-skipped-numbers>")
    print("e.g.: local/split_rename.py 1 30")
    print("validates files numbered 1 to 30")
    sys.exit();

def writefile(ctmfile,ctmlist):
    with open("build/machine/split/"+ctmfile,"w") as out:
        for item in ctmlist:
            out.write(item)

min = int(sys.argv[1])
max = int(sys.argv[2])+1
if(len(sys.argv) == 4):
    arr = sys.argv[3].split(',')
else:
    arr = []

try:
    os.mkdir("build/machine/split")
except Exception:
    print('Directory exists.')
    
for x in range(min,max):
    if(len(arr) != 0 and str(x) in arr):
        continue
    with open("build/machine/segments","r") as f1:
        ctmlist = []
        for i,line in enumerate(f1):
            tmp = line.split(" ",1)
            id = "weather"+"{0:03}".format(x)
            tmp2 = tmp[1].split(" ",1)
            if(id in tmp[0]):
                ctmlist.append(tmp[0].replace("_00","_",1)+" "+tmp2[1])
        writefile("weather"+"{0:03}".format(x)+"_Segments.txt",ctmlist)
        
    with open("build/machine/text","r") as f2:
        ctmlist = []
        for i,line in enumerate(f2):
            tmp = line.split(" ",1)
            id = "weather"+"{0:03}".format(x)
            if(id in tmp[0]):
                ctmlist.append(tmp[0].replace("_00","_",1)+" "+tmp[1])
        writefile("weather"+"{0:03}".format(x)+".txt",ctmlist)
        
print(sys.argv[0]+":", "split segments and texts.")