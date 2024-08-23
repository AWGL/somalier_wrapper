#!/usr/bin/env python

import argparse
import subprocess
import os
import glob
import csv
import logging
import pandas as pd


def parse_arguments():
	argument_parser = argparse.ArgumentParser()
	argument_parser.add_argument("--sample_info_csv", help="requires following columns: sample_id, cram_path and (optional) patient_identifier", required=True)
	argument_parser.add_argument("--fasta", help="Path to reference genome", required=True)
	argument_parser.add_argument("--sites", help="Path to sites file", required=True)
	argument_parser.add_argument("--prefix", help="Prefix for results", required=True)
	argument_parser.add_argument("--patient_identifier", help="Column specifying unique patient identifier (optional)", required=False)
	argument_parser.add_argument("--somalier_1K_directory", help="Path to directory containing .somalier files for 1K genomes", required=False)
	args = argument_parser.parse_args("--somalier_1K_labels", help="Path to labels file for 1K genomes samples", required=False)
	return args


def somalier_extract(file, sites, ref):
	"""
	Extract informative sites from sample crams
	"""
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

			# Construct command for extracting informative sites from CRAMs
			cmd = (
				f"somalier extract "
				f"--sites {sites} "
				f"--fasta {ref} "
				f"--out-dir {output_dir} "
				f"{cram_path}"
			)
			
			# Run command
			try:
				if os.path.exists(f"{output_dir}/{sample_id}.somalier"):
					logging.info(f"Extraction successful for sample: {sample_id} (using previous extraction)")
				else:
					subprocess.run(cmd, shell=True, check=True)
					logging.info(f"Extraction successful for sample: {sample_id}")
			except subprocess.CalledProcessError as e:
				logging.error(f"Error occurred while extracting sample: {sample_id}")
				logging.error(str(e))


def somalier_relatedness(file, prefix):
	"""
	Run somalier relate without groups file e.g. when sample pairs are not known
	"""

	# Get list of .somalier files in the specified directory
	# If no files present return error
	somalier_files = glob.glob("somalier_output/temp/*.somalier") ## <- update so that only looks at specified samples
	if not somalier_files:
		logging.warning("No .somalier files found in 'somalier_output/temp/' directory.")
		return

	# Join list into a single string
	somalier_files_str = ' '.join(somalier_files)

	# Construct command
	cmd = (
		f"somalier relate "
		f"{somalier_files_str} "
		f"--output-prefix somalier_output/{prefix}"
	)

	# Run command
	try:
		subprocess.run(cmd, shell=True, check=True)
		logging.info(f"Relatedness analysis completed.")
	except subprocess.CalledProcessError as e:
		logging.error("Error occurred during somalier relate.")
		logging.error(str(e))

		
def somalier_relatedness_expected(file, identifier, prefix):
	"""
	Run somalier relate with groups file (use when sample relationships are known 
	e.g. multiple samples are from the same patient)
	"""

	# Load sample IDs and patient identifier from CSV file
	df = pd.read_csv(file, usecols=['sample_id', identifier])

	# Check that the given patient identifier column is present in the sample info csv
	if identifier not in df.columns:
		raise ValueError(f"The identifier '{identifier}' is not present in the file '{file}'.")

	# Group by patient identifier and join sample IDs
	grouped = df.groupby(identifier)['sample_id'].apply(lambda x: ','.join(x)).reset_index()

	# Write to file without quotes
	output_file = 'somalier_output/expected_relationships.csv'
	with open(output_file, 'w') as f:
		for item in grouped['sample_id']:
			print(item)
			f.write(f"{item}\n")

	# Get list of .somalier files in the specified directory
	# If no files present return error
	somalier_files = glob.glob("somalier_output/temp/*.somalier") ## <- update so that only looks at specified samples
	if not somalier_files:
		logging.warning("No .somalier files found in 'somalier_output/temp/' directory.")
		return

	# Join list into a single string
	somalier_files_str = ' '.join(somalier_files)

	# Construct command
	cmd = (
		f"somalier relate "
		f"{somalier_files_str} "
		f"--output-prefix somalier_output/{prefix} "
		f"--groups somalier_output/expected_relationships.csv"
	)

	# Run command
	try:
		subprocess.run(cmd, shell=True, check=True)
		logging.info(f"Relatedness analysis completed with groups file: somalier_output/expected_relationships.csv")
	except subprocess.CalledProcessError as e:
		logging.error("Error occurred during somalier relate.")
		logging.error(str(e))


def somalier_ancestry(path_1K, ancestry_labels, prefix):

	# Get list of .somalier files for 1K genomes
	somalier_1K_files = glob.glob(f"{path_1K}/*.somalier")
	somalier_1K_files = ' '.join(somalier_1K_files)

	# Get list of .somalier files for samples
	somalier_files = glob.glob("somalier_output/temp/*.somalier")
	somalier_files = ' '.join(somalier_files)

	# Construct command
	cmd = (
		f"somalier ancestry "
		f"--labels {ancestry_labels}"
		f"{somalier_1K_files}"
		f"{somalier_files} "
		f"--output-prefix {prefix}"
	)

def main():
	# Set log format
	logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
	
	# Gather command line argumentsCalledProcessError
	args = parse_arguments()
	
	# Extract informative sites from CRAMs
	somalier_extract(args.sample_info_csv, args.sites, args.fasta)
	
	# Calculate pairwise relatedness between all samples
	if args.patient_identifier:
		somalier_relatedness_expected(args.sample_info_csv, args.patient_identifier, args.prefix)
	else:
		somalier_relatedness(args.sample_info_csv, args.prefix)
	
	# Estimate sample population ancestry
	if args.somalier_1K_directory and args.somalier_1K_labels:
		somalier_ancestry(args.somalier_1K_directory, args.somalier_1K_labels, args.prefix)

	
if __name__ == "__main__":
	main()
