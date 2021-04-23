import os

ref = dict()
phones = dict()

with open("../lexicon.txt") as f:
	for line in f:
		line = line.strip()
		columns = line.split(" ", 1)
		word = columns[0]
		pron = columns[1]
		try:
			ref[word].append(pron)
		except:
			ref[word] = list()
			ref[word].append(pron)

print(ref)

lex = open("../local/lang/lexicon.txt", "w")

with open("words.txt") as f:
    for line in f:
        line = line.strip()
        if line in ref.keys():
            for pron in ref[line]:
                lex.write(line + " " + pron+"\n")
        else:
            print( "Word not in lexicon:" + line)