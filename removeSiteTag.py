#! /usr/bin/env python
"""
Removes site tags (like DDLValley.net) from the beginning of your files. This
script is intended to use with pyLoad.
"""

import os
import re
import argparse

# the list of tags to search for
TAGS = [
    r'(DDLValley\.(eu|net|org|com)_)(.*)'
]

# default directory to search in
DIR = '~/Downloads/'


def search_and_rename(path, args):
    """Search for matching filenames and remove the matched pattern."""
    for fCandidate in os.listdir(path):
        if not os.path.isfile(path+fCandidate):
            if args.verbose:
                print "Skip '{0}', is not a file.".format(fCandidate)
            continue

        for tag in TAGS:
            match = re.search(tag, fCandidate)
            if match:
                oldFilePath = path+fCandidate
                newFilePath = path+match.group(3)
                if not args.dry_run:
                    os.rename(oldFilePath, newFilePath)
                if args.verbose:
                    print "Rename '{0}' -> '{1}'".format(
                        fCandidate, match.group(3))


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

    for path in args.paths:
        path = os.path.expanduser(path)
        if args.verbose:
            print "Searching in path '{0}'".format(path)
        search_and_rename(path, args)


if __name__ == "__main__":
    main()
