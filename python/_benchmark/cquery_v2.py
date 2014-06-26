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
        for root, _, _ in os.walk(os.getcwd()):
            if os.path.basename(root).startswith("."):
                continue

            path = os.path.join(root, ".meta", selector)
            if os.path.exists(path):
                matches.append(root)
                if verbose:
                    print "  {}".format(path)

    elif direction == 'up':
        root = os.getcwd()
        while True:
            path = os.path.join(root, ".meta", selector)
            if os.path.exists(path):
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
    parser.add_argument('--verbose', action='store_true', default=False)

    args = parser.parse_args()

    cquery(selector=args.selector,
           direction=args.direction,
           verbose=args.verbose)
