#This script plots the rarefaction curve of the samples, by the desired taxonomic level

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

def load_and_filter_data(file_path, taxonomic_level):
    """
    Load Kraken report and filter data by taxonomic level.
    """
    kraken_data = pd.read_csv(file_path, sep='\t', header=None, usecols=[1,2,3,4,5],
                              names=['percentage', 'reads', 'tax_reads', 'level', 'tax_id', 'name'])
    filtered_data = kraken_data[kraken_data['level'] == taxonomic_level.upper()]
    return filtered_data['reads'].values

def rarefaction_curve(reads, max_depth, step=100, iterations=10):
    """
    Generate a rarefaction curve from read counts.
    """
    depths = range(0, max_depth + step, step)
    species_counts = np.zeros((iterations, len(depths)))
    
    for i in range(iterations):
        for j, depth in enumerate(depths):
            if depth == 0:
                continue
            subsampled = np.random.choice(reads, size=depth, replace=True)
            unique_taxa = len(np.unique(subsampled))
            species_counts[i, j] = unique_taxa
    
    mean_species_counts = species_counts.mean(axis=0)
    return depths, mean_species_counts

def extract_sample_name(file_path):
    """
    Extract the sample name from the file path.
    """
    return file_path.split('/')[-1].split('_kraken2_report')[0]

def main(input_file, taxonomic_level, output_file):
    # Plot setup
    plt.figure(figsize=(10, 6))

    with open(input_file, 'r') as f:
        for line in f:
            file_path = line.strip()
            sample_name = extract_sample_name(file_path)
            read_counts = load_and_filter_data(file_path, taxonomic_level)
            max_depth = min(1000, sum(read_counts))
            depths, mean_species_counts = rarefaction_curve(read_counts, max_depth)
            plt.plot(depths, mean_species_counts, label=sample_name)

    plt.title('Rarefaction Curve of Selected Samples')
    plt.xlabel('Sequencing Depth')
    plt.ylabel('Number of Unique OTUs')
    plt.legend(title="Samples", loc='upper right')
    plt.grid(True)

    # Save the plot as a JPEG image
    plt.savefig(output_file, format='jpg')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate and save rarefaction curves from multiple Kraken reports.')
    parser.add_argument('--input', type=str, required=True, help='File containing paths to Kraken report files')
    parser.add_argument('--taxlevel', type=str, required=True, help='Taxonomic level to analyze (e.g., S for species, F for family)')
    parser.add_argument('--output', type=str, required=True, help='Output filename for the plot (JPEG format)')

    args = parser.parse_args()
    main(args.input, args.taxlevel, args.output)

#Run individually
#python3 rarefaction_curve.py --input '/home/.../kraken_report_paths.txt' --taxlevel 'C' --output "plot.jpg"
