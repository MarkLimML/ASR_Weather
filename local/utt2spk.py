import sys

if(len(sys.argv) < 3):
	print("usage: python local/utt2spk.py <number-of-wavefiles> <list-of-skipped-numbers>")
	sys.exit();

max = int(sys.argv[1])+1
if(len(sys.argv) == 3):
    arr = sys.argv[2].split(',')
else:
    arr = []

total = 0

with open("data/full/utt2spk","w") as y:
	for i in range(1,max):
		if(len(arr) != 0 and str(i) in arr):
			continue
		with open("text_weather/weather"+"{0:03}".format(i)+".txt","r") as f:
			for num,file in enumerate(f):
				total+=1
				seg = "{0:03}".format(num+1)
				fno = "{0:03}".format(i)
				l = "weather"+fno+"_"+seg
				print(l,l,file=y)
                
print(sys.argv[0]+":","Created", total, "utterances")