#!/bin/bash
. ./path.sh || exit 1
. ./cmd.sh || exit 1
nj=4       # number of parallel jobs - 1 is perfect for such a small dataset
lm_order=4 # language model order (n-gram quantity) - 1 is enough for digits grammar
train_size=266 # number of utterances (train set)
test_size=66 # number of utterances (test set)
# Safety mechanism (possible running this script with modified arguments)
. utils/parse_options.sh || exit 1
[[ $# -ge 1 ]] && { echo "Wrong arguments!"; exit 1; }
# Removing previously created data (from last run.sh execution)
#rm -rf exp mfcc data/train/spk2utt data/train/cmvn.scp data/train/feats.scp data/train/split1 data/test/spk2utt data/test/cmvn.scp data/test/feats.scp data/test/split1 data/local/lang data/lang data/local/tmp data/local/dict/lexiconp.txt
rm -rf exp mfcc data/train/cmvn.scp data/train/feats.scp data/test/cmvn.scp data/test/feats.scp data/train/spk2utt data/test/spk2utt data/local/lang/lexiconp.txt data/local/tmp data/lang data/train data/test

echo
echo "===== TAKING SUBSET OF DATA ====="
echo
utils/subset_data_dir.sh --first data/full $train_size data/train
utils/subset_data_dir.sh --last data/full $test_size data/test

# Making spk2utt files
utils/utt2spk_to_spk2utt.pl data/train/utt2spk > data/train/spk2utt
utils/utt2spk_to_spk2utt.pl data/test/utt2spk > data/test/spk2utt

echo
echo "===== FEATURES EXTRACTION ====="
echo
# Making feats.scp files
mfccdir=mfcc
# Uncomment and modify arguments in scripts below if you have any problems with data sorting
# utils/validate_data_dir.sh data/train     # script for checking prepared data - here: for data/train directory
# utils/fix_data_dir.sh data/train          # tool for data proper sorting if needed - here: for data/train directory
steps/make_mfcc.sh --nj 16 --cmd "$train_cmd" data/train exp/make_mfcc/train $mfccdir
steps/make_mfcc.sh --nj 16 --cmd "$train_cmd" data/test exp/make_mfcc/test $mfccdir
# Making cmvn.scp files
steps/compute_cmvn_stats.sh data/train exp/make_mfcc/train $mfccdir
steps/compute_cmvn_stats.sh data/test exp/make_mfcc/test $mfccdir
echo
echo "===== PREPARING LANGUAGE DATA ====="
echo
# Needs to be prepared by hand (or using self written scripts):
#
# lexicon.txt           [<word> <phone 1> <phone 2> ...]
# nonsilence_phones.txt [<phone>]
# silence_phones.txt    [<phone>]
# optional_silence.txt  [<phone>]
# Preparing language data
utils/prepare_lang.sh data/local/lang '<UNK>' data/local/ data/lang

echo
echo "===== LANGUAGE MODEL CREATION ====="
echo "===== MAKING lm.arpa ====="
echo
loc=`which ngram-count`;
if [ -z $loc ]; then
        if uname -a | grep 64 >/dev/null; then
                sdir=$KALDI_ROOT/tools/srilm/bin/i686-m64
        else
                        sdir=$KALDI_ROOT/tools/srilm/bin/i686
        fi
        if [ -f $sdir/ngram-count ]; then
                        echo "Using SRILM language modelling tool from $sdir"
                        export PATH=$PATH:$sdir
        else
                        echo "SRILM toolkit is probably not installed.
                                Instructions: tools/install_srilm.sh"
                        exit 1
        fi
fi
local=data/local
mkdir $local/tmp
ngram-count -order $lm_order -write-vocab $local/tmp/vocab-full.txt -wbdiscount -text $local/corpus.txt -lm $local/tmp/lm.arpa
echo
echo "===== MAKING G.fst ====="
echo
lang=data/lang
arpa2fst --disambig-symbol=#0 --read-symbol-table=$lang/words.txt $local/tmp/lm.arpa $lang/G.fst

echo
echo "===== MONO TRAINING ====="
echo
steps/train_mono.sh --boost-silence 1.25 --nj $nj --cmd "$train_cmd" data/train data/lang exp/mono || exit 1
echo
echo "===== MONO DECODING ====="
echo
utils/mkgraph.sh --mono data/lang exp/mono exp/mono/graph || exit 1
steps/decode.sh --config conf/decode.config --nj 16 --cmd "$decode_cmd" exp/mono/graph data/test exp/mono/decode
echo
echo "===== MONO ALIGNMENT ====="
echo
steps/align_si.sh --boost-silence 1.25 --nj $nj --cmd "$train_cmd" data/train data/lang exp/mono exp/mono_ali || exit 1
echo
echo "===== TRI1 (first triphone pass) TRAINING ====="
echo
steps/train_deltas.sh --boost-silence 1.25 --cmd "$train_cmd" 4200 20000 data/train data/lang exp/mono_ali exp/tri1 || exit 1
echo
echo "===== TRI1 (first triphone pass) DECODING ====="
echo
utils/mkgraph.sh data/lang exp/tri1 exp/tri1/graph || exit 1
steps/decode.sh --config conf/decode.config --nj 16 --cmd "$decode_cmd" exp/tri1/graph data/test exp/tri1/decode
echo
echo "===== TRI1 ALIGNMENT ====="
echo
steps/align_si.sh --nj $nj --cmd "$train_cmd" data/train data/lang exp/tri1 exp/tri1_ali || exit 1;
echo
echo "===== Delta+delta-delta TRI2 TRAINING ====="
echo
steps/train_deltas.sh --cmd "$train_cmd" 2900 20000 data/train data/lang exp/tri1_ali exp/tri2a || exit 1;
echo
echo "===== Delta+delta-delta TRI2 DECODING ====="
echo
utils/mkgraph.sh data/lang exp/tri2a exp/tri2a/graph || exit 1
steps/decode.sh --config conf/decode.config --nj 16 --cmd "$decode_cmd" exp/tri2a/graph data/test exp/tri2a/decode
echo
echo "===== Delta+delta-delta TRI2 ALIGNMENT ====="
echo
steps/align_si.sh  --nj $nj --cmd "$train_cmd" --use-graphs true data/train data/lang exp/tri2a exp/tri2a_ali  || exit 1;
echo
echo "===== LDA-MLLT TRI3 TRAINING ====="
echo
steps/train_lda_mllt.sh --cmd "$train_cmd" 7300 47000 data/train data/lang exp/tri2a_ali exp/tri3a || exit 1;
echo
echo "===== LDA-MLLT TRI3 DECODING ====="
echo
utils/mkgraph.sh data/lang exp/tri3a exp/tri3a/graph || exit 1
steps/decode.sh --config conf/decode.config --nj 16 --cmd "$decode_cmd" exp/tri3a/graph data/test exp/tri3a/decode
echo
echo "===== LDA-MLLT TRI3 ALIGNMENT (WITH FMLLR)====="
echo
steps/align_fmllr.sh --nj $nj --cmd "$train_cmd" data/train data/lang exp/tri3a exp/tri3a_ali || exit 1;
echo
echo "===== SAT TRI4 TRAINING ====="
echo
steps/train_sat.sh  --cmd "$train_cmd" 8800 95000 data/train data/lang exp/tri3a_ali exp/tri4a || exit 1;
echo
echo "===== SAT TRI4 DECODING ====="
echo
utils/mkgraph.sh data/lang exp/tri4a exp/tri4a/graph || exit 1
steps/decode_fmllr.sh --config conf/decode --nj 16 --cmd "$decode_cmd" exp/tri4a/graph data/test exp/tri4a/decode
echo
echo "===== SAT TRI4 ALIGNMENT (WITH FMLLR)====="
echo
steps/align_fmllr.sh --cmd "$train_cmd" data/train data/lang exp/tri4a exp/tri4a_ali || exit 1;
echo
echo "===== BEST WER RESULTS ====="
echo
for x in exp/*/decode*; do
  [ -d $x ] && grep WER $x/wer_* | utils/best_wer.sh;
done
echo
echo "===== AVERAGE WER REPORT ====="
echo
. ./local/get_wer_report.sh || exit 1
echo
echo "===== run.sh script is finished ====="
echo