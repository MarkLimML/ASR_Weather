#!/usr/bin/env python
import sys
import os

ref = dict()
phones = dict()

with open("lexicon.txt") as f:
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

lex = open("lexicon_tmp.txt", "wb")
lex.write(b"<UNK> SPN\n")
i = 0

with open("words.txt") as f:
	for line in f:
		line = line.strip()
		if line in ref.keys():
			for pron in ref[line]:
				lex.write(bytes(line, 'utf-8') + b" " + bytes(pron, 'utf-8')+b"\n")
		else:
			i += 1
			lex.write(bytes(line, 'utf-8') + b"\n")
			print("Word not in lexicon:" + line + "\n")
			
			
print(i, "words not included in lexicon")
			