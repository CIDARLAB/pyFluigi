#!/bin/sh
set -x
echo "Converting the LFR Files"

echo "-----------------------"

FOLDER=out/convert/benchmarking_out_"`date +"%d-%m-%Y-%T"`"

echo "Generating results in $FOLDER"


for f in ./../Microfluidics-Benchmarks/LFR-TestCases/chthesis/*.lfr;

do
    echo "Running File $f";
    fluigi lfr-compile --outpath "$FOLDER/LFR-to-MINT/chthesis" $f
done