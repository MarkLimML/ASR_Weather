#!/usr/bin/env bash
. ./path.sh || exit 1

phases=( 
    'Computing MFCC feats...'
    'Computing CMVN stats...'
    'Applying CMVN...'
	'Splicing features...'
	'Applying feature transforms...'
	'Generating lattice...'
	'Determing best path...'
	'Converting to text...'
	'Calculating WER...'
	'Extracting forced alignment and converting to ctm...'
) 

# begin configuration section.
num_threads=1
frame_shift=0.01
lmwt=20
wip=0.0
print_silence=false
mfcc_config=conf/mfcc.conf
#end configuration section.

decode_dir=$1

thread_string=
[ $num_threads -gt 1 ] && thread_string="-parallel --num-threads=$num_threads"

echo "$0 $@"

lang=exp/tri4a/graph/ # Note: may be graph directory not lang directory, but has the necessary stuff copied.
decode_dir=exp/tri4a/decode/
dir=exp_log

{
echo "${phase[0]}"
echo 5
	run.pl build/log/asr.1.mfcc.log \
	set -o pipefail '&&'\
	compute-mfcc-feats \
    --config=conf/mfcc.conf \
	--subtract-mean=true \
    --allow-upsample=true \
    scp:data/dev/wav.scp \
    ark,scp:data/dev/feats.ark,data/dev/feats.scp

echo "${phase[1]}"
echo 10
	run.pl build/log/asr.2.computecmvn.log \
	set -o pipefail '&&'\
	compute-cmvn-stats \
	scp:data/dev/feats.scp \
	ark,scp:data/dev/cmvn.ark,data/dev/cmvn.scp

echo "${phase[2]}"
echo 15
	run.pl build/log/asr.3.applycmvn.log \
	set -o pipefail '&&'\
	apply-cmvn \
    scp:data/dev/cmvn.scp \
    scp:data/dev/feats.scp ark:data/dev/cmvn-feats.ark

echo "${phase[3]}"	
echo 20
	run.pl build/log/asr.4.splice.log \
	set -o pipefail '&&'\
	splice-feats \
	scp:data/dev/feats.scp \
	ark:data/dev/splice-feats-tri4a.ark

echo "${phase[4]}"
echo 30
	run.pl build/log/asr.5.transforms.log \
	set -o pipefail '&&'\
	transform-feats \
	exp/tri4a/final.mat \
	ark:data/dev/splice-feats-tri4a.ark \
	ark:data/dev/splice-transform-feats-tri4a.ark

echo "${phase[5]}"
echo 40	
	run.pl --num-threads $num_threads build/log/asr.6.lats.log \
	gmm-latgen-faster$thread_string --max-active=7000 --beam=13.0 --lattice-beam=6.0 --acoustic-scale=0.083333 --allow-partial=true\
    --word-symbol-table=exp/tri4a/graph/words.txt \
    exp/tri4a/final.mdl \
    exp/tri4a/graph/HCLG.fst \
    ark:data/dev/splice-transform-feats-tri4a.ark \
	"ark:|gzip -c > data/dev/lat.gz"

echo "${phase[6]}"
echo 70
	run.pl build/log/asr.7.bestpath.log \
	set -o pipefail '&&'\
	lattice-best-path \
    --word-symbol-table=exp/tri4a/graph/words.txt \
    "ark:gunzip -c data/dev/lat.gz|" \
    ark,t:data/dev/one-best-tri4a.tra

echo "${phase[7]}"
echo 80
	run.pl build/log/asr.8.convert.log \
	utils/int2sym.pl -f 2- \
	exp/tri4a/graph/words.txt \
	data/dev/one-best-tri4a.tra \
	">&" data/dev/one-best-hypothesis-tri4a.txt
	
echo "Generated hypothesis. Process finished."

echo "${phase[8]}"
echo 90
	run.pl build/log/asr.9.align.log \
	cat data/dev/one-best-hypothesis-tri4a.txt \| \
	sed 's:\<UNK\>::g' \| \
	compute-wer --text --mode=present ark:data/dev/weather032.txt ark,p:- ">&" build/wer

echo "${phase[9]}"
echo 100
	run.pl build/log/asr.9.align.log \
	set -o pipefail '&&'\
	lattice-1best --lm-scale=$lmwt "ark:gunzip -c data/dev/lat.gz|" ark:- \| \
	lattice-align-words exp/tri4a/graph/phones/word_boundary.int exp/tri4a/final.mdl ark:- ark:- \| \
	nbest-to-ctm --frame-shift=$frame_shift --print-silence=$print_silence ark:- - \| \
	utils/int2sym.pl -f 5 exp/tri4a/graph/words.txt \| \
	cat '>' data/dev/hyp.ctm
} | whiptail --title 'Taglish ASR System' --gauge "Processing audio..." 6 60 0

whiptail --title 'Taglish ASR System' --msgbox "Finished. Check the data/dev directory." 7 60

local/ctm2srt.py data/dev/hyp.ctm data/dev/hyp.srt exp/tri4a/graph/words.txt