#!/usr/bin/env python3

import sys
import codecs
import os
from collections import defaultdict
from datetime import timedelta

if(len(sys.argv) < 3):
	print("usage: "+sys.argv[0]+" <text-file> <segments-file>")
	print("e.g.: "+sys.argv[0]+" weather001.txt weather001_segments.txt")
	sys.exit();

def format_time(time):
	time_sec_frac = int(round(time - int(time), 3) * 1000)
	time_sec = timedelta(seconds=int(time))
	return str(time_sec) + ',' + str(time_sec_frac).zfill(3)
	
def print_st(srt_file, index, line):
	output = str(index + 1) + '\n'
	start_time = format_time(line['start_time'])
	end_time = format_time(line['end_time'])
	output += start_time + ' --> ' + end_time + '\n'
	st = line['subs']
	output += st + '\n\n'
	try:
		srt_file.write(output)
	except Exception:
		print('Could not process the following string:')
		print(st)
		exit(1)
	
fname = sys.argv[1].split('.')
srt = open(fname[0]+".srt","w")

with open(sys.argv[1]) as t:
	with open(sys.argv[2]) as s:
		i = 0
		for line in t:
			for time in s:
				tmp = time.strip().split()
				tmp2 = line.strip().split(" ",1)
				info = {'start_time':float(tmp[1]),'end_time':float(tmp[2]),"subs":tmp2[1]}
				print_st(srt,i,info)
				break
			i+=1