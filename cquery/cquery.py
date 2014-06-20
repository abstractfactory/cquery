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


def cquery(query, direction='down', silent=False):
    matches = list()

    # Classes
    if query.startswith("."):
        query = query[1:] + '.class'

    # IDs
    elif query.startswith("#"):
        query = query[1:] + '.id'

    else:
        print "Error: Must specify either Class . or ID #"
        return

    if direction == 'down':
        for root, folders, _ in os.walk(os.getcwd()):
            for folder in folders:
                if folder.startswith("."):
                    continue

                path = os.path.join(root, folder)

                if om.find(path, query):
                    matches.append(path)
                    if not silent:
                        print "  {}".format(path)

    elif direction == 'up':
        root = os.getcwd()
        while True:
            if om.find(root, query):
                matches.append(path)
                if not silent:
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
    parser.add_argument('query')
    parser.add_argument('--direction', default='down')

    args = parser.parse_args()

    cquery(query=args.query, direction=args.direction)
