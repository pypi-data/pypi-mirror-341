#!/usr/bin/env python3
"""
This script takes a Quiver file and extracts the scorefile from it
Usage:
    qvscorefile.py <mydesigns.qv>

"""

import sys
import os
import argparse
import pandas as pd


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Extract scorefile from Quiver file")
    parser.add_argument(
        "qvfile", type=str, help="Quiver file to extract scorefile from"
    )

    args = parser.parse_args()

    # Iterate though the Quiver file and extract the scorelines
    records = []

    with open(args.qvfile, "r") as qvfile:
        for line in qvfile:
            if line.startswith("QV_SCORE"):
                splits = line.split()
                tag = splits[1]

                scores = {
                    entry[0]: float(entry[1])
                    for entry in [score.split("=") for score in splits[2].split("|")]
                }
                scores["tag"] = tag

                # Replace empty strings with None
                for key, value in scores.items():
                    if value == "":
                        scores[key] = None

                records.append(scores)
    if records == []:
        print("No scorelines found in Quiver file", file=sys.stderr)
        sys.exit(1)

    # Convert to dataframe
    df = pd.DataFrame.from_records(records)

    # Write to scorefile
    outfn = os.path.splitext(args.qvfile)[0] + ".sc"
    df.to_csv(outfn, sep="\t", na_rep="NaN", index=False)


if __name__ == "__main__":
    main()
