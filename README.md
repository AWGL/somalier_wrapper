# somalier_wrapper.py

## Description
A python wrapper script for estimating relatedness between samples and predicting sample ancestry using [somalier](https://github.com/brentp/somalier/)

## Run
```
python bin/somalier_wrapper.py --sample_info_csv tso_repeated_testing_anonymised.csv \
	--fasta /data/resources/human/references/GRCh38_masked/GRCh38_full_analysis_set_plus_decoy_hla_masked.fa \
	--sites /data/resources/human/somalier/sites.hg38.vcf.gz \
	--somalier_1K_directory /data/resources/human/somalier/1K_genomes \
	--somalier_1K_labels /data/resources/human/somalier/ancestry-labels-1kg.tsv \
	--prefix tso_repeats
```

## Author:
Ash Sendell-Price, Oct 2024