#!/usr/bin/env python
import sys
import os

if(len(sys.argv) < 2):
	print("usage: python local/get_average_wer.py <decode-type>")
	sys.exit();

type = sys.argv[1]
ave = 0.0
total = 0

for filename in os.listdir("exp/"+type+"/decode"):
	if filename.startswith("wer"):
		total += 1
		with open("exp/"+type+"/decode/"+filename) as fp:
			for i, line in enumerate(fp):
				if i == 1:
					line = line.split(" ")
					ave += float(line[1])

ave /= total
print(sys.argv[0]+":", "Average WER for "+type+" is", "{:.2f}".format(ave)+"%.")