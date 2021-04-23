#!/bin/bash

nf=70 # number of wave files in the dataset
sk=45,62,65,69

echo
echo "===== PREPARING DATA ====="
echo
python3 local/concat_texts.py $nf $sk
python3 local/concat_segments.py $nf $sk
python3 local/utt2spk.py $nf $sk
python3 local/wav_file.py $nf $sk
dos2unix data/full/text
echo
echo "===== prepare_data.sh is finished ====="
echo