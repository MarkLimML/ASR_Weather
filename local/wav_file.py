import sys

if(len(sys.argv) < 2):
	print("usage: python local/wav_file.py <number-of-wavefiles>")
	sys.exit();

max = int(sys.argv[1])+1

with open("data/full/wav.scp","w") as y:
	for i in range(1,max):
		print("weather"+"{0:0=3d}".format(i),"waves_weather/weather"+"{0:0=3d}".format(i)+".wav",file=y);
		
print(sys.argv[0]+":", "created wav.scp.", sys.argv[1],"files present in dataset")