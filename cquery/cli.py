"""cQuery command-line interface

The cli is designed to help construct a hierarchy and to
debug potential issues when doing the same through code
would take too long.

This module is generally accessed via :mod:`__main__.py` but can
also be imported and used via Python - e.g. for integration with
other command-line interfaces.

"""

# Standard library
import os
import time
import argparse

# Local library
import cquery

parser = argparse.ArgumentParser()
parser.add_argument('selector', help="CSS3-compliant selector")
parser.add_argument('--tag',
                    action='store_true',
                    default=False,
                    help="Tag `root` with metadata matching this selector")
parser.add_argument('--detag',
                    action='store_true',
                    default=False,
                    help="Detag `root` from metadata matching this selector")
parser.add_argument('--root',
                    default=None,
                    help="Absolute or relative path to query root"
                         " (defaults to the working directory")
parser.add_argument('--direction', default='down',
                    help=("Search either up through a hierarchy,"
                          "or down across the full subtree"))
parser.add_argument('--verbose',
                    action='store_true',
                    default=True,
                    help="Print additional information about query")
parser.add_argument('--first',
                    action='store_true',
                    default=False,
                    help="Only return a first match")


def cli(selector,
        root=None,
        tag=False,
        detag=False,
        direction='down',
        verbose=False,
        first=False):

    """Command-line interface interpreter

    Arguments:
        selector (str): CSS3 compliant selector
        direction (enum): Up, down or none, search direction of query
        verbose (bool): Output additional information about the query
        first (bool): Only output a first result

    Example:

    .. code-block:: bash

        $ # Tag content with Classes and an ID, and then query them.
        $ cd /projects/spiderman
        $ cquery --class=Asset --root=assets/Peter
        $ cquery --class=Asset --root=assets/Harry
        $ cquery --class=Shot --root=shots/1000
        $ cquery --id=Spidey --root=assets/Peter
        $ cquery .Asset
        /projects/spiderman/assets/Peter
        /projects/spiderman/assets/Harry
        $ cquery .Project --direction=up
        /projects/spiderman


    """

    if tag and detag:
        print "Error: tag and detag flags must be mutually exclusive"
        return

    root = root

    if root:
        root = os.path.abspath(root)
    else:
        root = os.getcwd()

    if direction == 'down':
        direction = cquery.DOWN
    elif direction == 'up':
        direction = cquery.UP
    elif direction == 'none':
        direction = cquery.NONE
    else:
        print "Error: direction must be either up, down or none"

    if not (tag or detag):
        try:
            results = list()
            clock = time.clock()
            for result in cquery.matches(root=root,
                                         selector=selector,
                                         direction=direction):

                if verbose is True:
                    print "{}".format(result)
                    results.append(result)

                if first is True:
                    break

            if verbose:
                print ""
                print " Querying directory of {}".format(root)
                print "\t\tSelector {}".format(selector)
                print "\t\t%i results in %fs" % (len(results),
                                                 time.clock()-clock)

        except KeyboardInterrupt:
            pass

    elif tag:
        try:
            cquery.tag(root, selector)
        except (cquery.TagExists, cquery.RootExists) as e:
            print "Error: {}".format(e)

    elif detag:
        try:
            cquery.detag(root, selector)

        except (cquery.TagExists, cquery.RootExists) as e:
                print "Error: {}".format(e)


def main():
    args = parser.parse_args()
    cli(selector=args.selector,
        root=args.root,
        tag=args.tag,
        detag=args.detag,
        direction=args.direction,
        verbose=args.verbose,
        first=args.first)


if __name__ == '__main__':
    main()
