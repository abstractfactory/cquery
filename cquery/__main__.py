"""cQuery package interface

This module makes the cQuery package into an executable, via cli.py

"""

import cquery.cli


def main():
    cquery.cli.main(obj=dict(), prog_name="cquery")


if __name__ == '__main__':
    main()
