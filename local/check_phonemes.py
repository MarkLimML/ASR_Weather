#!/usr/bin/env python3
import sys

phones = ['p','b','t','d','k','g','tS','dZ','s','S','h','m','n','N','l','r','j','w','i','e','6','a','o','u','aj','6j','ej','oj','uj','aw','6w','iw','ow','f','v','z','T','I','3']
print("There are only "+str(len(phones))+" phones in the phoneme set")

def unique(list1):
    list_set = set(list1)
    unique_list = (list(list_set))
    return unique_list

with open('data/lexicon.txt','r') as f:
    for line in f:
        ps = []
        if("SPN" in line):
            continue
        tmp = line.split(' ',1)
        if(len(tmp) != 2 or len(tmp[1].strip()) == 0):
            tmp[0] = tmp[0].strip()
            print("The word "+tmp[0]+": does not have a phone.")
            continue
        else:
            tmp[1] = tmp[1].strip()
            ps = unique(tmp[1].split(' '))
        for p in ps:
            p = p.strip()
            if(p not in phones):
                print("In word "+tmp[0]+": "+p+" is not a phone.")
        
		
with open('data/nonsilence_phones.txt','r') as p:
	tmp = []
	for i,line in enumerate(p):
		line = line.strip()
		tmp.append(line)
	print(str(list(set(phones)-set(tmp)))+" not included in current phoneme set")

print(sys.argv[0]+":", "checked lexicon.")