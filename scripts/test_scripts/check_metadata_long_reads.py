import pandas as pd
import os
import yaml
import sys

def check_metadata_file():
    # Construct the path to the configuration file in the current directory
    config_path = os.path.join(os.getcwd(), 'config_long.yaml')

    # Read configuration from the YAML file
    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
    
    file_path = config['metadata_file']

    # Check if the file exists
    if os.path.exists(file_path):
        sys.stderr.write(f"Found file at '{file_path}'.\n")
        # Load the CSV file into a DataFrame
        metadata_df = pd.read_csv(file_path)
        
        # Check if the first column (SampleID) contains unique values
        if metadata_df['SampleID'].is_unique:
            sys.stderr.write("Success: The 'SampleID' column contains unique values. \n")
        else:
            sys.stderr.write("Error: The 'SampleID' column does not contain unique values. Please check for duplicates. \n")
    else:
        sys.stderr.write(f"Error: The file was not found at '{file_path}'.")
        sys.stderr.write("\n You can continue without a metadata file but you cannot do the post processing \n")

# Call the function without needing to specify the config_path
#check_metadata_file()

