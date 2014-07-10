"""Default test suite."""

import os
import cquery
import cquery.tests


class TestQueries(cquery.tests.BaseCQueryTestCase):
    """Test making queries

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
        with self.assertRaises(AssertionError):
            # direction expects an integer, not passing an integer is a bug
            cquery.first_match(self.root_path, '.Test', direction='invalid')

        with self.assertRaises(ValueError):
            # cquery.UP, cquery.DOWN and cquery.NONE use flags between 0-2
            cquery.first_match(self.root_path, '.Test', direction=1 << 3)
