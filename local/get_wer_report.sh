#!/bin/bash

echo
echo "===== WER Report ====="
echo
dir="mono tri1 tri2a tri3a"
for x in $dir; do
	python3 local/get_average_wer.py $x;
done
echo
echo "===== get_wer_report.sh is finished ====="
echo