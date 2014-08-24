#! /usr/bin/env python
"""
Removes site tags (like DDLValley.net) from the beginning of your files. This
script is intended to use with pyLoad.
"""

import sys
import os
import argparse

# the list of tags to search for
TAGS = [
    '/DDLValley\.(eu|net|org|com)_/'
]

# default directory to search in
DIR = '~/Downloads/'


def searchAndRename(args):
    """Search for matching filenames and remove the matched pattern."""
    for path in args.paths:
        paths.append(os.path.expanduser(path))
    print paths
    #print os.listdir(os.path.expanduser(DIR))


def main():
    """The main function that is called automatically."""
    parser = argparse.ArgumentParser(
        description='Search for files containing a certain tag and remove it.')
    parser.add_argument(
        "paths", metavar='path',
        type=str, nargs='*',
        default=[DIR],
        help="The directories to search in. Default: {0}".format(DIR))
    parser.add_argument(
        '-n', '--dry-run',
        action='store_true',
        help="Don't change anything.")
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help="Verbose output.")
    args = parser.parse_args()

    searchAndRename(args)


if __name__ == "__main__":
    main()
