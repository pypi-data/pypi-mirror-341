# msa_handler

msa_handler is a Python package that processes multiple sequence alignments (MSAs) and maps aligned residue positions to the original residue numbers using Biopython.

## Overview

This package allows you to:
- Parse MSA files in FASTA format.
- For each alignment column, generate objects that include:
  - The sequence header.
  - The aligned amino acid (or gap).
  - The original residue number (None for gaps).

## Installation

Ensure you have Python 3.6 or later installed. Install the package using pip:

```bash
pip install msa_handler

## Usage

from Bio import AlignIO
from msa_handler import build_msa_columns

alignment = AlignIO.read("your_alignment.fasta", "fasta")
columns = build_msa_columns(alignment)

# Print details of the first column
print(columns[0])

Requirements
Python >= 3.6

Biopython
