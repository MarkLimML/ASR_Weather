#! /usr/bin/env python3
import sys
import wave
import math

if(len(sys.argv) < 2):
	print("usage: cat <segments-file> | local/get_kfold_size.py <total-wav-hours>")
	sys.exit();

maxtotal = float(sys.argv[1])
maxset = maxtotal * 0.2 * 3600
total = 0
set = 0
test = 0
dur = 0

setutt = []
setids = []

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
x = 0
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
	if(int(tmp2[1]) == 1):
		sil = float(tmp[2])
	dur = tgap - float(tmp[2])
	
	tgap = float(tmp[2])
	if(set+dur <= maxset):
		set += dur
	elif(math.isclose(set+dur,maxset,rel_tol=9e-4)):
		set += dur
	else:
		setutt.append(tmp[0])
		setids.append(str(x))
		print(ID,set/3600,dur/3600)
		set = 0.00
		x = 0
	stmp = tmp[0]
	x+=1
print(ID,set/3600,tgap/3600)
	
for i,item in enumerate(setutt):
	total += (set/3600)
	print(setutt[i],setids[i])
	
print(stmp, x)
print(total)
print(maxtotal, maxset/3600)
