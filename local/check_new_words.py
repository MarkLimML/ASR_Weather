#!/usr/bin/env python3
import sys
import os

ref = dict()
phones = dict()

with open("data/local/lang/lexicon.txt") as f:
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

lex = open("lexicon_tmp.txt", "wb")
lex.write(b"<UNK> SPN\n")
i = 0

with open("data/test/words.txt") as f:
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
			