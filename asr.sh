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
max_active=14000
beam=13.0
lattice_beam=6.0

stage=1
freq=16000
num_threads=1
frame_shift=0.01
lmwt=17
acwt=0.083333
silence_weight=0.01
print_silence=false
max_fmllr_jobs=25
fmllr_update_type=full
mfcc_config=conf/mfcc.conf
#end configuration section.

score_result=$1 #compute wer of hypothesized transcript (0=false,1=true)
score_reftxt=$2 #if score_result=1, provide reference text

thread_string=
[ $num_threads -gt 1 ] && thread_string="-parallel --num-threads=$num_threads"

echo "$0 $@"

alignment_model=exp/tri3a/final.alimdl
adapt_model=exp/tri3a/final.mdl
final_model=exp/tri3a/final.mdl
lang=exp/tri3a/graph # Note: may be graph directory not lang directory, but has the necessary stuff copied.
decode_dir=exp/tri3a/decode/
dir=exp_log
data_dir=data/dev
output_dir=build/output

silphonelist=`cat $lang/phones/silence.csl` || exit 1;
splice_opts=`cat exp/tri3a/splice_opts 2>/dev/null` # frame-splicing options.
cmvn_opts=`cat exp/tri3a/cmvn_opts 2>/dev/null`

sifeats="ark,s,cs:apply-cmvn $cmvn_opts scp:$data_dir/cmvn.scp scp:$data_dir/feats.scp ark:- | splice-feats $splice_opts ark:- ark:- | transform-feats exp/tri3a/final.mat ark:- ark:- |"
pass1feats="$sifeats transform-feats ark:$data_dir/pre_trans.1 ark:- ark:- |";
feats="$sifeats transform-feats  ark:$data_dir/trans.1 ark:- ark:- |"

rm -r build
mkdir build
mkdir -p $output_dir

#if [ $stage -eq 0 ]; then
#if ! grep -q "cat" "$data_dir/wav.scp"; then
#mv $data_dir/wav.scp $data_dir/wav.scp.tmp
#cat $data_dir/wav.scp.tmp | python -c "import sys
#for line in sys.stdin.readlines():
#  splits = line.strip().split()
#  if splits[-1] == '|':
#    out_line = line.strip() + ' /usr/bin/sox -t wav - -c 1 -b 16 -t wav - rate $freq |'
#  else:
#    out_line = '{0} cat {1} | /usr/bin/sox -t wav - -c 1 -b 16 -t wav - rate $freq |'.format(splits[0], ' '.join(splits[1:]))
#  print (out_line)" > $data_dir/wav.scp
#rm $data_dir/wav.scp.tmp
#fi
#stage=1
#fi

if [ $stage -eq 1 ]; then
{
	echo "${phase[0]}"
	echo 5
		run.pl build/log/asr.1.mfcc.log \
		set -o pipefail '&&'\
		compute-mfcc-feats \
		--config=conf/mfcc.conf \
		--allow-downsample=true \
		scp:$data_dir/wav.scp \
		ark,scp:$data_dir/feats.ark,$data_dir/feats.scp

	echo "${phase[1]}"
	echo 10
		run.pl build/log/asr.2.computecmvn.log \
		set -o pipefail '&&'\
		compute-cmvn-stats \
		scp:$data_dir/feats.scp \
		ark,scp:$data_dir/cmvn.ark,$data_dir/cmvn.scp

	echo "${phase[5]}"
	echo 20	
		#Speaker Independent Lattice Generation
		run.pl --num-threads $num_threads build/log/asr.6.lats.log \
		gmm-latgen-faster$thread_string --max-active=2000 --beam=10 --lattice-beam=$lattice_beam --acoustic-scale=$acwt --allow-partial=true\
		--word-symbol-table=$lang/words.txt \
		exp/tri3a/final.alimdl \
		$lang/HCLG.fst \
		"$sifeats" \
		"ark:|gzip -c > $data_dir/lat.gz"
	
		#First-pass fMLLR transform
		run.pl --max-jobs-run $max_fmllr_jobs build/log/asr.6.fmllr_pass1.log \
		gunzip -c $data_dir/lat.gz \| \
		lattice-to-post --acoustic-scale=$acwt ark:- ark:- \| \
		weight-silence-post $silence_weight $silphonelist $alignment_model ark:- ark:- \| \
		gmm-post-to-gpost $alignment_model "$sifeats" ark:- ark:- \| \
		gmm-est-fmllr-gpost --fmllr-update-type=$fmllr_update_type \
		$adapt_model "$sifeats" ark,s,cs:- \
		ark:$data_dir/pre_trans.1
		
		#Main Lattice Generation
		run.pl --num-threads $num_threads build/log/asr.6.lats2.log \
		gmm-latgen-faster$thread_string --max-active=$max_active --beam=$beam --lattice-beam=$lattice_beam --acoustic-scale=$acwt --allow-partial=true\
		--word-symbol-table=$lang/words.txt \
		exp/tri3a/final.mdl \
		$lang/HCLG.fst \
		"$pass1feats" \
		"ark:|gzip -c > $data_dir/lat.tmp.gz"
		
		#Second-pass fMLLR transform
		run.pl --max-jobs-run $max_fmllr_jobs build/log/asr.6.fmllr_pass2.log \
		lattice-determinize-pruned$thread_string --acoustic-scale=$acwt --beam=4.0 \
		"ark:gunzip -c $data_dir/lat.tmp.gz|" ark:- \| \
		lattice-to-post --acoustic-scale=$acwt ark:- ark:- \| \
		weight-silence-post $silence_weight $silphonelist $adapt_model ark:- ark:- \| \
		gmm-est-fmllr --fmllr-update-type=$fmllr_update_type \
		$adapt_model "$pass1feats" \
		ark,s,cs:- ark:$data_dir/trans_tmp.1 '&&' \
		compose-transforms --b-is-affine=true ark:$data_dir/trans_tmp.1 ark:$data_dir/pre_trans.1 \
		ark:$data_dir/trans.1
		
		#Lattice-rescoring
		run.pl --num-threads $num_threads build/log/asr.6.acoustic_rescore.log \
		gmm-rescore-lattice $final_model "ark:gunzip -c $data_dir/lat.tmp.gz|" "$feats" ark:- \| \
		lattice-determinize-pruned$thread_string --acoustic-scale=$acwt --beam=$lattice_beam ark:- \
		"ark:|gzip -c > $data_dir/lat.gz" '&&' rm $data_dir/lat.tmp.gz
		
	echo "${phase[6]}"
	echo 70
		run.pl build/log/asr.7.bestpath.log \
		set -o pipefail '&&'\
		lattice-best-path \
		--lm-scale=$lmwt \
		--word-symbol-table=$lang/words.txt \
		"ark:gunzip -c $data_dir/lat.gz|" \
		ark,t:$data_dir/one-best-tri3a.tra

	echo "${phase[7]}"
	echo 80
		run.pl build/log/asr.8.convert.log \
		utils/int2sym.pl -f 2- \
		$lang/words.txt \
		$data_dir/one-best-tri3a.tra \
		">&" $output_dir/hyp.txt
		
	echo "Generated hypothesis. Process finished."

	if [ $score_result -eq 1 ]; then
		run.pl build/log/asr.9.wer.log \
		cat $output_dir/hyp.txt \| \
		sed 's:\<UNK\>::g' \| \
		compute-wer --text --mode=present ark:$score_reftxt ark,p:- ">&" build/wer.txt
	fi

	echo "${phase[9]}"
	echo 100
		run.pl build/log/asr.9.align.log \
		set -o pipefail '&&'\
		lattice-1best --lm-scale=$lmwt "ark:gunzip -c $data_dir/lat.gz|" ark:- \| \
		lattice-align-words $lang/phones/word_boundary.int exp/tri3a/final.mdl ark:- ark:- \| \
		nbest-to-ctm --frame-shift=$frame_shift --print-silence=$print_silence ark:- - \| \
		utils/int2sym.pl -f 5 $lang/words.txt \| \
		cat '>' $output_dir/word.ctm
} | whiptail --title 'Taglish ASR System' --gauge "Processing audio..." 6 60 0
stage=2
fi

whiptail --title 'Taglish ASR System' --msgbox "Finished. Check the $data_dir directory." 7 60

if [ $stage -eq 2 ]; then
	run.pl build/log/asr.10.phonealign.log \
	set -o pipefail '&&'\
	lattice-1best --lm-scale=$lmwt "ark:gunzip -c $data_dir/lat.gz|" ark:- \| \
	lattice-align-phones --replace-output-symbols=true exp/tri3a/final.mdl ark:- ark:- \| \
	nbest-to-ctm --frame-shift=0.01 --print-silence=false ark:- - \| \
	utils/int2sym.pl -f 5 $lang/phones.txt \| \
	cat '>' $output_dir/phone.ctm
	
	local/split_word_ctm.py
	local/split_phone_ctm.py
	line=$(cat $data_dir/wav.scp)
	for word in $line; do
		if [[ "$word" == *"waves"* ]]; then
			continue;
		fi
		local/ctm2srt.py $output_dir/"$word".ctm $output_dir/"$word".srt $lang/words.txt;
	done
fi
