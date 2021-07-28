#!/usr/bin/env python3
import sys
import os

ref = dict()
phones = dict()

spn = ['AH','AHH','AHM','EH','EHM','UH','UMM',]

with open("data/lexicon.txt") as f:
	for line in f:
		line = line.strip()
		columns = line.split(" ", 1)
		if(len(columns)<2):
			print(columns[0]+" is missing a phoneme transcript")
			sys.exit();
		word = columns[0]
		pron = columns[1]
		try:
			ref[word].append(pron)
		except:
			ref[word] = list()
			ref[word].append(pron)

#print(ref)

lex = open("lexicon_tmp.txt", "wb")
lex.write(b"<UNK> SPN\n")
i = 0

with open("data/full/words.txt", "w") as f1:
	f1.write("<UNK> SPN\n")
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
			if(w not in spn):
				f1.write(w+"\n")

with open("data/full/words.txt") as f:
	with open("nonlex.txt","w") as n:
		for line in f:
			if(i == 0):
				i += 1
				continue
			line = line.strip()
			if line in ref.keys():
				for pron in ref[line]:
					lex.write(bytes(line, 'utf-8') + b" " + bytes(pron, 'utf-8')+b"\n")
			else:
				i += 1
				lex.write(bytes(line, 'utf-8') + b"\n")
				print("Word not in lexicon:" + line + "\n")
				n.write(line + "\n")
			
			
print(i-1, "words not included in lexicon")
			