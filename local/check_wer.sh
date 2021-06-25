#!/usr/bin/env bash

ctrs=0
ctrd=0
ctri=0
ttl=0

fctr=$(wc -w $1 | awk '{print $1}')
fline=$(wc -l $1 | awk '{print $1}')
((len=$fctr-$fline))
while : ; do
	clear
	echo "Press 'esc' to exit"
	echo ""
	echo "	Q-Sub W-Del E-Ins (+)	"
	echo "	A-Sub S-Del D-Ins (-)	"
	echo " "
	echo "	Sub=$ctrs Del=$ctrd Ins=$ctri"
	echo "	Total=$ttl"
	echo "	Length=$len"
	echo ""
	python -c "print('	WER={0:0.2f}%'.format($ttl/$len*100))"
	read -n 1 k <&1
	if [[ $k = $'\e' ]] ; then
		printf "\nQuitting from the program\n"
		break
	else
		case $k in
		q* ) ((ctrs++))
		     ((ttl++));;
		w* ) ((ctrd++))
		     ((ttl++))
			 ((len++));;
		e* ) ((ctri++))
		     ((ttl++))
			 ((len--));;
		a* ) ((ctrs--))
		     ((ttl--));;
		s* ) ((ctrd--))
		     ((ttl--))
			 ((len--));;
		d* ) ((ctri--))
		     ((ttl--))
			 ((len++));;
		* )     echo "Try again.";;
		esac
	fi
done
