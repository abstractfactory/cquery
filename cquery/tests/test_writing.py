"""Default test suite."""


import os
import cquery

import cquery.tests


class TestTagging(cquery.tests.BaseCQueryTestCase):
    """Test tagging, which modifies the hierarchy with additional tags"""

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
