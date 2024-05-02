import pandas as pd
import os
import yaml
import sys


def check_metadata_file():
    # Construct the path to the configuration file in the current directory
    config_path = os.path.join(os.getcwd(), 'config_templates/config_post_analysis.yaml')
    
    # Read configuration from the YAML file
    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
    
    file_path = config['metadata_path']

    # Check if the file exists
    if os.path.exists(file_path):
        sys.stderr.write(f"Found file at '{file_path}'.\n")
        # Load the CSV file into a DataFrame
        metadata_df = pd.read_csv(file_path)

        # Check if the first column (SampleID) contains unique values
        if metadata_df['SampleID'].is_unique:
            sys.stderr.write("Success: The 'SampleID' column contains unique values. \n")
            # Check if there's only one unique SampleID
            if len(metadata_df['SampleID'].unique()) == 1:
                sys.stderr.write("\nError: There is only one sample. You can't do post-analysis of only one sample \n \n")
                return False
            else:
                return True
        else:
            sys.stderr.write("Error: The 'SampleID' column does not contain unique values. Please check for duplicates. \n")
            return False
    else:
        sys.stderr.write(f"Error: The file was not found at '{file_path}'.")
        return False

# Call the function without needing to specify the config_path
if check_metadata_file():
    pass
else:
    sys.exit(1)  # Exit the script with a non-zero status code

