"""cQuery package interface

This module makes the cQuery package into an executable, via cli.py

"""

import cquery.cli

if __name__ == '__main__':
    args = cquery.cli.parser.parse_args()
    cquery.cli.main(selector=args.selector,
                    root=args.root,
                    tag=args.tag,
                    direction=args.direction,
                    verbose=args.verbose,
                    first=args.first)
