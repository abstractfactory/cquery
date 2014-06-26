"""cQuery Prototype

Usage:
    There are two methods of filtering content:
        1. By Class
        2. By ID

    To return all contained folders with class "Asset":
    $ cquery .Asset

    To return the contained unique folder with ID "MyFolder":
    $ cquery #MyFolder

    To search up-wards for the closest folder with class "Project":
    $ cquery .Project --direction=up

"""

import os
import openmetadata as om


def cquery(selector, direction='down', verbose=False):
    matches = list()

    # Classes
    if selector.startswith("."):
        selector = selector[1:] + '.class'

    # IDs
    elif selector.startswith("#"):
        selector = selector[1:] + '.id'

    else:
        print "Error: Must specify either Class . or ID #"
        return

    if direction == 'down':
        for root, folders, _ in os.walk(os.getcwd()):
            for folder in folders:
                if folder.startswith("."):
                    continue

                path = os.path.join(root, folder)

                if om.find(path, selector):
                    matches.append(path)
                    if verbose:
                        print "  {}".format(path)

    elif direction == 'up':
        root = os.getcwd()
        while True:
            if om.find(root, selector):
                matches.append(path)
                if verbose:
                    print root

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

    args = parser.parse_args()

    cquery(selector=args.selector, direction=args.direction)
