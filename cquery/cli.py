"""cQuery command-line interface

The cli is designed to help construct a hierarchy and to
debug potential issues when doing the same through code
would take too long.

Arguments:
    selector (str): CSS3 compliant selector
    direction (enum): Up, down or none, search direction of query
    verbose (bool): Output additional information about the query
    first (bool): Only output a first result

Example:
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

import os
import time
import cquery
import argparse
import openmetadata.cli

parser = argparse.ArgumentParser()
parser.add_argument('selector', help="CSS3 compliant selector")
parser.add_argument('--tag',
                    action='store_true',
                    default=False,
                    help="Tag `root` with selector")
parser.add_argument('--root',
                    default=None,
                    help="Absolute or relative path to query root"
                         " (defaults to the working directory")
parser.add_argument('--direction', default='down')
parser.add_argument('--verbose', action='store_true', default=True)
parser.add_argument('--first', action='store_true', default=False)


def main(selector,
         root=None,
         tag=False,
         direction='down',
         verbose=False,
         first=False):

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

    if not tag:
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

    else:
        # Write metadata
        selector = cquery.convert(selector)
        openmetadata.cli.main(selector, value=None, root=root)
