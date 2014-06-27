"""cQuery - Content Object Model traversal with Open Metadata

Functions:
    matches (iterator): Iterate over matches
    first_match (str): Return first match from `matches`

Attributes:
  CONTAINER (str): Metadata storage prefix
    Metadata associated with directories are prefixed
    with a so-called "container". In Open Metadata land, this means an
    additional directory by the name of `~openmetadata.Path.CONTAINER`

  UP (flag): Search direction
    A flag for `~cquery.matches()` specifying that the content
    traversal should proceed up from the `root` directory. Use this to
    retrieve a hierarchy of matches.

  DOWN (flag): Search direction
    The opposite of the above UP. Use this to retrieve
    multiple matches within a given hierarchy, located under `root`

"""

import os
import openmetadata

__all__ = [
    'NONE',
    'UP',
    'DOWN',
    'matches',
    'first_match',
    'convert'
]

# Base-directory for Open Metadata contents (.meta)
CONTAINER = openmetadata.Path.CONTAINER

# Directions
NONE = 1 << 0
UP = 1 << 1
DOWN = 1 << 2


def convert(selector):
    """Convert CSS3 `selector` into Open Metadata-compatible path

    Example:
        .Asset  --> Asset.class
        #MyId   --> MyId.id

    """

    # By Class
    if selector.startswith("."):
        selector = selector[1:] + '.class'

    # By ID
    elif selector.startswith("#"):
        selector = selector[1:] + '.id'

    # By Name
    else:
        pass

    return selector


def matches(root, selector, direction=DOWN):
    """Main cQuery algorithm

    Arguments:
        root (str): Absolute path from which where to start looking
        selector (str): CSS-style selector, e.g. ".Asset"
        direction (enum, optional): Search either up or down a hierarchy

    Yields:
        Absolute path as str of next match.

        When only looking for a first match, it is recommended to use
        the convenience function `first_match` below.

    """

    selector = os.path.join(CONTAINER, convert(selector))

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

    elif direction & NONE:
        path = os.path.join(root, selector)
        if os.path.isfile(path):
            yield root

    else:
        raise ValueError("Direction not recognised: %s" % direction)


def first_match(root, selector, direction=DOWN):
    """Return first match from `matches()` above (convenience)

    Arguments:
        root (str): Absolute path from which where to start loo
        selector (str): CSS-style selector, e.g. .Asset
        direction (enum): Search either up or down a hierarchy

    Returns:
        Absolute path as str if successful, None otherwise.

    """

    try:
        return next(matches(root=root,
                            selector=selector,
                            direction=direction))
    except StopIteration:
        return None

