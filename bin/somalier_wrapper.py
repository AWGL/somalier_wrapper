#!/usr/bin/env python

import argparse
import subprocess
import os
import glob

def parse_arguments():
	argument_parser = argparse.ArgumentParser()
	argument_parser.add_argument(
		"--sample_info_tsv",
		help="Tab delimited file specifying sampleIDs and paths to bam/cram file",
		required=True,
	)
	argument_parser.add_argument(
		"--fasta", help="Path to reference genome", required=True
	)
	argument_parser.add_argument("--sites", help="Path to sites file", required=True)
	argument_parser.add_argument("--prefix", help="Prefix for results", required=True)
	argument_parser.add_argument("--keep", help="Keeps temp directory", required=False)
	args = argument_parser.parse_args()
	return args


def somalier_extract(file, sites, ref):
	try:
		# Make output directory if it doesn't already exist
		os.makedirs("somalier_output", exist_ok=True)
		print(f"Output directory sucessfully created")
	except Exception as e:
		print(f"Error creating output directory: {e}")
		raise
	
	with open(file, "rt") as f:
		for line in f:

			# Get sample ID and path to bam/cram
			sample_id = line.strip().split("\t")[0]
			bam_path = line.strip().split("\t")[1]

			# Extract informative sites from bam
			cmd = (
				f"somalier extract "
				f"--sites {sites} "
				f"--fasta {ref} "
				f"--sample-prefix {sample_id} "
				f"--out-dir somalier_output/temp "
				f"{bam_path}"
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
	somalier_relate(args.prefix)

if __name__ == "__main__":
	main()