#!/usr/bin/env python3
"""
This is a command-line tool to rename the tags in a Quiver file.

Usage:
    qvls.py <quiver_file> | sed 's/$/_newsuffix/g' | qvrename.py <quiver_file>

"""

import sys
import os

from quiver import Quiver

# Thanks to bcov for this code
import stat

quiver_file = sys.argv[1]

tag_buffers = []
if stat.S_ISFIFO(os.stat("/dev/stdin").st_mode):
    tag_buffers += sys.stdin.readlines()
tag_buffers += sys.argv[2:]

tags = []
for line in tag_buffers:
    line = line.strip()
    if len(line) == 0:
        continue
    sp = line.split(" ")
    for tag in sp:
        tags.append(tag)

qv = Quiver(quiver_file, "r")

present_tags = qv.get_tags()

assert len(present_tags) == len(tags), (
    f"Number of tags in file ({len(present_tags)}) does not match number of tags provided ({len(tags)})"
)

# Now iterate through the file and rename the tags in the order they appear

tag_idx = 0
with open(quiver_file, "r") as f:
    for line in f:
        if line.startswith("QV_TAG"):
            line = f"QV_TAG {tags[tag_idx]}\n"

            # Check if the next line is a score line
            next_line = f.readline()

            if next_line.startswith("QV_TAG"):
                sys.exit(
                    f"Error: Found two QV_TAG lines in a row. This is not supported. Line: {next_line}"
                )

            if next_line.startswith("QV_SCORE"):
                splits = next_line.split(" ")
                splits[1] = tags[tag_idx]
                next_line = " ".join(splits)

            line += next_line

            tag_idx += 1

        sys.stdout.write(line)
