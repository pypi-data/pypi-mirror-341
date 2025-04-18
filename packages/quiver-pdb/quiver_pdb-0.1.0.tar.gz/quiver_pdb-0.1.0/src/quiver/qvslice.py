#!/usr/bin/env python3
"""
This is a command-line tool to slice a specific set of tags from a Quiver file
into another Quiver file.

Usage:
    qvslice.py big.qv <tag1> <tag2> ... <tagN> > smaller.qv
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

# We are going to use the get_struct_list function instead here
qv_lines, found_tags = qv.get_struct_list(tags)

for tag in tags:
    if tag not in found_tags:
        print(f"Error: tag {tag} not found in Quiver file", file=sys.stderr)

# Just print to stdout so that we can redirect to a file
# Write the qv_lines to stdout
print(qv_lines, end="")
