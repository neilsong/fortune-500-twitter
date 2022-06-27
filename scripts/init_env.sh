#!/bin/bash
conda install mamba -n base -c conda-forge --yes
mamba env create
eval "$(conda shell.bash hook)"
conda activate f500