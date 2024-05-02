#python3 scripts/gzip_to_fq.py data/

import os
import gzip
import shutil
import argparse

def decompress_files(path_to_samples):
    # Filter for .gz files
    files = [f for f in os.listdir(path_to_samples) if f.endswith('.fq.gz') or f.endswith('.fasta.gz')]
    for file in files:
        gz_file_path = os.path.join(path_to_samples, file)
        # Construct output file path by removing '.gz' extension
        fq_file_path = gz_file_path.rsplit('.', 1)[0]
        
        # Check if the decompressed file already exists to avoid redundant work
        if os.path.exists(fq_file_path):
            print(f"Skipped decompression for {file} as uncompressed file already exists.")
            continue
        
        with gzip.open(gz_file_path, 'rb') as f_in:
            with open(fq_file_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        print(f"Decompressed {file} to {fq_file_path}")

def main():
    parser = argparse.ArgumentParser(description='Decompress .fq.gz files into .fq format in the same folder.')
    parser.add_argument('folder', type=str, help='Path to the folder containing .fq.gz files to decompress.')
    
    args = parser.parse_args()
    
    decompress_files(args.folder)

if __name__ == "__main__":
    main()
