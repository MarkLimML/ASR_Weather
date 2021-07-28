#! /usr/bin/env python3
import sys

if(len(sys.argv) < 2):
	print("usage: python local/utt2spk.py <number-of-wavefiles> <list-of-skipped-numbers>")
	sys.exit();
	
max = int(sys.argv[1])+1
if(len(sys.argv) == 3):
	arr = sys.argv[2].split(',')
else:
	arr = []

for x in range(1,max) :
	if(len(arr) != 0 and str(x) in arr):
			continue
	seg = open("text_weather/weather"+"{0:03}".format(x)+"_Segments.txt","r")
	txt = open("text_weather/weather"+"{0:03}".format(x)+".txt","r")
	slines = seg.readlines()
	tlines = txt.readlines()
	if("_000" in tlines[0]):
		for i,line in enumerate(tlines):
			old = "_"+"{0:03}".format(i)
			new = "_"+"{0:03}".format(i+1)
			slines[i] = slines[i].replace(old,new)
			tlines[i] = tlines[i].replace(old,new)
		seg = open("text_weather/weather"+"{0:03}".format(x)+"_Segments.txt","w")
		txt = open("text_weather/weather"+"{0:03}".format(x)+".txt","w")
		seg.writelines(slines)
		txt.writelines(tlines)
		print("weather"+str(x)+" and segments fixed")
	
print(sys.argv[0]+":", "checked txt files.")