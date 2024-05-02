#!/bin/bash

# run_trimmomatic.sh

if [ "$#" -ne 6 ]; then
    echo "Usage: $0 <input_forward> <input_reverse> <output_paired_forward> <output_unpaired_forward> <output_paired_reverse> <output_unpaired_reverse>"
    exit 1
fi

input_forward=$1
input_reverse=$2
output_paired_forward=$3
output_unpaired_forward=$4
output_paired_reverse=$5
output_unpaired_reverse=$6

trimmomatic PE -threads 5 \
    "$input_forward" "$input_reverse" \
    "$output_paired_forward" "$output_unpaired_forward" \
    "$output_paired_reverse" "$output_unpaired_reverse" \
    ILLUMINACLIP:"/home/pablorr24/snake_folder/adapters/TruSeq2-SE.fa":2:30:10 \
    LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36
