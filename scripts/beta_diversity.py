#this script calculates beta diversity via bray curtis distance

#This script was modified from 
### https://github.com/jenniferlu717/KrakenTools


import os, sys, argparse
import numpy as np
import csv
import re 

def calculate_bray_curtis(input_file_list, output_file_path, filetype='kreport2', cols='1,2', lvl='all'):
    # Read file paths from the provided text file
    with open(input_file_list, 'r') as file:
        in_files = file.read().splitlines()

    # Ensure the output directory exists
    output_dir = os.path.dirname(output_file_path)
    if not os.path.exists(output_dir) and output_dir != '':
        os.makedirs(output_dir, exist_ok=True)

    # Define a regex pattern to extract the sample name (based on kraken or centrifuge)
    sample_name_pattern = re.compile(r'.*/([^/]+)/(kraken2|centrifuge)/.*$')

    num_samples = 0
    i2names = {}
    i2totals = {}
    i2counts = {}
    genus = {}

    for f in in_files:
        if not os.path.isfile(f):
            sys.stderr.write(f"File {f} not found\n")
            sys.exit(1)

        # Use regex to extract the sample name
        match = sample_name_pattern.search(f)
        sample_name = match.group(1) if match else "UnknownSample"

        i2names[num_samples] = sample_name
        i2totals[num_samples] = 0
        i2counts[num_samples] = {}
        genus[num_samples] = {}

        with open(f, 'r') as i_file:
            for line in i_file:
                l_vals = line.strip().split("\t")
                if len(l_vals) == 0 or (not l_vals[1].isdigit()) or l_vals[0] == '#':
                    continue

                if int(l_vals[1]) > 0:  # Assuming the count column is the second one (index 1)
                    # Adjust the following condition based on your specific needs
                    if lvl == "all" or l_vals[3][0] == lvl:  # Assuming the taxonomy level is in the fourth column (index 3)
                        tax_id = l_vals[4]  # Assuming the category/taxonomy ID is in the fifth column (index 4)
                        genus[num_samples][tax_id] = l_vals[0]
                        i2totals[num_samples] += int(l_vals[1])
                        i2counts[num_samples].setdefault(tax_id, 0)
                        i2counts[num_samples][tax_id] += int(l_vals[1])
        num_samples += 1

    # Calculate Bray-Curtis 
    bc = np.zeros((num_samples, num_samples))
    for i in range(num_samples):
        for j in range(i + 1, num_samples):
            C_ij = sum(min(i2counts[i].get(k, 0), i2counts[j].get(k, 0)) for k in i2counts[i])
            sum_i = i2totals[i]
            sum_j = i2totals[j]
            bc_ij = 1 - (2 * C_ij) / (sum_i + sum_j) if (sum_i + sum_j) > 0 else np.nan
            bc[i, j] = bc_ij
            bc[j, i] = bc_ij

    # Write the results as CSV
    with open(output_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        headers = ['Sample'] + [i2names[i] for i in range(num_samples)]
        writer.writerow(headers)
        for i in range(num_samples):
            row = [i2names[i]] + [f'{bc[i, j]:0.3f}' if j != i else 'x.xxx' for j in range(num_samples)]
            writer.writerow(row)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True, dest='input_file_list',
                        help='Path to the text file containing input file paths, one per line')
    parser.add_argument('--type', required=False, default='kreport2', dest='filetype',
                        choices=['single', 'kreport2'])
    parser.add_argument('--cols', '--columns', dest='cols', required=False, default='1,2',
                        help='Specify category/counts separated by a single comma: cat,counts (1 = first col)')
    parser.add_argument('--level', '-l', dest='lvl', required=False, default='all',
                        choices=['all', 'S', 'G', 'F', 'O'],
                        help='Select taxonomy level for which to compare samples. Default: all')
    parser.add_argument('--output', '-o', required=True, dest='output_file_path',
                        help='Full path to the output file where the results will be saved')
    args = parser.parse_args()

    calculate_bray_curtis(args.input_file_list, args.output_file_path, args.filetype, args.cols, args.lvl)

if __name__ == "__main__":
    main()
