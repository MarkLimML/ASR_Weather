#! /usr/bin/env python3
import sys
import wave
import contextlib

if(len(sys.argv) < 2):
	print("usage: cat <segments-file> | local/get_data_split.py <total-wav-hours>")
	sys.exit();

maxtotal = float(sys.argv[1])
maxtrain = maxtotal * 0.8 * 3600
maxtest = maxtotal * 0.2 * 3600
total = 0
train = 0
test = 0
dur = 0
chktrain = True
chklast = False

file = []
for line in sys.stdin:
	file.append(line)
	
fdur = []
with open("exp_log/data_stat.txt") as d:
	for line in d:
		tmp = line.strip().split()
		fdur.append(tmp[1])

file = file[::-1]
fdur = fdur[::-1]
stmp = ""
i = 0
sil = 0.00
tgap = 0.00
ID = 0
for line in file:
	tmp = line.split(" ")
	tmp2 = tmp[0].split("_")
	tmpID = ID
	ID = int(tmp2[0][-3:])
	if(tmpID != ID):
		tgap = 0.00
		sil = 0.00
	if(tgap == 0.00):
		tgap = float(fdur[ID-1])
	if(int(tmp2[1]) == 1 and not chklast):
		sil = float(tmp[2])
		chklast = True
	dur = tgap - float(tmp[2])
	
	tgap = float(tmp[2])
	if(train+dur <= maxtrain and chktrain):
		train += dur
	elif(test+dur <= maxtest):
		if(chktrain):
			chktrain = False
		if(stmp == ""):
			stmp = tmp[0]+" "+str(i)
		test += dur
	i+=1
	print(ID,train,tgap)
	
	

print(stmp)
total = (train + test)/3600
train = train/3600
test = test/3600
print(total, train, test)
print(maxtotal, maxtrain/3600, maxtest/3600)
