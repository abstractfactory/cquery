"""cQuery - Content Object Model traversal.

Attributes:
  CONTAINER (str): Metadata storage prefix
    Metadata associated with directories are prefixed
    with a so-called "container". In Open Metadata land, this means an
    additional directory by the name of `~openmetadata.Path.CONTAINER`

  UP (flag): Search direction
    A flag for :func:`cquery.matches` specifying that the content
    traversal should proceed up from the `root` directory. Use this to
    retrieve a hierarchy of matches.

  DOWN (flag): Search direction
    The opposite of the above UP. Use this to retrieve
    multiple matches within a given hierarchy, located under `root`

"""

import os
import errno

__all__ = [
    'NONE',
    'UP',
    'DOWN',
    'tag',
    'detag',
    'matches',
    'qualify',
    'has_class',
    'has_id',
    'first_match',
    'convert',
    'TagExists',
    'RootExists',
    'CONTAINER'
]

# As per the Open Metadata RFC
# http://rfc.abstractfactory.io/spec/10/
CONTAINER = ".meta"

# Directions
NONE = 1 << 0
UP = 1 << 1
DOWN = 1 << 2


class TagExists(OSError):
    """Raised when a selector either exists or does not exist"""


class RootExists(OSError):
    """Raised when a root either exists or does not exist"""


def has_class(root, selector):
    """Test absolute path `root` for class `selector`

    Returns:
        True if `root` has been tagged with class `selector` else False

    """

    return True if first_match(root, selector) is not None else False


def has_id(root, selector):
    """Test absolute path `root` for id `selector`

    Returns:
        True if `root` has been tagged with id `selector` else False

    """

    return True if first_match(root, selector) is not None else False


def tag(root, selector):
    """Tag absolute path `root` with selector `selector`

    This function physically tags a directory with metadata
    relevant for queries.

    Arguments:
        root (str): Absolute path at which to write
        selector (str): CSS3-compliant selector

    Returns:
        status (bool): True if success

    Raises:
        TagExists: If selector `selector` already exists.
        RootExists: If root does not exist

    Example:
        >>> import tempfile
        >>> root = tempfile.mkdtemp()
        >>> tag(root, ".User")
        True
        >>> detag(root, ".User")
        True

    """

    selector = convert(selector)

    if not os.path.exists(root):
        raise RootExists("{} did not exist".format(root))

    container = os.path.join(root, CONTAINER)
    if not os.path.exists(container):
        os.makedirs(container)

    path = os.path.join(container, selector)

    # Use os.open() as opposed to __builtin__.open()
    # due to support for low-level flags. This only
    # creates a new file if no file already exists.
    try:
        f = os.open(path, os.O_CREAT | os.O_EXCL)
        os.close(f)
    except OSError as e:
        if e.errno == errno.EEXIST:
            raise TagExists("%s already exists." % selector)
        raise

    return True


def detag(root, selector):
    """Detag selector `selector` from absolute path `root`

    This function is the inverse of :func:`tag` and in effect
    removes a tag from the given directory.

    Precondition:
        Selector must exists within root

    Returns:
        status (bool): True if successful, False otherwise

    Raises:
        TagExist: If selector `selector` at absolute path `root`
            does not exists.

    Example:
        >>> import tempfile
        >>> root = tempfile.mkdtemp()
        >>> tag(root, ".User")
        True
        >>> detag(root, ".User")
        True

    """

    if not os.path.exists(root):
        raise RootExists("Root did not exist")

    selector = convert(selector)

    container = os.path.join(root, CONTAINER)
    path = os.path.join(container, selector)

    try:
        os.remove(path)
    except OSError as e:
        if e.errno == errno.ENOENT:
            raise TagExists("%s does not exist." % selector)
        raise

    return True


def convert(selector):
    """Convert CSS3 selector `selector` into compatible file-path

    Arguments:
        selector (str): CSS3 selector, e.g. .Asset

    Returns:
        str: Resolved selector

    Example:

    .. code-block:: bash

        $ .Asset  --> Asset.class
        $ #MyId   --> MyId.id

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


def qualify(selector):
    """Return fully-qualified selector from `selector`

    This function converts `selector` into an a searchable
    relative path for :func:`matches`

    Arguments:
        selector (str): CSS3-compliant selector

    Returns:
        path (str): Relative path to selector within a root directory

    Example:
        >>> import os
        >>> path = qualify('.Asset')
        >>> if os.name == 'nt':
        ...     assert path == ".meta\\Asset.class"
        ... else:
        ...     assert path == ".meta/Asset.class"

    """

    return os.path.join(CONTAINER, convert(selector))


def matches(root, selector, direction=DOWN, depth=-1):
    """Yield matches at absolute path `root` for selector `selector`
    given the direction `direction`.

    When looking for a first match only, use :func:`first_match`

    Arguments:
        root (str): Absolute path from which where to start looking
        selector (str): CSS3-compliant selector, e.g. ".Asset"
        direction (enum, optional): Search either up or down a hierarchy
        depth (int): Depth of traversal; a value of -1 means infinite

    Yields:
        path (str): Absolute path of next match.

    Attributes:
        errors: Collection of errors occured during os.walk (NotImplemented)

    Raises:
        OSError: ENOTDIR is raised if path `root` is not a directory

    Example:
        >>> import os
        >>> paths = list()
        >>> for match in matches(os.getcwd(), ".Asset"):
        ...     paths.append(match)

    """

    assert isinstance(direction, int)

    if os.path.exists(root) and not os.path.isdir(root):
        raise OSError(errno.ENOTDIR, "{} is not a directory".format(root))

    errors = list()
    selector = qualify(selector)

    def error_collector(exception):
        errors.append(exception)

    if direction & DOWN:
        for base, dirs, _ in os.walk(root,
                                     topdown=True,
                                     onerror=error_collector):
            if os.path.basename(base).startswith("."):
                continue

            if depth >= 0:
                head = base[len(root)+len(os.path.sep) - 1:]
                level = head.count(os.path.sep)
                if level >= depth:
                    dirs[:] = []  # Don't recurse any deeper

            path = os.path.join(base, selector)
            if os.path.isfile(path):
                yield base

    elif direction & UP:
        level = 0
        while True:
            path = os.path.join(root, selector)
            if os.path.isfile(path):
                yield root

            old_root = root
            root = os.path.dirname(root)

            if depth >= 0:
                level += 1
                if level >= depth:
                    break

            if root == old_root:
                # Top-level reached
                break

    elif direction & NONE:
        path = os.path.join(root, selector)
        if os.path.isfile(path):
            yield root

    else:
        raise ValueError("Direction not recognised: %s" % direction)


def first_match(root, selector, direction=DOWN, depth=-1):
    """Convenience function for returning a first match from :func:`matches`.

    Arguments:
        root (str): Absolute path from which where to start loo
        selector (str): CSS-style selector, e.g. .Asset
        direction (enum): Search either up or down a hierarchy

    Returns:
        path (str): Absolute path if successful, None otherwise.

    Example:
        >>> import os
        >>> path = first_match(os.getcwd(), ".Asset")

    """

    try:
        return next(matches(root=root,
                            selector=selector,
                            direction=direction,
                            depth=depth))
    except StopIteration:
        return None


if __name__ == '__main__':
    import doctest
    doctest.testmod()
