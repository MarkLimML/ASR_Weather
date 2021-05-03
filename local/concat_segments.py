import sys

if(len(sys.argv) < 2):
	print("usage: python local/utt2spk.py <number-of-wavefiles> <list-of-skipped-numbers>")
	sys.exit();

def ins(w):
    wsplit = w.split()
    nfile = wsplit[0].split('_')
    wsplit.insert(1, nfile[0])
    final_string = ' '.join(wsplit)
    return final_string

max = int(sys.argv[1])+1
if(len(sys.argv) == 3):
    arr = sys.argv[2].split(',')
else:
    arr = []

with open("data/full/segments","w") as f:
    for x in range(1,max):
        if(len(arr) != 0 and str(x) in arr):
            continue
        with open("text_weather/weather"+"{0:03}".format(x)+"_Segments.txt","r") as f2:
            for line in f2:
                f.write(ins(line.strip())+"\n")
        
print(sys.argv[0]+":", "concatinating segments.")