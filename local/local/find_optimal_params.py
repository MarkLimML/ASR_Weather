#!/usr/bin/env python3
import sys

if(len(sys.argv) < 2):
    print("usage: python3 local/find_optimal_param.py <param-type> (tri|delta|lda|sat)")
    print( " Param Type:")
    print( "    1      # find optimal number of leaves")
    print( "    2      # find optimal number of gaussians")
    sys.exit();

ave = 0.0
param = ""
min = 100.0
ctr = ""

if(sys.argv[1] == "1"):
    with open("transform_log/leaves_"+sys.argv[2]+".txt") as fp:
        for i, line in enumerate(fp):
            if(sys.argv[2] == "tri"):
                if("steps/train_deltas.sh --boost-silence" in line):
                    l = line.split(" ")
                    param = l[5]+" "+l[6]
            elif(sys.argv[2] == "delta"):
                if("steps/train_deltas.sh --cmd" in line):
                    l = line.split(" ")
                    param = l[3]+" "+l[4]
            elif(sys.argv[2] == "lda"):
                if("steps/train_lda_mllt.sh --cmd" in line):
                    l = line.split(" ")
                    param = l[3]+" "+l[4]
            elif(sys.argv[2] == "sat"):
                if("steps/train_sat.sh --cmd" in line):
                    l = line.split(" ")
                    param = l[3]+" "+l[4]
            if("local/get_average_wer.py" in line):
                l = line.split(" ")
                ave += float(l[6][0:5])
                if(ave < min):
                    min = ave
                    ctr = param
                print("Param: "+param+"\n"+"WER: "+"{:.2f}".format(ave))
            ave = 0.0

elif(sys.argv[1] == "2"):
    with open("transform_log/gauss_"+sys.argv[2]+".txt") as fp:
        for i, line in enumerate(fp):
            if(sys.argv[2] == "tri"):
                if("steps/train_deltas.sh --boost-silence" in line):
                    l = line.split(" ")
                    param = l[5]+" "+l[6]
            elif(sys.argv[2] == "delta"):
                if("steps/train_deltas.sh --cmd" in line):
                    l = line.split(" ")
                    param = l[3]+" "+l[4]
            elif(sys.argv[2] == "lda"):
                if("steps/train_lda_mllt.sh --cmd" in line):
                    l = line.split(" ")
                    param = l[3]+" "+l[4]
            elif(sys.argv[2] == "sat"):
                if("steps/train_sat.sh --cmd" in line):
                    l = line.split(" ")
                    param = l[3]+" "+l[4]
            if("local/get_average_wer.py" in line):
                l = line.split(" ")
                ave += float(l[6][0:5])
                if(ave < min):
                    min = ave
                    ctr = param
                print("Param: "+param+"\n"+"WER: "+"{:.2f}".format(ave))
            ave = 0.0

print("Minimum WER: "+"{:.2f}".format(min)+"\n"+"With param: "+ctr)