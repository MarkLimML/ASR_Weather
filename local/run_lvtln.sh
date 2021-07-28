#!/bin/bash
. ./path.sh || exit 1
. ./cmd.sh || exit 1
nj=16     # number of parallel jobs

#curdate="$(date '+%m_%d_%Y')"
#tmp=$curdate
#for i in 2 3 4 5 6 7 8 9 10; do
#	if [ -f "exp_log/log_$curdate.txt" ]; then
#		curdate="$tmp"_"$i"
#	else
#		echo "logging to exp_log/log_$curdate"
#		break
#	fi
#done

echo "========================================="
echo "===== RUNNING LVTLN TRAINING SCRIPT ====="
echo "========================================="
echo
echo "===== LVTLN TRI2b TRAINING ====="
echo
steps/train_lvtln.sh  --cmd "$train_cmd" 600 12500 data/train data/lang exp/tri1 exp/tri2b || exit 1;
mkdir -p data/train_vtln
cp -r data/train/* data/train_vtln || exit 1
cp exp/tri2b/final.warp data/train_vtln/spk2warp || exit 1
echo
echo "===== LVTLN TRI2b DECODING ====="
echo
utils/mkgraph.sh data/lang exp/tri2b exp/tri2b/graph || exit 1
steps/decode_lvtln.sh --config conf/decode.config --nj 16 --cmd "$decode_cmd" exp/tri2b/graph data/test exp/tri2b/decode
mkdir -p data/test_vtln
cp -r data/test/* data/test_vtln || exit 1
cp exp/tri2b/decode/final.warp data/test_vtln/spk2warp || exit 1

mfccdir=mfcc_vtln
for x in train test; do
	steps/make_mfcc.sh --nj $nj --cmd "$train_cmd" data/"$x"_vtln exp/make_mfcc/"$x"_vtln $mfccdir
	steps/compute_cmvn_stats.sh data/"$x"_vtln exp/make_mfcc/"$x"_vtln $mfccdir
	utils/fix_data_dir.sh data/"$x"_vtln
done

echo
echo "===== LVTLN TRI2b ALIGNMENT ====="
echo
steps/align_si.sh --nj $nj --cmd "$train_cmd" data/train_vtln data/lang exp/tri2b exp/tri2b_ali || exit 1;
echo
echo "===== LDA-MLLT TRI3b(LVTLN + LDA-MLLT) TRAINING ====="
echo
steps/train_lda_mllt.sh  --cmd "$train_cmd" --splice-opts "--left-context=3 --right-context=3" 700 15000 data/train_vtln data/lang exp/tri2b_ali exp/tri3b || exit 1;
echo
echo "===== LDA-MLLT TRI3b(LVTLN + LDA-MLLT) DECODING ====="
echo
utils/mkgraph.sh data/lang exp/tri3b exp/tri3b/graph || exit 1
steps/decode.sh --config conf/decode.config --nj 16 --cmd "$decode_cmd" exp/tri3b/graph data/test_vtln exp/tri3b/decode
echo
echo "===== LDA-MLLT TRI3b(LVTLN + LDA-MLLT) ALIGNMENT ====="
echo
steps/align_si.sh --nj $nj --cmd "$train_cmd" data/train_vtln data/lang exp/tri3b exp/tri3b_ali || exit 1;
echo
echo "===== SAT TRI4a(LVTLN + SAT) TRAINING ====="
echo
steps/train_sat.sh --cmd "$train_cmd" 700 15000 data/train_vtln data/lang exp/tri3b_ali exp/tri4a || exit 1;
steps/train_sat_basis.sh --cmd "$train_cmd" 700 15000 data/train_vtln data/lang exp/tri3b_ali exp/tri4b || exit 1;
echo
echo "===== SAT TRI4a(LVTLN + SAT) DECODING ====="
echo
utils/mkgraph.sh data/lang exp/tri4a exp/tri4a/graph || exit 1
steps/decode_basis_fmllr.sh --config conf/decode.config --nj 16 --cmd "$decode_cmd" exp/tri4a/graph data/test_vtln exp/tri4a/decode
utils/mkgraph.sh data/lang exp/tri4b exp/tri4b/graph || exit 1
steps/decode_fmllr.sh --config conf/decode.config --nj 16 --cmd "$decode_cmd" exp/tri4b/graph data/test_vtln exp/tri4b/decode
