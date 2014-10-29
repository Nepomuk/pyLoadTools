#! /usr/bin/env python
"""
Removes site tags (like DDLValley.net) from the beginning of your files. This
script is intended to use with pyLoad.
"""

import os
import re
import argparse
import logging

# The list of tags to search for. The characters within the group named 'keep'
# will be kept.
TAGS = [
    r'(DDLValley\.(eu|net|org|com|rocks)_)(?P<keep>.*)'
]

# default log file
LOGFILE = 'removeSiteTag.log'


def check_path_candidate(pathCandidate):
    """Check the path candidate and put it into a proper format."""
    pathCandidate = os.path.expanduser(pathCandidate)
    if os.path.exists(pathCandidate) and os.path.isdir(pathCandidate):
        # for some reason it doesn't work if there is a trailing slash
        if pathCandidate.endswith('/'):
            return pathCandidate[:-1]
        else:
            return pathCandidate

    return None


def get_paths_to_search_in(args):
    """Gather the paths passed by arguments, check if they exist and expand
    user directories."""
    paths = []

    # first the argument from pyLoad
    if len(args.pyload) > 2:
        pathCandidate = check_path_candidate(args.pyload[1])
        if pathCandidate:
            paths.append(pathCandidate)

    # now the user defined ones
    if args.paths:
        for path in args.paths:
            pathCandidate = check_path_candidate(path)
            if pathCandidate:
                paths.append(pathCandidate)

    return paths


def search_and_rename(path, args):
    """Search for matching filenames and remove the matched pattern."""
    for fCandidate in os.listdir(path):
        oldFilePath = os.path.join(path, fCandidate)
        if not os.path.isfile(oldFilePath):
            if args.verbose:
                print "Skip '{0}', is not a file.".format(fCandidate)
            continue

        # download in progress
        if re.search(r'chunk(s|\d+)$', fCandidate):
            if args.verbose:
                print "Skip '{0}', download in progress.".format(fCandidate)
            continue

        for tag in TAGS:
            match = re.search(tag, fCandidate)
            if match:
                newFilePath = os.path.join(path, match.group('keep'))
                if not args.dry_run:
                    os.rename(oldFilePath, newFilePath)
                if args.verbose:
                    print "Rename '{0}' -> '{1}'".format(
                        fCandidate, match.group('keep'))
                if args.logging:
                    logging.debug("Rename '{0}' -> '{1}'".format(
                        fCandidate, match.group('keep')))


def main():
    """The main function that is called automatically."""
    parser = argparse.ArgumentParser(
        description='Search for files containing a certain tag and remove it.')
    parser.add_argument(
        "pyload", metavar='pyload-arg',
        type=str, nargs='*',
        help="The arguments coming from pyLoad.")
    parser.add_argument(
        "--paths", metavar='path',
        type=str, nargs='*',
        help="The directories to search in. Default: Just the second argument passed over from pyload.")
    parser.add_argument(
        '-n', '--dry-run',
        action='store_true',
        help="Don't change anything.")
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help="Verbose output.")
    parser.add_argument(
        '-l', '--logging',
        action='store_true',
        help="Activate log output.")
    parser.add_argument(
        '-L', '--log-file',
        type=str, default=LOGFILE,
        help="Choose log file name, default: {0}".format(LOGFILE))
    args = parser.parse_args()

    if args.logging:
        logging.basicConfig(
            filename='removeSiteTag.log',
            level=logging.DEBUG,
            format='%(asctime)s  %(message)s')
        logging.debug("==== Running script =====")
        for arg, val in vars(args).iteritems():
            logging.debug("Argument {0}={1}".format(arg, val))

    paths = get_paths_to_search_in(args)

    for path in paths:
        if args.verbose:
            print "Searching in path '{0}'".format(path)
        if args.logging:
            logging.debug("Searching in path '{0}'".format(path))
        search_and_rename(path, args)


if __name__ == "__main__":
    main()
