#!/bin/bash

nf=31 # number of wave files in the dataset

echo
echo "===== PREPARING DATA ====="
echo
python3 local/concat_texts.py $nf
python3 local/concat_segments.py $nf
python3 local/utt2spk.py $nf
python3 local/wav_file.py $nf
dos2unix data/full/text
echo
echo "===== prepare_data.sh is finished ====="
echo