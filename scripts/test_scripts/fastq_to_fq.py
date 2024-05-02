#converts fastq files into fq files

import os
import re

def rename_files(path_to_samples):
    files = os.listdir(path_to_samples)

    # Rename files ending with .fastq to .fq
    for file in files:
        if file.endswith('.fastq'):
            old_path = os.path.join(path_to_samples, file)
            new_file = file.replace('.fastq', '.fq')
            new_path = os.path.join(path_to_samples, new_file)
            os.rename(old_path, new_path)

    # Extract sample names from modified files
    samples = list(set([re.sub(r'_[12]\.fq$', '', file) for file in files if file.endswith('.fq')]))
    return samples

def main():
    path_to_samples = config_file['sample_path']
    samples = rename_files(path_to_samples)
    print("Files renamed successfully.")

if __name__ == "__main__":
   main()

