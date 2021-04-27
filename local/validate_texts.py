#!/usr/bin/env python3
import sys

if(len(sys.argv) < 3):
    print("usage: local/validate_texts.py <start-num> <end-num> <list-of-skipped-numbers>")
    print("e.g.: local/validate_texts.py 1 30")
    print("validates files numbered 1 to 30")
    sys.exit();

min = int(sys.argv[1])
max = int(sys.argv[2])+1
if(len(sys.argv) == 4):
    arr = sys.argv[3].split(',')
else:
    arr = []

for x in range(min,max):
    if(len(arr) != 0 and str(x) in arr):
        continue
    with open("text_weather/weather"+"{0:03}".format(x)+".txt","r") as f2:
        for i,line in enumerate(f2):
            tmp = line.split(" ",1)
            if("  " in line):
                print("DOUBLE SPACE:",line)
            elif(" \n" in line):
                print("EXTRA SPACE ON END:",line)
            elif(not tmp[1].isupper()):
                print("LOWERCASE:",line)
        
print(sys.argv[0]+":", "checked segments.")