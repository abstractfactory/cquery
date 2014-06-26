"""cQuery command-line interface

The cli is designed to help construct a hierarchy and to
debug potential issues when doing the same through code
would take too long.

Example:
    $ cd /projects/spiderman/assets/Peter/animLow
    $ cquery .Asset
    /projects/spiderman/assets/Peter
    $ cquery .Project
    /projects/spiderman

"""

import os
import cquery

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('selector')
parser.add_argument('--direction', default='down')
parser.add_argument('--verbose', action='store_true', default=True)
parser.add_argument('--first', action='store_true', default=False)

args = parser.parse_args()

if args.direction == 'down':
    direction = cquery.DOWN
elif args.direction == 'up':
    direction = cquery.UP
else:
    print "Error: direction must be either up or down"

try:
    for result in cquery.matches(root=os.getcwd(),
                                 selector=args.selector,
                                 direction=direction):

        if args.verbose is True:
            print "  {}".format(result)

        if args.first is True:
            break

except KeyboardInterrupt:
    pass