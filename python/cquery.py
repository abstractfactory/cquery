"""cQuery - Content Object Model traversal with Open Metadata

cQuery supports three selectors; class, ID and name.
To search for a class, prefix your selector with a dot
(.). To do the equivalent but for an ID, use hash (#).
To search by name, do not include a prefix.

When searching by name, matches are returned via a
user-defined suffix, as opposed to the built-in class
and ID (.class and .id respectively).

For example, these two queries are identical
$ cquery .Female
$ cquery Female.class

Usage:
    To return all matches of class "Asset":
        $ cquery .Asset

    To return all matches of ID "MyFolder":
        $ cquery #MyFolder

    To return all matches of name "SomeFolder":
        $ cquery MyProperty.string

"""

import os
import openmetadata

# Base-directory for Open Metadata contents (.meta)
CONTAINER = openmetadata.Path.CONTAINER

# Directions
UP = 1 << 0
DOWN = 1 << 1


def matches(root, selector, direction=DOWN):
    """cQuery algorithm

    Arguments:
        root (str): Absolute path from which where to start looking
        selector (str): CSS-style selector, e.g. .Asset
        direction (enum): Search either up or down a hierarchy

    """

    # By Class
    if selector.startswith("."):
        selector = os.path.join(CONTAINER, selector[1:] + '.class')

    # By ID
    elif selector.startswith("#"):
        selector = os.path.join(CONTAINER, selector[1:] + '.id')

    # By Name
    else:
        selector = os.path.join(CONTAINER, selector)

    if direction & DOWN:
        for root, _, _ in os.walk(root):
            if os.path.basename(root).startswith("."):
                continue

            path = os.path.join(root, selector)
            if os.path.isfile(path):
                yield root

    elif direction & UP:
        while True:
            path = os.path.join(root, selector)
            if os.path.isfile(path):
                yield root

            old_root = root
            root = os.path.dirname(root)
            if root == old_root:
                # Top-level reached
                break
    else:
        raise ValueError("Direction not recognised: %s" % direction)


def first_match(root, selector, direction=DOWN):
    """Return first match from `matches()` above (convenience)"""

    try:
        return next(matches(root=root,
                            selector=selector,
                            direction=direction))
    except StopIteration:
        return None


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('selector')
    parser.add_argument('--direction', default='down')
    parser.add_argument('--verbose', action='store_true', default=False)
    parser.add_argument('--first', action='store_true', default=False)

    args = parser.parse_args()

    if args.direction == 'down':
        direction = DOWN
    elif args.direction == 'up':
        direction = UP
    else:
        print "Error: direction must be either up or down"

    for result in matches(root=os.getcwd(),
                        selector=args.selector,
                        direction=direction):

        if args.verbose is True:
            print "  {}".format(result)

        if args.first is True:
            break
