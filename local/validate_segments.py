#!/usr/bin/env python3
import sys

if(len(sys.argv) < 3):
    print("usage: local/validate_segments.py <start-num> <end-num> <list-of-skipped-numbers>")
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
if(len(sys.argv) == 4):
    arr = sys.argv[3].split(',')
else:
    arr = []

for x in range(min,max):
    tmpstart = 0.0
    tmpend = 0.0
    if(len(arr) != 0 and str(x) in arr):
            continue
    with open("text_weather/weather"+"{0:03}".format(x)+"_Segments.txt","r") as f2:
        for i,line in enumerate(f2):
            tmp = line.split(" ")
            start = float(tmp[1])
            end = float(tmp[2])
            if(start<tmpend or end<start):
                print("ERROR: incorrect segment",line.strip())
            elif(" \n" in line):
                print("ERROR: extra end space",line.strip())
            elif(len(tmp) != 3):
                print("ERROR: incorrect format",line.strip())
            else:
                tmpstart = start
                tmpend = end
        
print(sys.argv[0]+":", "checked segments.")