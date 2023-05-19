#!/bin/sh

echo "Converting the MINT Files"

for f in ../Microfluidics-Benchmarks/MINT-TestCases/chthesis/*.mint;

do
    echo "Runnign File $f";
    fluigi convert-to-parchmint $f --assign-terminals --generate-graph-view --outpath ~/MINT-to-json/chthesis
done

for f in ../Microfluidics-Benchmarks/MINT-TestCases/dropx_ref/*.mint;

do
    echo "Runnign File $f";
    fluigi convert-to-parchmint $f --assign-terminals --generate-graph-view --outpath ~/MINT-to-json/dropx_ref
done

for f in ../Microfluidics-Benchmarks/MINT-TestCases/grid/*.mint;

do
    echo "Runnign File $f";
    fluigi convert-to-parchmint $f --assign-terminals --generate-graph-view --outpath ~/MINT-to-json/grid
done