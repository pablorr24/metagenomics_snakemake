import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import resample

def rarefaction_curve(otu_table, depth_steps=10, iterations=50):
    """
    Generate a rarefaction curve from an OTU table.
    Args:
    - otu_table (DataFrame): OTU table with samples as columns and OTUs as rows.
    - depth_steps (int): Number of depth steps to include in the curve.
    - iterations (int): Number of iterations for averaging the rarefied richness.
    
    Returns:
    - DataFrame: Rarefaction data (average and standard deviation of OTU richness).
    """
    max_depth = otu_table.sum().min()  # Maximum depth for subsampling
    depth_range = np.linspace(start=1, stop=max_depth, num=depth_steps).astype(int)
    rarefaction_data = pd.DataFrame(index=depth_range, columns=['mean', 'std'])

    for depth in depth_range:
        richness_values = []
        for _ in range(iterations):
            subsampled_otu = otu_table.apply(lambda x: resample(x, n_samples=min(depth, x.sum()), replace=False) if x.sum() > depth else x, axis=0)
            richness = subsampled_otu.astype(bool).sum(axis=0)
            richness_values.append(richness.mean())

        rarefaction_data.loc[depth, 'mean'] = np.mean(richness_values)
        rarefaction_data.loc[depth, 'std'] = np.std(richness_values)

    return rarefaction_data

# Load your OTU table (replace with the path to your OTU table file)
#otu_table = pd.read_csv('/home/pablorr24/Downloads/csvotu_table.csv', index_col=0)
otu_table = pd.read_csv('/home/pablorr24/Documents/otu_test.csv', index_col=0)
#otu_table = pd.read_csv('/home/pablorr24/snake_folder/output/result08-Jan-2024-12/otu_table_F.csv', index_col=0)


# Generate the rarefaction data
rarefaction_data = rarefaction_curve(otu_table)

# Plot the rarefaction curve
plt.figure(figsize=(10, 6))
plt.errorbar(rarefaction_data.index, rarefaction_data['mean'], yerr=rarefaction_data['std'], fmt='-o')
plt.title('Rarefaction Curve')
plt.xlabel('Sequencing Depth')
plt.ylabel('Average Observed OTU Richness')
plt.grid(True)
plt.show()