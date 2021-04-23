import wave
import contextlib
with open("utt2dur", "w") as y:
	for i in range(1,32) :
		fname = '../wav/weather'+"{0:0=2d}".format(i)+'.wav';
		with contextlib.closing(wave.open(fname,'r')) as f:
			frames = f.getnframes()
			rate = f.getframerate()
			duration = frames / float(rate)
			formatted_float = "{:.2f}".format(duration)
			print('weather'+"{0:0=2d}".format(i),formatted_float,file=y)