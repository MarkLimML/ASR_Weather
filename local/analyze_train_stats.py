#!/usr/bin/env python3
import sys
import os

if(len(sys.argv) < 2):
    print("usage: local/analyze_train_stats.py (mono|tri|delta|lda|sat)")
    print("e.g.: local/analyze_train_stats.py tri")
    sys.exit();

filepath = "exp/"
if(sys.argv[1] == "mono"):
    filepath += "mono/"
elif(sys.argv[1] == "tri"):
    filepath += "tri/"
elif(sys.argv[1] == "delta"):
    filepath += "tri2a/"
elif(sys.argv[1] == "lda"):
    filepath += "tri3a/"
elif(sys.argv[1] == "sat"):
    filepath += "tri4a/"
filepath += "log/"

accno = 0
alignno = 0
acclist = []
alignlist = []
for file in os.listdir(filepath):
    if file.startswith("acc"):
        with open(filepath+file) as f1:
            for line in f1:
                if("WARNING" in line and "No alignment" in line):
                    tmp = line.split(" ")
                    if(tmp[6] not in acclist):
                        accno+=1
                        acclist.append(tmp[6])
    elif file.startswith("align"):
        with open(filepath+file) as f1:
            for line in f1:
                if("WARNING" in line and "Did not" in line):
                    tmp = line.split(" ")
                    if(tmp[7][:-1]+"\n" not in alignlist):
                        alignno+=1
                        alignlist.append(tmp[7][:-1]+"\n")

with open("exp_log/acc_"+sys.argv[1]+"_stats.txt","w") as w1:
    for item in acclist:
        w1.write(item)
with open("exp_log/align_"+sys.argv[1]+"_stats.txt","w") as w2:
    for item in alignlist:
        w2.write(item)
print(accno, alignno)
        
dupno = 0
with open("exp_log/acc_"+sys.argv[1]+"_stats.txt","r") as w1:
    with open("exp_log/align_"+sys.argv[1]+"_stats.txt","r") as w2:
        for i1 in w2:
            for i2 in w1:
                if(i1 == i2):
                    dupno+=1
                    break
print(dupno)

print(sys.argv[0]+":", "checked segments.")