#!/usr/bin/env python

import argparse
import subprocess
import os
import glob
import csv
import logging

def parse_arguments():
	argument_parser = argparse.ArgumentParser()
	argument_parser.add_argument("--sample_info_csv", help="requires following columns: sample_id, cram_path and (optional) patient_identifier", required=True)
	argument_parser.add_argument("--fasta", help="Path to reference genome", required=True)
	argument_parser.add_argument("--sites", help="Path to sites file", required=True)
	argument_parser.add_argument("--prefix", help="Prefix for results", required=True)
	argument_parser.add_argument("--patient_identifier", help="Column specifying unique patient identifier (optional)", required=False)
	args = argument_parser.parse_args()
	return args

def somalier_extract(file, sites, ref):
	# Make output directory if it doesn't already exist
	output_dir = "somalier_output/temp"
	os.makedirs(output_dir, exist_ok=True)
	logging.info(f"Output directory {output_dir} successfully created")

	# Load CSV file
	with open(file, mode='r') as csv_file:
		# Create a DictReader object
		reader = csv.DictReader(csv_file)

		# Get sample IDs and CRAM paths
		for row in reader:
			sample_id = row['sample_id']
			cram_path = row['cram_path']
			
			logging.info(f"Processing sample: {sample_id} with CRAM path: {cram_path}")

			# Extract informative sites from CRAM
			cmd = (
				f"somalier extract "
				f"--sites {sites} "
				f"--fasta {ref} "
				f"--sample-prefix {sample_id} "
				f"--out-dir {output_dir} "
				f"{cram_path}"
			)
			try:
				if os.path.exists(f"{output_dir}/{sample_id}.somalier"):
					logging.info(f"Extraction successful for sample: {sample_id} (using previous extraction)")
				else:
					subprocess.run(cmd, shell=True, check=True)
					logging.info(f"Extraction successful for sample: {sample_id}")
			except subprocess.CalledProcessError as e:
				logging.error(f"Error occurred while extracting sample: {sample_id}")
				logging.error(str(e))

def somalier_relate(prefix):
	# Get list of .somalier files in the specified directory
	somalier_files = glob.glob("somalier_output/temp/*.somalier")
	
	# Check if there are somalier files to process
	if not somalier_files:
		logging.warning("No .somalier files found for processing.")
		return
	
	# Join list into a single string
	somalier_files = ' '.join(somalier_files)
	
	# Construct command
	cmd = (
		f"somalier relate "
		f"{somalier_files} "
		f"--output-prefix somalier_output/{prefix}"
	)
	
	# Run command
	try:
		subprocess.run(cmd, shell=True, check=True)
		logging.info(f"Relation analysis completed with prefix: {prefix}")
	except subprocess.CalledProcessError as e:
		logging.error(f"Error occurred during somalier relate.")
		logging.error(str(e))

def main():
	logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
	args = parse_arguments()
	somalier_extract(args.sample_info_csv, args.sites, args.fasta)
	somalier_relate(args.prefix)

if __name__ == "__main__":
	main()
