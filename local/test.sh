#!/bin/bash

curdate="$(date '+%m_%d_%Y')"
tmp=$curdate
for i in 2 3 4 5 6 7 8; do
	if [ -f "exp_log/log_$curdate.txt" ]; then
		echo "log_$curdate exists"
		curdate="$tmp"_"$i"
		echo $curdate
	else
		echo "creating log_$curdate"
		touch exp_log/log_$curdate.txt
		break
	fi
done
