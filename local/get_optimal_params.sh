#!/bin/bash
. ./cmd.sh || exit 1

if [ $# -ne 2 ]; then
  echo "Usage: local/get_optimal_params.sh <param-type> (tri|delta|lda|sat)"
  echo " Param Type:"
  echo "    1      # find optimal number of leaves"
  echo "    2      # find optimal number of gaussians"
fi

if [ $2 == "tri" ]; then # TRI SECTION
	if [ $1 -eq 1 ]; then
		echo
		echo "===== GETTING OPTIMAL LEAVES FOR TRIPHONE ====="
		echo
		for i in `seq 2000 100 5000`; do
		  steps/train_deltas.sh --boost-silence 1.25 --cmd "$train_cmd" $i 20000 data/train data/lang exp/mono_ali exp/tri1;
		  utils/mkgraph.sh data/lang exp/tri1 exp/tri1/graph;
		  steps/decode.sh --config conf/decode.config --nj 16 --cmd "$decode_cmd" exp/tri1/graph data/test exp/tri1/decode;
		  python3 local/get_average_wer.py tri1;
		done
	elif [ $1 -eq 2 ]; then
		echo
		echo "===== GETTING OPTIMAL GAUSSIANS FOR TRIPHONE ====="
		echo
		for i in `seq 10000 1000 50000`; do
		  steps/train_deltas.sh --boost-silence 1.25 --cmd "$train_cmd" 4200 $i data/train data/lang exp/mono_ali exp/tri1;
		  utils/mkgraph.sh data/lang exp/tri1 exp/tri1/graph;
		  steps/decode.sh --config conf/decode.config --nj 16 --cmd "$decode_cmd" exp/tri1/graph data/test exp/tri1/decode;
		  python3 local/get_average_wer.py tri1;
		done
	fi
elif [ $2 == "delta" ]; then # DELTA SECTION
	if [ $1 -eq 1 ]; then
		echo
		echo "===== GETTING OPTIMAL LEAVES FOR DELTA ====="
		echo
		for i in `seq 2000 100 5000`; do
		  steps/train_deltas.sh --cmd "$train_cmd" $i 20000 data/train data/lang exp/tri1_ali exp/tri2a;
		  utils/mkgraph.sh data/lang exp/tri2a exp/tri2a/graph;
		  steps/decode.sh --config conf/decode.config --nj 16 --cmd "$decode_cmd" exp/tri2a/graph data/test exp/tri2a/decode;
		  python3 local/get_average_wer.py tri2a;
		done
	elif [ $1 -eq 2 ]; then
		echo
		echo "===== GETTING OPTIMAL GAUSSIANS FOR DELTA ====="
		echo
		for i in `seq 10000 1000 50000`; do
		  steps/train_deltas.sh --cmd "$train_cmd" 2900 $i data/train data/lang exp/tri1_ali exp/tri2a;
		  utils/mkgraph.sh data/lang exp/tri2a exp/tri2a/graph;
		  steps/decode.sh --config conf/decode.config --nj 16 --cmd "$decode_cmd" exp/tri2a/graph data/test exp/tri2a/decode;
		  python3 local/get_average_wer.py tri2a;
		done
	fi
elif [ $2 == "lda" ]; then # LDA SECTION
	if [ $1 -eq 1 ]; then
		echo
		echo "===== GETTING OPTIMAL LEAVES FOR LDA ====="
		echo
		for i in `seq 2500 100 7500`; do
		  steps/train_lda_mllt.sh --cmd "$train_cmd" $i 47000 data/train data/lang exp/tri2a_ali exp/tri3a;
		  utils/mkgraph.sh data/lang exp/tri3a exp/tri3a/graph;
		  steps/decode.sh --config conf/decode.config --nj 16 --cmd "$decode_cmd" exp/tri3a/graph data/test exp/tri3a/decode;
		  python3 local/get_average_wer.py tri3a;
		done
	elif [ $1 -eq 2 ]; then
		echo
		echo "===== GETTING OPTIMAL GAUSSIANS FOR LDA ====="
		echo
		for i in `seq 15000 1000 75000`; do
		  steps/train_lda_mllt.sh --cmd "$train_cmd" 7300 $i data/train data/lang exp/tri2a_ali exp/tri3a;
		  utils/mkgraph.sh data/lang exp/tri3a exp/tri3a/graph;
		  steps/decode.sh --config conf/decode.config --nj 16 --cmd "$decode_cmd" exp/tri3a/graph data/test exp/tri3a/decode;
		  python3 local/get_average_wer.py tri3a;
		done
	fi
elif [ $2 == "sat" ]; then # SAT SECTION
	if [ $1 -eq 1 ]; then
		echo
		echo "===== GETTING OPTIMAL LEAVES FOR SAT ====="
		echo
		for i in `seq 2500 500 10000`; do
		  steps/train_sat.sh  --cmd "$train_cmd" $i 95000 data/train data/lang exp/tri3a_ali exp/tri4a;
		  utils/mkgraph.sh data/lang exp/tri4a exp/tri4a/graph;
		  steps/decode_fmllr.sh --nj 16 --cmd "$decode_cmd" exp/tri4a/graph data/test exp/tri4a/decode;
		  python3 local/get_average_wer.py tri4a;
		done
	elif [ $1 -eq 2 ]; then
		echo
		echo "===== GETTING OPTIMAL GAUSSIANS FOR SAT ====="
		echo
		for i in `seq 15000 5000 200000`; do
		  steps/train_sat.sh  --cmd "$train_cmd" 8800 $i data/train data/lang exp/tri3a_ali exp/tri4a;
		  utils/mkgraph.sh data/lang exp/tri4a exp/tri4a/graph;
		  steps/decode_fmllr.sh --nj 16 --cmd "$decode_cmd" exp/tri4a/graph data/test exp/tri4a/decode;
		  python3 local/get_average_wer.py tri4a;
		done
	fi

fi
