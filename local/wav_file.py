#!/usr/bin/env python3
import sys

if(len(sys.argv) < 2):
	print("usage: python local/wav_file.py <number-of-wavefiles> <list-of-skipped-numbers>")
	sys.exit();

max = int(sys.argv[1])+1
if(len(sys.argv) == 3):
    arr = sys.argv[2].split(',')
else:
    arr = []

with open("data/full/wav.scp","w") as y:
	for i in range(1,max):
		if(len(arr) != 0 and str(i) in arr):
			continue
		print("weather"+"{0:0=3d}".format(i),"waves_weather/weather"+"{0:0=3d}".format(i)+".wav",file=y);
		
total = int(sys.argv[1])-len(arr)
print(sys.argv[0]+":", "created wav.scp", total,"files present in dataset")