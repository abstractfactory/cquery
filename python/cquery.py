#!python

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


def query(selector, direction='down', verbose=False):
    matches = list()

    # By Class
    if selector.startswith("."):
        selector = os.path.join(CONTAINER, selector[1:] + '.class')

    # By ID
    elif selector.startswith("#"):
        selector = os.path.join(CONTAINER, selector[1:] + '.id')

    # By Name
    else:
        selector = os.path.join(CONTAINER, selector)

    if direction == 'down':
        for root, _, _ in os.walk(os.getcwd()):
            if os.path.basename(root).startswith("."):
                continue

            path = os.path.join(root, selector)
            if os.path.exists(path):
                matches.append(root)
                if verbose:
                    print "  {}".format(root)

    elif direction == 'up':
        root = os.getcwd()
        while True:
            path = os.path.join(root, selector)
            if os.path.exists(path):
                matches.append(path)
                if verbose:
                    print "  {}".format(root)

            old_root = root
            root = os.path.dirname(root)
            if root == old_root:
                # Top-level reached
                break

    return matches


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('selector')
    parser.add_argument('--direction', default='down')
    parser.add_argument('--verbose', action='store_true', default=False)

    args = parser.parse_args()

    query(selector=args.selector,
          direction=args.direction,
          verbose=args.verbose)
