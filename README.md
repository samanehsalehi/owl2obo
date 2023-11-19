# Owl2Obo

Owl2Obo is a Python-based toolkit for working with ontologies, specifically designed to convert ontologies from the OWL format to the OBO format, createa network from OBO file and then examine the robustness of the network. It includes three main programs: `owl-obo.py`, `cross-ontology_parser.py`, and `Perturbation.py`.

## Table of Contents
- [Setup](#setup)
- [Requirements](#requirements)
- [Running programs](#runningprograms)
  - [`owl-obo.py`](#1-owl-obopy)
  - [`cross-ontology_parser.py`](#2-cross-ontology-parser.py)
  - [`Perturbation.py`](#3-perturbation.py)
- [Output](#output)
- [Contact](#contact)

## Setup
#### Clone the repository:
```bash
git clone git@github.com:samanehsalehi/owl2obo.git
```
## Requirements
#### Install requirements:
```bash
pip install -r requirements.txt
```
## Running programs

### 1. `owl-obo.py`

Converts ontologies from OWL format to OBO format.
**Command:**
```bash
python owl-obo.py -i input_file.owl -o output_file.obo
```
### 2. `cross-ontology_parser.py`
Extracts terms, term IDs, is-a relationships, and xref relations from an OBO file.
**Command:**
```bash
python cross-ontology_parser.py -i input_file.obo -o output_file.txt
```
### 3. `Perturbation.py`
Checks the robustness of a network created from the file generated by cross-ontology_parser.py.
**Command:**
```bash
python Perturbation.py -i input_file.txt
```
# Output
### 1. `owl-obo.py`
- obo file 
### 2. `cross-ontology_parser.py`
- text file
### 3. `Perturbation.py`
- csv file

# Contact
- Samaneh Salehi Nasab
- Email: samaneh.s@aol.com
