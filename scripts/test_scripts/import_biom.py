#This script converts a BIOM file to a Pandas DataFrame and optionally saves it as a CSV file.

import biom
import pandas as pd

# Load BIOM file
table = biom.load_table('/home/pablorr24/Downloads/otu_table_even.biom')

# Convert to Pandas DataFrame
df = table.to_dataframe()

# Optionally, convert to CSV
df.to_csv('/home/pablorr24/Downloads/csvotu_table.csv')
