#This script calculate the alpha diversity of the kraken report files

#This script was modified from 
### https://github.com/jenniferlu717/KrakenTools

import os
import argparse
import math
import numpy as np
from scipy.optimize import fsolve
import warnings

warnings.filterwarnings('ignore', 'The iteration is not making good progress')

def write_results_to_file(filename, results):
    with open(filename, 'w') as f:
        for result in results:
            f.write(f"{result}\n")

def shannons_alpha(p):
    h = -sum(i * math.log(i) for i in p if i > 0)
    return f"Shannon: {h:.2f}"

def berger_parkers_alpha(p):
    bp = max(p)
    return f"Berger-Parker: {bp:.2f}"

def simpsons_alpha(D):
    si = 1 - D
    return f"Simpson: {si:.2f}"

def fishers_alpha(N, S):
    def eqn_output(a):
        return a * np.log(1 + N / a) - S

    fish = fsolve(eqn_output, 1)[0]
    return f"Fisher's: {fish:.2f}"

def calculate_all_indices(p, D, N, S):
    results = [
        shannons_alpha(p),
        berger_parkers_alpha(p),
        simpsons_alpha(D),
        fishers_alpha(N, S)
    ]
    return results

def main():
    parser = argparse.ArgumentParser(description='Calculate various alpha diversity indices.')
    parser.add_argument('-f', '--filename', dest='filename', help='File with species abundance estimates', required=True)
    parser.add_argument('-a', '--alpha', dest='value', default='Sh', type=str, help='Type of alpha diversity to calculate (Sh, BP, Si, F, all), default=Sh')
    parser.add_argument('-o', '--output', dest='output_file', help='Output file name', required=False)

    args = parser.parse_args()

    with open(args.filename) as f:
        #f.readline()  # Assuming the first line is a header
        n = [float(line.split('\t')[0]) for line in f]
        #n = [float(line.split('\t')[1]) for line in f]

    N = sum(n)  # Total number of individuals
    S = len(n)  # Total number of species
    p = [i / N for i in n if i != 0]  # Proportions
    D = sum(i * (i - 1) for i in n) / (N * (N - 1))  # Simpson's index base calculation
    

    if args.output_file:
        output_filename = args.output_file
    else:
        base_filename = os.path.splitext(os.path.basename(args.filename))[0]
        output_filename = f"alpha_diversity_{base_filename}.txt"

    if args.value == 'all':
        results = calculate_all_indices(p, D, N, S)
    else:
        indices_functions = {
            'Shannon': shannons_alpha,
            'BP': berger_parkers_alpha,
            'Simpsons': simpsons_alpha,
            'Fischer': lambda: fishers_alpha(N, S) 
        }
        results = [indices_functions[args.value](p) if args.value != 'F' else indices_functions[args.value]()] if args.value in indices_functions else ["Not a supported alpha"]

    write_results_to_file(output_filename, results)

if __name__ == "__main__":
    main()
