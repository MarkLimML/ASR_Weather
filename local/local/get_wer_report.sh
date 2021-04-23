#!/bin/bash

echo
echo "===== WER Report ====="
echo
python3 local/get_average_wer.py mono;
python3 local/get_average_wer.py tri1;
python3 local/get_average_wer.py tri2a;
python3 local/get_average_wer.py tri3a;
python3 local/get_average_wer.py tri4a;
echo
echo "===== get_wer_report.sh is finished ====="
echo