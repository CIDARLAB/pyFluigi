#!/bin/sh

echo "Running PRIMITIVE TESTS"

date

echo "-----------------------"

FOLDER=out/par/benchmarking_out_"`date +"%d-%m-%Y-%T"`"

echo "Generating results in $FOLDER"


for f in ./Microfluidics-Benchmarks/MINT-TestCases/primitive/*.mint;

do
    echo "Running File $f";
    fluigi  convert-to-parchmint --outpath "$FOLDER/MINT-to-json/primitives" $f
    fluigi  mint-compile --outpath "$FOLDER/MINT-to-par/primitives" $f
done
