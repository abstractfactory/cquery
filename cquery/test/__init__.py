"""Default test suite."""

import os
import cquery
import shutil
import tempfile
import unittest


class BaseTest(unittest.TestCase):
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
        cquery.tag(root_path, '.Root')
        cquery.tag(project_path, '.Project')

        # Setup assets
        root = os.path.join(project_path, "assets")

        for asset in assets:
            path = os.path.join(root, asset)
            os.makedirs(path)
            cquery.tag(path, ".Asset")

            if asset == 'Peter':
                cquery.tag(path, '.Hero')
                cquery.tag(path, "#Spidey")

            if asset == 'Goblin':
                cquery.tag(path, '.Villain')

        # Setup sub-assets
        root = os.path.join(project_path, "assets", "Peter")
        for subasset in subassets:
            path = os.path.join(root, subasset)
            os.makedirs(path)
            cquery.tag(path, ".Asset")

        # Setup shots
        root = os.path.join(project_path, "shots")

        for shot in xrange(shots_count):
            shot = str(shot + 1).ljust(4, "0")
            path = os.path.join(root, shot)
            os.makedirs(path)
            cquery.tag(path, ".Shot")

            if shot == '1000':
                cquery.tag(path, "#Intro")

            if shot == '2000':
                cquery.tag(path, "#Prelude")

            if shot == '5000':
                cquery.tag(path, "#Extro")

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


class QueryTest(BaseTest):
    """Test queries

    .. note:: This doesn't make any new tags or alter the file-system
        in any way.

    """

    def test_selector(self):
        count = 0
        for match in cquery.matches(self.root_path, ".Asset"):
            assert isinstance(match, basestring)
            count += 1

        assert count == len(self.assets + self.subassets), count

    def test_nonexisting_root(self):
        nonexisting_path = "not exist"
        assert not os.path.exists(nonexisting_path)
        result = cquery.first_match(root=nonexisting_path, selector=".Asset")
        assert result is None

    def test_invalid_argument_count(self):
        with self.assertRaises(TypeError):
            cquery.first_match(
                root="not exist",
                selector=".Asset",
                direction=cquery.DOWN,
                notexist=10)

    def test_id(self):
        result = cquery.first_match(self.project_path, '#Spidey')
        supposed_path = os.path.join(self.project_path, 'assets', 'Peter')
        self.assertEquals(result, supposed_path)

    def test_class(self):
        result = cquery.first_match(self.project_path, '.Villain')
        supposed_path = os.path.join(self.project_path, 'assets', 'Goblin')
        self.assertEquals(result, supposed_path)

    def test_has_class(self):
        for asset in ['Peter', 'Goblin']:
            path = os.path.join(self.project_path, 'assets', asset)
            self.assertTrue(cquery.has_class(path, '.Asset'))

    def test_has_id(self):
        asset = os.path.join(self.project_path, 'assets', 'Peter')
        self.assertTrue(cquery.has_id(asset, '#Spidey'))

    def test_depth_0(self):
        """A depth of 0 means to only look at the given `root` directory"""
        root = os.path.join(self.project_path, 'assets', 'Peter')
        matches = list()

        # At a depth of 0, this should only return Peter which
        # is the asset we are querying.
        for match in cquery.matches(root, '.Asset'):
            matches.append(match)

        self.assertTrue(len(matches), 1)

    def test_depth_1(self):
        matches = list()
        for match in cquery.matches(self.root_path,
                                    '.Asset',
                                    depth=1):
            matches.append(match)
        self.assertEqual(matches, list())

    def test_root_as_file(self):
        """Pass in an existing file as `root` argument"""
        with self.assertRaises(OSError):
            cquery.first_match(self.filepath, '.TestRootAsFile')

    def test_up_direction(self):
        """Query asset for its associated project"""
        asset = os.path.join(self.project_path, 'assets', 'Peter')
        match = cquery.first_match(asset, '.Project', direction=cquery.UP)
        self.assertEquals(match, self.project_path)

        # With insufficient depth, a match should not be found
        match = cquery.first_match(asset, '.Project',
                                   direction=cquery.UP,
                                   depth=1)
        self.assertEquals(match, None)

    def test_up_nonexisting(self):
        """Look for a tag that doesn't exist, upwards"""
        match = cquery.first_match(self.root_path, '.NotExist')
        self.assertEquals(match, None)

    def test_invalid_direction(self):
        with self.assertRaises(ValueError):
            cquery.first_match(self.root_path, '.Test', direction='invalid')


class TagTest(BaseTest):
    """Test tagging

    .. note:: This modifies the hierarchy with additional tags.

    """

    def test_class_tag(self):
        cquery.tag(self.project_path, ".TestClassTag")
        results = list()
        for match in cquery.matches(self.root_path,
                                    ".TestClassTag"):
            results.append(match)

        assert len(results) == 1

    def test_tag_nonexisting_path(self):
        with self.assertRaises(cquery.RootExists):
            cquery.tag("not exist", ".TestNotExist")

    def test_tag_existing_tag(self):
        """A tag has already been applied"""
        cquery.tag(self.project_path, ".TestingExisting")
        with self.assertRaises(cquery.TagExists):
            cquery.tag(self.project_path, ".TestingExisting")

    def test_detag(self):
        """Ensure detagging physically removes the file from disk"""
        tag = ".NewTag"
        cquery.tag(self.project_path, tag)

        tag_path = cquery.qualify(tag)
        tag_path = os.path.join(self.project_path, tag_path)
        assert os.path.isfile(tag_path)

        cquery.detag(self.project_path, tag)
        assert not os.path.exists(tag_path)

    def test_detag_nonexisting(self):
        """Trying to detag a tag that doesn't exist"""
        with self.assertRaises(cquery.TagExists):
            cquery.detag(self.project_path, ".NotExist")

    def test_detag_rootmissing(self):
        """The given path doesn't exist"""
        with self.assertRaises(cquery.RootExists):
            cquery.tag("not exist", ".TestNotExist")

        with self.assertRaises(cquery.RootExists):
            cquery.detag("not exist", ".TestNotExist")

    def test_tag_id(self):
        """Creating a tag that didn't previously exist"""
        tag = "#NewID"
        cquery.tag(self.project_path, tag)

        tag_path = cquery.qualify(tag)
        tag_path = os.path.join(self.project_path, tag_path)
        assert os.path.isfile(tag_path)

        cquery.detag(self.project_path, tag)
        assert not os.path.exists(tag_path)


if __name__ == '__main__':
    import nose
    nose.run()
