#!/usr/bin/python3

import sys

def usage():
    print(
    """
    ./addarticle.py  <htmlfile>
    """
    )

def getText(htmlfile):
    with open(htmlfile) as f:
        text = f.read()

    return text

if __name__ == "__main__":
    print(getText(sys.argv[1]))
