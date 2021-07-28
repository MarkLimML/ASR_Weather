#!/usr/bin/env python3
import sys

with open('data/full/text','r') as f:
    filedata = f.read()
	
filedata = filedata.replace(' AGICULTURAL ', ' AGRICULTURAL ')
filedata = filedata.replace(' ALOS ', ' ALAS ')
filedata = filedata.replace(' ANGTRATED ', ' ISOLATED ')
filedata = filedata.replace(' AYE ', ' AY ')
filedata = filedata.replace(' BAHYAGYANG ', ' BAHAGYANG ')
filedata = filedata.replace(' DAHILI ', ' DAHIL ')
filedata = filedata.replace(' DELAYD ', ' DELAYED ')
filedata = filedata.replace(' DYIS ', ' DYES ')
filedata = filedata.replace(' HALAS', ' HALOS ')
filedata = filedata.replace(' HIHIGOPIN ', ' HIHIGUPIN ')
filedata = filedata.replace(' IBIGSABIHIN ', ' IBIG SABIHIN ')
filedata = filedata.replace(' ILOLO ', ' ILOILO ')
filedata = filedata.replace(' IPATULON ', ' IPATULOY ')
filedata = filedata.replace(' LAYR ', ' LAYER ')
filedata = filedata.replace(' MAGLALANFALL ', ' MAGLALANDFALL ')
filedata = filedata.replace('MALALAKASS', 'MALALAKAS')
filedata = filedata.replace('MALALAKA', 'MALALAKAS')
filedata = filedata.replace('MALALAKASS', 'MALALAKAS')
filedata = filedata.replace(' N0 ', ' NO ')
filedata = filedata.replace(' NAIDESSIMINANTE ', ' NAIDESSEMINATE ')
filedata = filedata.replace(' PAPUNTAN ', ' PAPUNTANG ')
filedata = filedata.replace(' PULU-PULUONG ', ' PULU-PULONG ')
filedata = filedata.replace(' TAGINIK', ' TAGINIT ')

with open('data/full/text','w') as f:
	f.write(filedata)

print(sys.argv[0]+":", "fixed text.")