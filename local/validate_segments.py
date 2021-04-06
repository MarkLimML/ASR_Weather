#!/usr/bin/env python
import sys

if(len(sys.argv) < 3):
    print("usage: local/validate_segments.py <start-num> <end-num>")
    print("e.g.: local/validate_segments.py 1 30")
    print("validates files numbered 1 to 30")
    sys.exit();

def ins(w):
    wsplit = w.split()
    nfile = wsplit[0].split('_')
    wsplit.insert(1, nfile[0])
    final_string = ' '.join(wsplit)
    return final_string

min = int(sys.argv[1])
max = int(sys.argv[2])+1

for x in range(min,max):
    tmpstart = 0.0
    tmpend = 0.0
    with open("text_weather/weather"+"{0:03}".format(x)+"_Segments.txt","r") as f2:
        for i,line in enumerate(f2):
            tmp = line.split(" ")
            start = float(tmp[1])
            end = float(tmp[2])
            if(start<tmpend or end<start):
                print("ERROR: incorrect segment",line)
            else:
                tmpstart = start
                tmpend = end
        
print(sys.argv[0]+":", "checked segments.")