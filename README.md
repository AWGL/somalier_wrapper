# somalier_wrapper.py

## Description
A python wrapper script for estimating relatedness between samples and predicting sample ancestry using [somalier](https://github.com/brentp/somalier/). 

## Installation
This repository can be cloned from GitHub
```
https://github.com/AWGL/somalier_wrapper.git
```

Additional files, programs, or resources required are:
- A static binary of [somalier](https://github.com/brentp/somalier/releases/) (v0.2.19). Must be added to .bashrc
- Reference genome GRCh38
- [Sites file](https://github.com/brentp/somalier/files/3412456/sites.hg38.vcf.gz) specifying informative polymorphic sites
- Somalier files for 1k genomes (available [here](https://zenodo.org/record/3479773/files/1kg.somalier.tar.gz))
- Ancestry labels file for 1k genomes (available [here](https://raw.githubusercontent.com/brentp/somalier/master/scripts/ancestry-labels-1kg.tsv))


## Run

somalier_wrapper.py can be run from anywhere, using the following commands:
```
python bin/somalier_wrapper.py \
--sample_info_csv tso_repeated_testing_anonymised.csv \
--fasta /data/resources/human/references/GRCh38_masked/GRCh38_full_analysis_set_plus_decoy_hla_masked.fa \
--sites /data/resources/human/somalier/sites.hg38.vcf.gz \
--somalier_1K_directory /data/resources/human/somalier/1K_genomes \
--somalier_1K_labels /data/resources/human/somalier/ancestry-labels-1kg.tsv \
--patient_identifier patient_identifier_column_name \
--prefix tso_repeats
```

A description of each flag is provided below:
| Flag                       | Description                                                                                         | Required or optional? |
| -------------------------- | --------------------------------------------------------------------------------------------------- | --------------------- |
| --sample_info_csv	         | A comma seperated file with column headings: sample_id, cram_path                                   | Required              |
| --fasta                    | Path to the reference sequenced against which the sample reads were aligned                         | Required              |
| --sites                    | Path to somalier informative sites file                                                             | Required              |
| --prefix                   | Prefix to use when naming output files                                                              | Required              |
| --patient_identifier       | Patient identifier column name (see notes below)                                                    | Optional              |
| --somalier_1K_directory    | Path to directory containing genome sketches for 1K Genomes Project samples                         | Optional              |
| --somalier_1K_labels       | Path to ancestry-labels-1kg.tsv specifying known population assignments for 1K Genomes samples      | Optional              |

## Notes:
### Running somalier_wrapper.py with known sample relationships
A unique patient identifier can be added as a third field within the sample_info csv file which (if included) is used to indicate multiple samples from the same patient. To activate this functionality the optional flag *--patient_identifier* must be passed followed by a string specifying the column name. Sample pairs from the same patient will be highlighted within the html report produced by **somalier relate**.

### Predicting sample ancestry
When both *--somalier_1K_directory* and *--somalier_1K_labels* flags are specified **somalier ancestry** will be invoked and samples assigned to superpopulations based on clustering in PC space. 1K Genome samples of known population ancestry are used as a guide. Samples are assigned to the following superpopulations: EAS, AFR, AMR, SAS, and EUR. Output file: ".somalier-ancestry.tsv".

## Author:
Ash Sendell-Price, Oct 2024