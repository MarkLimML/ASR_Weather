#!/bin/bash

if [[ $# -le 0 ]]; then
	echo "Usage:$0 <number-of-wave-files> <wave-files-to-skip>"
	echo "e.g.$0 70 45,62,65,69"
	exit 1
fi
nf=$1 # number of wave files in the dataset
sk=$2 # numbers to skip

echo
echo "===== PREPARING DATA ====="
echo
python3 local/fix_uttid.py $nf $sk
python3 local/concat_texts.py $nf $sk
python3 local/concat_segments.py $nf $sk
python3 local/utt2spk.py $nf $sk
python3 local/wav_file.py $nf $sk
dos2unix data/full/text
utils/utt2spk_to_spk2utt.pl data/full/utt2spk > data/full/spk2utt
echo
echo "===== prepare_data.sh is finished ====="
echo
