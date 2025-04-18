#!/usr/bin/env python3
"""
This is a command-line tool to extract all PDB files from a Quiver file.

Usage:
    qvextract.py <quiver_file>
"""

import os

from quiver import Quiver

import argparse


def main():
    # Parse the command-line arguments
    parser = argparse.ArgumentParser(description="Extract PDB files from a Quiver file")
    parser.add_argument("quiver_file", help="the Quiver file to extract PDB files from")

    args = parser.parse_args()

    qv = Quiver(args.quiver_file, "r")

    for tag in qv.get_tags():
        outfn = f"{tag}.pdb"

        if os.path.exists(outfn):
            print(f"File {outfn} already exists, skipping")
            continue

        lines = qv.get_pdblines(tag)
        with open(outfn, "w") as f:
            for line in lines:
                f.write(line)

    print(f"Successfully extracted {qv.size()} PDB files from {args.quiver_file}")


if __name__ == "__main__":
    main()
