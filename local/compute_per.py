#!/usr/bin/env python3
import sys
import os

if(len(sys.argv) < 2):
    print("usage: local/split_rename.py <conf-matrix-dir>")
    sys.exit();

with open(sys.argv[1]+"/confusions.txt","r") as f1:
    ins = 0
    dle = 0
    sub = 0
    cor = 0
    total = 0
    for i,line in enumerate(f1):
        tmp = line.split(" ")
        if(tmp[0] == tmp[1]):
            cor += int(tmp[2])
        elif(tmp[0] == "<eps>"):
            ins += int(tmp[2])
        elif(tmp[1] == "<eps>"):
            dle += int(tmp[2])
        elif(tmp[0] != tmp[1]):
            sub += int(tmp[2])
    total = cor+sub+dle
    per = ((ins+sub+dle)/total)
    fper = "{0:.2f}".format(per * 100)
        
print(sys.argv[0]+":", "PER computed.")
print("%PER "+fper+"% [ "+str(ins+sub+dle)+" / "+str(total)+ ", "+str(ins)+" ins, "+str(dle)+" del, "+str(sub)+" sub ]")
print(sys.argv[1])