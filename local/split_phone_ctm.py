#!/usr/bin/env python3
import sys

if(len(sys.argv) < 1):
    print("usage: local/split_phone_ctm.py")
    sys.exit();

def writectm(ctmfile,ctmlist):
    with open("build/output/"+ctmfile,"w") as out:
        for item in ctmlist:
            out.write(item)

with open("data/dev/wav.scp", "r") as f1:
    for line in f1:
        l = line.split(" ",1)
        ctmlist = []
        with open("build/output/phone.ctm","r") as f2:
            for i,line in enumerate(f2):
                tmp = line.split(" ",1)
                if(l[0] == tmp[0]):
                    ctmlist.append(line)
        writectm(l[0]+"_phone.ctm",ctmlist)
        
print(sys.argv[0]+":", "separated ctms.")