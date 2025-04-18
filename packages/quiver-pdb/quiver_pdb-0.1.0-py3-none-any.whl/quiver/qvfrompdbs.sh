#!/bin/bash

# This script takes a list of PDB IDs and generates a Quiver file from them

# Usage: qvfrompdbs.sh <pdb1> <pdb2> ... <pdbN> > mydesigns.qv

# Parse arguments
if [ $# -lt 1 ]; then
    echo "Usage: qvfrompdbs.sh <pdb1> <pdb2> ... <pdbN> > mydesigns.qv" >&2
    exit 1
fi

# Loop over PDB IDs
for pdbfn in "$@"
do
    # Get PDB tag
    pdbtag=$(basename $pdbfn .pdb)

    # Print this entry to stdout
    echo "QV_TAG ${pdbtag}"
    cat $pdbfn

done


