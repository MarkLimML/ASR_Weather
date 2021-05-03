#!/usr/bin/env python3
import sys
import os

if(len(sys.argv) < 2):
    print("usage: local/analyze_decode_stats.py (mono|tri|delta|lda|sat)")
    print("e.g.: local/analyze_decode_stats.py tri")
    sys.exit();

filepath = "exp/"
if(sys.argv[1] == "mono")
    filepath += "mono/decode"
elif(sys.argv[1] == "tri")
    filepath += "tri/decode"
elif(sys.argv[1] == "delta")
    filepath += "tri2a/decode"
elif(sys.argv[1] == "lda")
    filepath += "tri3a/decode"
elif(sys.argv[1] == "sat")
	filepath += "tri4a/decode"
filepath += "log/"


for file in os.listdir(filepath):
    if file.startswith("acc"):
        with open(filepath+file) as f1:
            for line in f1:
                if("WARNING" in line and "Did not" in line):
					tmp = line.split(" ")
					accno+=1
					print(tmp[4])
		
print(sys.argv[0]+":", "checked segments.")