#! /usr/bin/env python3
import sys
import wave
import contextlib

if(len(sys.argv) < 3):
	print("usage: local/get_data_duration.py <start-num> <end-num> <list-of-skipped-numbers>")
	print("e.g.: local/get_data_duration.py 1 30")
	print("gets duration of wav files numbered 1 to 30")
	sys.exit();

min = int(sys.argv[1])
max = int(sys.argv[2])+1
if(len(sys.argv) == 4):
	arr = sys.argv[3].split(',')
else:
	arr = []

total = 0
train = 0
test = 0
with open("exp_log/data_stat.txt", "w") as y:
	for i in range(70,0,-1):
		if(len(arr) != 0 and str(i) in arr):
			continue
		fname = 'waves_weather/weather'+"{0:0=3d}".format(i)+'.wav';
		with contextlib.closing(wave.open(fname,'r')) as f:
			frames = f.getnframes()
			rate = f.getframerate()
			duration = frames / float(rate)
			formatted_float = "{:.2f}".format(duration)
			total += float(formatted_float)
			print('weather'+"{0:0=3d}".format(i),formatted_float,file=y)
	train = (total * 0.8) / 60 / 60
	test = (total * 0.2) / 60 / 60
	total = total / 60 / 60
	print("train: "+"{:.2f}".format(train)+" hrs\ntest: "+"{:.2f}".format(test)+" hrs\ntotal: "+"{:.2f}".format(total)+" hrs")
	print("train: "+"{:.2f}".format(train)+" hrs\ntest: "+"{:.2f}".format(test)+" hrs\ntotal: "+"{:.2f}".format(total)+" hrs",file=y)
    
ttype=["train:","test:","total:"]
with open("exp_log/data_stat.txt", "r") as z:
    parttrain = 0
    parttest = 0
    stmp = ""
    for line in z:
        tmp = line.split(" ",1)
        if(tmp[0] in ttype):
            continue
        tmpval = float(tmp[1])
        if(parttrain+tmpval <= (train*60)*60):
            parttrain += tmpval
        elif(parttest <= (test*60)*60):
            if(stmp == ""):
                stmp = tmp[0]
            parttest += tmpval
    parttrain = parttrain / 60 / 60
    parttest = parttest / 60 / 60
    print("train: "+"{:.2f}".format(parttrain)+" hrs\ntest: "+"{:.2f}".format(parttest)+" hrs\ntotal: "+"{:.2f}".format(parttrain+parttest)+" hrs")
    print(stmp)
        