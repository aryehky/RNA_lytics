# Data Directory Structure

This directory contains all data files for the RNAlytics project.

## Directory Organization

### `/raw`
Contains raw RNA-seq data files:
- CsA treatment samples
- VOC treatment samples
- Control samples
- Quality control metrics

### `/processed`
Contains analyzed and transformed data:
- Normalized expression matrices
- Differential expression results
- Pathway analysis outputs
- GO term enrichment results

### `/metadata`
Contains experimental metadata:
- Sample information
- Treatment conditions
- Batch information
- Quality metrics

## File Naming Convention
- Raw files: `{treatment}_{replicate}_R{read}.fastq.gz`
- Processed files: `{analysis_type}_{treatment}_vs_control.csv`
- Metadata: `{dataset}_metadata.csv`

## Data Versions
Please note the version of data processing pipelines used:
- RNA-seq pipeline version: TBD
- DEG analysis version: TBD
- Pathway analysis version: TBD
