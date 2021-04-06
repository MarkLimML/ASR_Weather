import sys

if(len(sys.argv) < 2):
	print("usage: python local/utt2spk.py <number-of-wavefiles>")
	sys.exit();

max = int(sys.argv[1])+1

with open("data/full/text","wb") as f:
	for x in range(1,max):
		with open("text_weather/weather"+"{0:03}".format(x)+".txt","rb") as f2:
			f.write(f2.read())
		f.write(b"\n")
			
print(sys.argv[0]+":", "concatinating texts.")