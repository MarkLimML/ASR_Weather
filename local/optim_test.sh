#!/bin/bash
. ./cmd.sh || exit 1

str=$(grep "With param:" op_tri.txt)
IFS=' '     # space is set as delimiter
read -ra LINE <<< $str
leaves=${LINE[2]}
echo $leaves
echo
echo "===== GETTING OPTIMAL GAUSSIANS FOR TRIPHONE ====="
echo
for i in {10000..2000..50000}; do
  steps/train_deltas.sh --boost-silence 1.25 --cmd "$train_cmd" $leaves $i data/train data/lang exp/mono_ali exp/tri1;
  python3 local/get_average_wer.py tri1;
done
