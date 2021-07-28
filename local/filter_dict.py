#! /usr/bin/env python3
import os

ref = dict()
phones = dict()

with open("data/words.txt", "w") as f1:
	words = []
	with open("data/full/text") as f:
		for line in f:
			line = line.strip()
			tmp = line.split(" ",1)
			line = tmp[1]
			line = line.split()
			for word in line:
				words.append(word.strip('.,!;()[]'))
		unique = []
		for word in words:
			if word not in unique:
				unique.append(word)
		unique.sort()
		for w in unique:
			f1.write(w+"\n")


with open("data/lexicon.txt") as f:
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

#print(ref)

lex = open("data/lexicon_tmp.txt", "w")

with open("data/words.txt") as f:
	lex.write("<UNK> SPN\n")
	for line in f:
		line = line.strip()
		if line in ref.keys():
			for pron in ref[line]:
				lex.write(line + " " + pron+"\n")
		else:
			print( "Word not in lexicon:" + line)

print("Notes:")
print("BASE has two variations")