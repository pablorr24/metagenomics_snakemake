#This script creates a sequence bar chart showing the number of sequences per sample

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description="Generate a stacked bar chart from Kraken report files.")
parser.add_argument("-i", "--input", required=True, help="Input file containing paths to Kraken reports.")
parser.add_argument("-o", "--output", required=True, help="Output file for the generated bar chart.")
args = parser.parse_args()

# Function to process a single sample report file
def process_sample_report(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            line_parts = line.strip().split('\t')
            if len(line_parts) >= 6:
                taxonomic_level = line_parts[3]
                num_samples = int(line_parts[1])
                data.append((taxonomic_level, num_samples))
    df = pd.DataFrame(data, columns=['Taxonomic Level', 'Number of Samples'])
    df_grouped = df.groupby('Taxonomic Level')['Number of Samples'].sum().reset_index()
    df_grouped_sorted = df_grouped.sort_values(by='Number of Samples', ascending=False)
    return df_grouped_sorted

# Read the list of file paths from the input file
sample_files = []
with open(args.input, 'r') as txt_file:
    for line in txt_file:
        sample_files.append(line.strip())

# Determine unique taxonomic levels across all files (s,g,c,o,f...)
all_taxonomic_levels = set()
for file_path in sample_files:
    df_grouped_sorted = process_sample_report(file_path)
    all_taxonomic_levels.update(df_grouped_sorted['Taxonomic Level'].unique())

#grey color
grey_color = np.array([[0.5, 0.5, 0.5, 1]]) #GREY
other_colors = plt.cm.viridis(np.linspace(0, 1, len(all_taxonomic_levels)-1))
colors = np.vstack((grey_color, other_colors)) if '-' in all_taxonomic_levels else other_colors
color_mapping = {taxonomic_level: color for taxonomic_level, color in zip(sorted(all_taxonomic_levels), colors)}

# Handle '-' scenario
if '-' in color_mapping:
    color_mapping['-'] = [0.75, 0.75, 0.75]

# Extract the first 5 letters of each file as sample names (sample name)
sample_names = [os.path.basename(file).split('_kraken2_report')[0] for file in sample_files]

# Create a figure for the plot
plt.figure(figsize=(15, 12))


default_color = [0.8, 0.8, 0.8, 1] # RGBA

# Inside your plotting loop
for i, file_path in enumerate(sample_files):
    df_grouped_sorted = process_sample_report(file_path)
    bottom = np.zeros(len(sample_names))

    for j, row in df_grouped_sorted.iterrows():
        taxonomic_level = row['Taxonomic Level']
        # Use get method with a default fallback color
        color = color_mapping.get(taxonomic_level, default_color)
        plt.bar(sample_names[i], row['Number of Samples'], bottom=bottom[i], color=color, label=taxonomic_level)
        bottom[i] += row['Number of Samples']


#  labels and titles
plt.ylabel('Number of Sequences')
plt.title('Number of Sequences by Sample, Colored by Taxonomic Level')
#plt.xticks(rotation=45)
plt.xlabel('Sample Name')

# Adding a legend with unique taxonomic levels
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys(), title='Taxonomic Level', bbox_to_anchor=(1.05, 1), loc='upper left')

# Save the plot to the output file
plt.savefig(args.output, bbox_inches='tight')

