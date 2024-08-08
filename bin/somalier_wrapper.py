#!/usr/bin/env python

import argparse
import subprocess
import os
import glob
import csv

def parse_arguments():
	argument_parser = argparse.ArgumentParser()
	argument_parser.add_argument("--sample_info_csv", help="requires following columns: sample_id, cram_path and (optional) patient_identifier", required=True)
	argument_parser.add_argument("--fasta", help="Path to reference genome", required=True)
	argument_parser.add_argument("--sites", help="Path to sites file", required=True)
	argument_parser.add_argument("--prefix", help="Prefix for results", required=True)
	argument_parser.add_argument("--keep", help="Keeps temp directory", required=False)
	argument_parser.add_argument("--patient_identifier", help="column specifying unique patient identifier (optional)",required=False)
	args = argument_parser.parse_args()
	return args

def somalier_extract(file, sites, ref):
	# Make output directory if it doesn't already exist
	os.makedirs("somalier_output", exist_ok=True)
	print(f"Output directory sucessfully created")
	
	# Load csv file
	with open(csv_file, mode='r') as file:
    	# Create a DictReader object
		reader = csv.DictReader(file)
    
    	# Get sample IDs, run IDs, and CRAM paths
    	for row in reader:
			sample_id = row['sample_id']
			cram_path = row['cram_path']

			# Extract informative sites from cram
			cmd = (
				f"somalier extract "
				f"--sites {sites} "
				f"--fasta {ref} "
				f"--sample-prefix {sample_id} "
				f"--out-dir somalier_output/temp "
				f"{cram_path}"
			)
			subprocess.run(cmd, shell=True, check=True)

def somalier_relate(prefix):
	# Get list of .somalier files in the specified directory
	somalier_files = glob.glob("somalier_output/temp/*.somalier")
	
	# Join list into a single string
	somalier_files = ' '.join(somalier_files)
	
	# Construct command
	cmd = (
		f"somalier relate "
		f"{somalier_files} "
		f"--output-prefix somalier_output/{prefix}"
		)
	
	# Run command
	subprocess.run(cmd, shell=True, check=True)

def main():
	args = parse_arguments()
	somalier_extract(args.sample_info_tsv, args.sites, args.fasta)
	#somalier_relate(args.prefix)

if __name__ == "__main__":
	main()