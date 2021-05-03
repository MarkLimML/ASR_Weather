#!/bin/bash
phases=( 
    'Computing MFCC feats...'
    'Computing CMVN stats...'
    'Applying CMVN...'
	'Splicing features...'
	'Applying feature transforms...'
	'Generating lattice...'
	'Determing best path...'
	'Converting to text...'
	'Calculating WER...'
	'Extracting forced alignment and converting to ctm...'
) 

x=0
for((i = 0 ; i <= 100 ; i+=5)); do
	sleep 0.1
	echo "XXX${phases[$x]}XXX"
	x+=1
done | whiptail --gauge "${phases[$x]}" 6 60 0
