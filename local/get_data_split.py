#! /usr/bin/env python3
import sys
import wave
import contextlib

if(len(sys.argv) < 1):
	print("usage: local/get_data_split.py")
	sys.exit();

maxtotal = 2.47
maxtrain = maxtotal * 0.8 * 3600
maxtest = maxtotal * 0.2 * 3600
total = 0
train = 0
test = 0
dur = 0

file = []
for line in sys.stdin:
    file.append(line)
    
file = file[::-1]
stmp = ""
i = 0
for line in file:
    tmp = line.split(" ")
    dur = float(tmp[3]) - float(tmp[2])
    if(train+dur < maxtrain):
        train += dur
    elif(test+dur < maxtest):
        if(stmp == ""):
            stmp = tmp[0]+" "+str(i)
        test += dur
    i+=1
    

print(stmp)
total = (train + test)/3600
train = train/3600
test = test/3600
print(total, train, test)
print(maxtotal, maxtrain/3600, maxtest/3600)
