# Standard library
import os
import errno
import shutil
import tempfile
import unittest

# cQuery library
import cquery


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
        >>> tag(r"c:\users\marcus", ".User")
        True
        >>> detag(r"c:\users\marcus", ".User")
        True

    """

    selector = convert(selector)

    if not os.path.exists(root):
        raise cquery.RootExists("{} did not exist".format(root))

    container = os.path.join(root, cquery.CONTAINER)
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
            raise cquery.TagExists("Error: Tag already exists. "
                                   "Use --detag to remove existing tag.")
        raise

    return True


class BaseCQueryTestCase(unittest.TestCase):
    def setUp(self):
        """Establish fixture for tests

        Each test will get run against the same fixture. The fixture
        is setup and teared down per run and per test-class.

        Fixture:
            / .Root
                projects/
                    spiderman/ .Project
                        assets/
                            Peter .Asset .Hero #Spidey
                                lowAnim .Asset .Animation .Rig
                                highAnim .Asset .Animation .Rig
                            Mary .Asset
                            Goblin .Asset .Villain
                            Spidey .Asset
                            Harry .Asset
                            Ben .Asset
                            a_long_filename.txt
                        shots/
                            1000 .Shot #Intro
                            2000 .Shot #Prelude
                            3000 .Shot
                            4000 .Shot
                            5000 .Shot #Extro

        """

        root_path = tempfile.mkdtemp()
        project_path = os.path.join(root_path, "projects", "spiderman")
        shots_count = 5
        assets = [
            'Peter',
            'Mary',
            'Goblin',
            'Spidey',
            'Harry',
            'Ben'
        ]

        subassets = [
            'animLow',
            'animHigh'
        ]

        os.makedirs(project_path)
        tag(root_path, '.Root')
        tag(project_path, '.Project')

        # Setup assets
        root = os.path.join(project_path, "assets")

        for asset in assets:
            path = os.path.join(root, asset)
            os.makedirs(path)
            tag(path, ".Asset")

            if asset == 'Peter':
                tag(path, '.Hero')
                tag(path, "#Spidey")

            if asset == 'Goblin':
                tag(path, '.Villain')

        # Setup sub-assets
        root = os.path.join(project_path, "assets", "Peter")
        for subasset in subassets:
            path = os.path.join(root, subasset)
            os.makedirs(path)
            tag(path, ".Asset")

        # Setup shots
        root = os.path.join(project_path, "shots")

        for shot in xrange(shots_count):
            shot = str(shot + 1).ljust(4, "0")
            path = os.path.join(root, shot)
            os.makedirs(path)
            tag(path, ".Shot")

            if shot == '1000':
                tag(path, "#Intro")

            if shot == '2000':
                tag(path, "#Prelude")

            if shot == '5000':
                tag(path, "#Extro")

        # Create file
        filepath = os.path.join(project_path, 'assets', 'a_long_filename.txt')
        f = open(filepath, 'w')
        f.close()

        # Store references
        self.root_path = root_path
        self.project_path = project_path
        self.assets = assets
        self.subassets = subassets
        self.shots_count = shots_count
        self.filepath = filepath

        assert os.path.isdir(os.path.join(
            root_path,
            "projects/spiderman/assets/Peter/animLow"))
        assert os.path.isdir(os.path.join(
            root_path,
            "projects/spiderman/shots/1000"))

    def tearDown(self):
        shutil.rmtree(self.root_path)


if __name__ == '__main__':
    import nose
    nose.run()
