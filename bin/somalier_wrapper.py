#!/usr/bin/env python

import argparse
import subprocess
import os


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
	argument_parser.add_argument("--outdir", help="Output directory", required=True)
	args = argument_parser.parse_args()
	return args


def somalier_extract(file, sites, ref, outdir):
	# Make output directory if doesn't already exist
	os.makedirs(outdir, exist_ok=True)

	with open(file, "rt") as f:
		for line in f:

			# Get sample ID and path to bam/cram
			sample_id = line.strip().split("\t")[0]
			bam_path = line.strip().split("\t")[1]

			# Extract informative sites from bam
			cmd = (
				f"somalier extract "
				f"--sites {sites} "
				f"--fasta {ref} -"
				f"-sample-prefix {outdir}/{sample_id} "
				f"{bam_path}"
			)
			subprocess.run(cmd, shell=True, check=True)


def main():
	args = parse_arguments()
	somalier_extract(args.sample_info_tsv, args.sites, args.fasta, args.outdir)
