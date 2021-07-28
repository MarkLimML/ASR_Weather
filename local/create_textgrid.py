#!/usr/bin/env python3

import sys
import os
from collections import defaultdict
import wave
import contextlib

if(len(sys.argv) < 4):
	print("usage: "+sys.argv[0]+" <text-file> <segments-file> <wave-file>")
	print("e.g.: "+sys.argv[0]+" weather001.txt weather001_segments.txt weather001.wav")
	sys.exit();
	
fname = sys.argv[1].split('.')
srt = open(fname[0]+".TextGrid","wb")

srt.write('File type = "ooTextFile"\nObject class = "TextGrid"\n\n')

maxtime = 0.000
with contextlib.closing(wave.open(sys.argv[3],'r')) as f:
	frames = f.getnframes()
	rate = f.getframerate()
	duration = frames / float(rate)
	formatted_float = "{:.3f}".format(duration)
	maxtime = formatted_float

srt.write('xmin = 0.0\nxmax = '+maxtime+'\ntiers? <exists>\nsize = 1\nitem []:\n')
srt.write('\titem[1]:\n')

utts = []
with open(sys.argv[1]) as t:
	with open(sys.argv[2]) as s:
		tmptime = "{:.3f}".format(0.000)
		i = 0
		for line in t:
			for time in s:
				info = {}
				tmp = time.strip().split()
				stime = "{:.3f}".format(float(tmp[1]))
				etime = "{:.3f}".format(float(tmp[2]))
				tmp2 = line.strip().split(" ",1)
				if (i == 0):
					while (stime != tmptime):
						info = {'start_time':0.00,'end_time':stime,"subs":""}
						tmptime = info['end_time']
						utts.append(info)
					info = {'start_time':stime,'end_time':etime,"subs":tmp2[1]}
					tmptime = info['end_time']
				else:
					while (stime != tmptime):
						info = {'start_time':tmptime,'end_time':stime,"subs":""}
						tmptime = info['end_time']
						utts.append(info)
					info = {'start_time':stime,'end_time':etime,"subs":tmp2[1]}
					tmptime = info['end_time']
				utts.append(info)
				break
			i+=1
		if (tmptime != maxtime):
			info = {'start_time':tmptime,'end_time':maxtime,"subs":""}
			utts.append(info)


srt.write('\t\tclass = "IntervalTier"\n\t\tname = "words"\n\t\txmin = 0.0\n\t\txmax = '+str(maxtime)+'\n\t\tintervals: size = '+str(len(utts))+'\n')

for i,utt in enumerate(utts):
	srt.write('\t\t\tintervals ['+str((i+1))+']:\n\t\t\t\txmin = '+str(utt['start_time'])+'\n\t\t\t\txmax = '+str(utt['end_time'])+'\n\t\t\t\ttext = "'+utt['subs']+'"\n')
		