"""cQuery package interface

This module makes the cQuery package into an executable, via cli.py

"""

from . import cli


def main():
    cquery.cli.main(obj=dict(), prog_name="cquery")


if __name__ == '__main__':
    main()
