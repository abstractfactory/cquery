"""cQuery command-line interface"""


import os
import time
import errno

from . import lib as cquery
from .vendor import click


CWD = os.getcwd()
ROOTHELP = "Path relative the current working directory."
VERBOSE_TEMPLATE = """
Querying directory of {dir}
    Selector {sel}
    {num} results in {sec}s"""


@click.group()
@click.option("--verbose",
              is_flag=True,
              help="Display additional information when running commands")
@click.pass_context
def main(ctx, verbose):
    """Command-line interface of cQuery.

    cQuery is used to find and identify content on a file-system
    using CSS3-compliant selectors, such as class and id.

    Upon tagging, prefix the name of your tag with either a dot (.)
    or a hash (#) for class or identifier respectively.

    \b
    Usage:
        $ cd MyAsset
        $ cquery tag .Asset
        $ cquery search .Asset
        /path/to/MyAsset

    """

    ctx.obj['verbose'] = verbose


@click.command()
@click.argument("selector")
@click.option("-r", "--root", default=CWD, help=ROOTHELP)
@click.pass_context
def tag(ctx, selector, root):
    """Tag root with selector.

    Given a CSS3-compliant selector, tag the current working directory,
    overridden by root

    """

    root = os.path.abspath(root)

    try:
        cquery.tag(root, selector)
    except (cquery.TagExists, cquery.RootExists) as e:
        print "Error: %s" % e


@click.command()
@click.argument("selector")
@click.option("-r", "--root")
@click.pass_context
def detag(ctx, selector, root):
    root = os.path.abspath(root)

    try:
        cquery.detag(root, selector)
    except (cquery.TagExists, cquery.RootExists) as e:
            print "Error: %s" % e


@click.command()
@click.argument("selector")
@click.option("-r", "--root", default=CWD, help=ROOTHELP)
@click.option("-d", "--depth", default=-1, help="Limit how many parents "
                                                "to look through")
@click.option("-f", "--first", default=True, help="Return first result")
@click.pass_context
def identify(ctx, selector, root, depth, first):
    """Query the current working directory.

    This command will traverse up through a hierarchy of directories in
    search for the selector until it finds a match.

    """

    root = os.path.abspath(root)

    try:
        results = list()
        clock = time.clock()
        try:
            for result in cquery.matches(root=root,
                                         selector=selector,
                                         direction=cquery.UP,
                                         depth=depth):

                print result
                results.append(result)

                if first is True:
                    break

        except OSError as e:
            if e.errno == errno.ENOTDIR:
                print e

        if ctx.obj.get('verbose'):
            print VERBOSE_TEMPLATE.format(
                dir=root,
                sel=selector,
                num=len(results),
                sec="%f" % (time.clock()-clock))
    except KeyboardInterrupt:
        print "Cancelled"


@click.command()
@click.argument("selector")
@click.option("-r", "--root", help=ROOTHELP)
@click.option("-d", "--depth", default=-1, help="Limit how deeply the "
                                                "search goes")
@click.option("-f", "--first", default=False, help="Return first result")
@click.pass_context
def search(ctx, selector, root, depth, first):
    """Search for all matches of selector.

    This command will look at the current working directory
    (overriden by --root) and traverse each level, depth-first
    in search for the given selector.

    """

    root = os.path.abspath(root)

    try:
        results = list()
        clock = time.clock()
        try:
            for result in cquery.matches(root=root,
                                         selector=selector,
                                         direction=cquery.DOWN,
                                         depth=depth):

                print result
                results.append(result)

                if first is True:
                    break

        except OSError as e:
            if e.errno == errno.ENOTDIR:
                print e

        if ctx.obj.get('verbose'):
            print VERBOSE_TEMPLATE.format(
                dir=root,
                sel=selector,
                num=len(results),
                sec="%f" % (time.clock()-clock))
    except KeyboardInterrupt:
        print "Cancelled"


main.add_command(tag)
main.add_command(detag)
main.add_command(identify)
main.add_command(search)
