#!/usr/bin/env python3
import sys
import re
import glob

read_files = glob.glob("exp/tri3a_decode/confusions.*.txt")

with open("exp/tri3a_decode/confcombine.txt", "wb") as outfile:
    for f in read_files:
        with open(f, "rb") as infile:
            outfile.write(infile.read())

total = 0
regex = re.compile(r'(\s*\<eps\> .\s*)|(\s*((SIL .)|(. SIL)|(SIL SIL))\s*)')
with open("exp/tri3a_decode/confcombine.txt", "r") as infile:
	for line in infile:
		tmp = line.split(" ",1)
		tmp2 = tmp[1].strip().split(";")
		tmp3 = [i for i in tmp2 if not regex.match(i)]
		total += len(tmp3)
		#print(total, tmp3)

print(str(total)+" phones present.")