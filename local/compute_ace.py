#!/usr/bin/env python3
import sys
import os
import re
import subprocess
from math import log10

lmwt = 17
lm1 = dict() #uni-gram
lm2 = dict() #bi-gram
lm3 = dict() #tri-gram
lm4 = dict() #4-gram

#Load file as string
try:
	os.mkdir("exp/tri3a/decode/scoring_ace")
except Exception:
	print('Directory exists.')
subprocess.call(["cat exp/tri3a/decode/scoring/"+str(lmwt)+".tra | perl utils/int2sym.pl -f 2- exp/tri3a/graph/words.txt | sed s:\<UNK\>::g > exp/tri3a/decode/scoring_ace/"+str(lmwt)+".txt"], shell=True)
with open("data/local/tmp/lm.arpa", "r") as f:
	for i,line in enumerate(f):
		if(i < 8):
			continue
		elif(i > 1227 and i < 1231):
			continue
		elif(i > 6438):
			break
		line = line.strip()
		columns = line.split("\t")
		prob = columns[0] # log-prob of word
		word = columns[1] # word
		if(i < 1228):
			
			try:
				lm1[word].append(prob)
			except:
				lm1[word] = list()
				lm1[word].append(prob)
		elif(i < 6439):
			try:
				lm2[word].append(prob)
			except:
				lm2[word] = list()
				lm2[word].append(prob)

#print(lm1)
#print("===========================")
#print(lm2)
captions = []

subprocess.call(["src/bin/align-text ark:exp/tri3a/decode/scoring_ace/"+str(lmwt)+".txt ark:exp/tri3a/decode/scoring/test_filt.txt ark,t:alignment.txt"], shell=True)

with open("exp/tri3a/decode/scoring_ace/"+str(lmwt)+".txt", "r") as f:
	for line in f:
		line = line.strip()
		columns = line.split(" ",1)
		if(len(columns) < 2):
			captions.extend(" ")
		else:
			captions.extend(columns[1].split(" "))

reference = []

with open("exp/tri3a/decode/scoring/test_filt.txt", "r") as f:
	for line in f:
		line = line.strip()
		columns = line.split(" ",1)
		if(len(columns) < 2):
			reference.extend(" ")
		else:
			reference.extend(columns[1].split(" "))

#print(len(captions))
#print(len(reference))


#Calculate Word Entropy


#Calculate Impact Error


#Calculate ACE