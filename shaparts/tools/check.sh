#!/bin/bash

for i in $(ls calculations);
do
    printf "__________________________________________________________\n";
    printf "started %s\n" "$i";
    cp calculations/"$i" data/input1.json;
    make self_gen_witness 1>/dev/null;
    python tools/check.py witness/witness.json twitness/witness.json;
done
printf "__________________________________________________________\n";
