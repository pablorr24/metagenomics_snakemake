#This script creates a rarefaction curve from an OTU table.
#Not working fully (not sure why) but it does create a rarefaction curve.
#May need metadata

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import resample

def safe_rarefaction_curve(otu_table, depth_steps=10, iterations=100):
    """
    Generate a rarefaction curve from an OTU table, using safe sampling depths.
    Args:
    - otu_table (DataFrame): OTU table with samples as columns and OTUs as rows.
    - depth_steps (int): Number of depth steps to include in the curve.
    - iterations (int): Number of iterations for averaging the rarefied richness.
    
    Returns:
    - DataFrame: Rarefaction data (average and standard deviation of OTU richness).
    """
    # Find the maximum depth that is safe for all samples
    min_non_zero_counts = otu_table[otu_table > 0].min()
    safe_max_depth = min_non_zero_counts.min()
    print(safe_max_depth)

    # Define a range of depths, ensuring they are within the safe range
    depth_range = np.linspace(start=10, stop=safe_max_depth, num=depth_steps).astype(int)
    #depth_range = np.linspace(start=1, stop=safe_max_depth, num=depth_steps).astype(int)
    print(depth_range)

    rarefaction_data = pd.DataFrame(index=depth_range, columns=['mean', 'std'])

    for depth in depth_range:
        richness_values = []

        for _ in range(iterations):
            subsampled_otu = otu_table.apply(lambda x: resample(x, n_samples=min(depth, sum(x)), replace=False) if sum(x) > 0 else x, axis=0)
            richness = subsampled_otu.astype(bool).sum(axis=0)
            richness_values.append(richness.mean())

        rarefaction_data.loc[depth, 'mean'] = np.mean(richness_values)
        rarefaction_data.loc[depth, 'std'] = np.std(richness_values)

    return rarefaction_data


# Load your OTU table (adjust the file path as needed)
#otu_table = pd.read_csv('/home/pablorr24/snake_folder/output/result08-Jan-2024-12/otu_table_F.csv', index_col=0)
#otu_table = pd.read_csv('/home/pablorr24/Documents/otu_test.csv', index_col=0)
otu_table = pd.read_csv('/home/pablorr24/Downloads/csvotu_table.csv', index_col=0)


# Call the function
rarefaction_data = safe_rarefaction_curve(otu_table)

# Plot the curve (optional)
plt.figure(figsize=(10, 6))
plt.errorbar(rarefaction_data.index, rarefaction_data['mean'], yerr=rarefaction_data['std'], fmt='-o')
plt.title('Rarefaction Curve')
plt.xlabel('Sequencing Depth')
plt.ylabel('Average Observed OTU Richness')
plt.grid(True)
plt.savefig('rarefaction_curve.png')  # Save the plot as a PNG file
plt.show()
