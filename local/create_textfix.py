#!/usr/bin/env python3

import sys
import os
from collections import defaultdict
import wave
import contextlib

if(len(sys.argv) < 2):
	print("usage: "+sys.argv[0]+" <TextGrid-file>")
	print("e.g.: "+sys.argv[0]+" weather001.TextGrid")
	sys.exit();
	
fname = sys.argv[1].split('.')
txt = open(fname[0]+".txt","w")
seg = open(fname[0]+"_Segments.txt","w")

ctr = 0
utts = []
with open(sys.argv[1]) as t:
	stime = 0.00
	etime = 0.00
	subs = ""
	for i,line in enumerate(t):
		if (i<14):
			continue
		if (ctr == 0):
			ctr += 1
			continue
		elif (ctr < 4):
			tmp = line.strip().split('=')
			if (ctr == 1):
				stime = tmp[1].strip('" ')
			elif (ctr == 2):
				etime = tmp[1].strip('" ')
			elif (ctr == 3):
				subs = tmp[1].strip('" ')
				if not subs:
					ctr = 0
					continue
				else:
					info = {'start_time':stime,'end_time':etime,"subs":subs}
					print(info)
					utts.append(info)
				ctr = -1
			ctr += 1

for i,utt in enumerate(utts):
	id = "{0:03}".format(i+1)
	txt.write(fname[0]+"_"+id+" "+utt['subs']+"\n")
	seg.write(fname[0]+"_"+id+" "+str(utt['start_time'])+" "+str(utt['end_time'])+"\n")
		