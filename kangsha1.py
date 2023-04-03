#!/usr/bin/env python

import hashlib
import sys
import fileinput

vendor = "sony"
device = "tama-common-kddi"
vendor_path = f"../../../vendor/{vendor}/{device}/proprietary"

def list_sections():
    sections = []
    with open("proprietary-files.txt") as f:
        for line in f:
            line = line.strip()
            if line.startswith("#"):
                section = line[1:].strip()
                sections.append(section)
    print("Available sections:")
    print("\n".join(sections))

if len(sys.argv) == 1:
    print("Please enter a section name to display its files.")
    print("Usage: ./kangsha1.py [SECTION NAME]")
    print("You can also run 'python kangsha1.py list' to list available sections.")
    sys.exit(1)

if sys.argv[1] == "list":
    list_sections()
    sys.exit(0)

section_found = False
section = ""
for line in fileinput.input("proprietary-files.txt", inplace=True):
    line = line.strip()
    if line.startswith("#"):
        section = line[1:].strip()
        section_found = section == sys.argv[1]
        print()
        print(line)
    elif not line:
        if section_found:
            print()
        continue
    elif section_found:
        path = f"{vendor_path}/{line}"
        try:
            with open(path, "rb") as file:
                sha1 = hashlib.sha1(file.read()).hexdigest()
                print(f"{line}|{sha1}")
        except FileNotFoundError:
            print(f"# File not found: {path}")
            print(line)
    else:
        print(line)
