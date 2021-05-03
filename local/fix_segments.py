#!/usr/bin/env python3
import sys

if(len(sys.argv) < 4):
    print("usage: local/fix_odd_texts.py <start-num> <end-num> <list-of-skipped-numbers>")
    print("e.g.: local/fix_odd_texts.py 1 30 20,30")
    print("fixes segments numbered 1 to 30 and skips 20 and 30")
    print("Note: does not fix incorrect time stamps")
    sys.exit();

min = int(sys.argv[1])
max = int(sys.argv[2])+1
if(len(sys.argv) == 4):
    arr = sys.argv[3].split(',')
else:
    arr = []

totalfix = 0
for x in range(min,max):
    if(len(arr) != 0 and str(x) in arr):
        continue
    with open("text_weather/weather"+"{0:03}".format(x)+"_Segments.txt","r") as f2:
        txt = f2.readlines()
    with open("text_weather/weather"+"{0:03}".format(x)+"_Segments.txt","w") as f3:
        i = 0
        for line in txt:
            tmp = line.split(" ",1)
            if("  " in line):
                txt[i] = txt[i].replace("  "," ")
                totalfix+=1
            elif(" \n" in line):
                txt[i] = txt[i].replace(" \n","\n")
                totalfix+=1
            f3.writelines(txt[i])
            i+=1

print(sys.argv[0]+":", "checked segments.")