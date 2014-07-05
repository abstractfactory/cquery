"""Brute-force approach to indexing, as per issue #2"""

import os
import re
import time
import fnmatch


class Node(object):
    """A Node represents a directory on disk

    Arguments:
        path (str): Absolute path to directory

    """

    @property
    def cls(self):
        pass

    @property
    def id(self):
        pass

    def __str__(self):
        return os.path.basename(self.path)

    def __repr__(self):
        return u"%s(%r)" % (type(self).__name__,
                            self.__str__())

    def __init__(self, path):
        self.path = path
        self._data = dict()

    def data(self, key):
        """Retrieve data about Node

        Arguments:
            key (str): Data is stored in a dict and this is its key

        """

        value = self._data.get(key)

        if not value:
            if key == 'basename':
                value = os.path.basename(self.path)

        return value


class Index(object):
    """Flat index of all directories within a hierarchy

    Arguments:
        root (str): Absolute path to use as starting point for index

    """

    def __iter__(self):
        pass

    def __init__(self, root):
        self.root = root
        self.store = dict()
        self.stats = dict()

    def find(self, pattern):
        """Find directory via regular expression

        Arguments:
            pattern (str): Regular expression

        Example:
            >>> # Find children of `/content`
            >>> find(r"/content/\w*$")

        """

        p = re.compile(pattern)
        for node in self.store:
            if p.match(node):
                yield node

    def listdir(self, root):
        """Convenience method of :meth:.find for listing children of `root`

        Arguments:
            root (str): Absolute path at which to list children

        """

        clock = time.clock()

        for match in self.find(root + "/\w*$"):
            print match

        print "\t\tTime taken: {}".format(time.clock() - clock)

    def walk(self, root):
        """Mimic os.walk"""
        raise NotImplemented

    def get(self, key):
        return self.store.get(key)

    def cquery(self, selector):
        """Re-implementation of cQuery

        cQuery is re-implemented rather than re-purposed due to
        the flatness of the dataset. It's difficult/suboptimal to
        do the depth-first walk as the original cQuery does with
        os.walk.

        """

        clock = time.clock()
        results = list()

        for path, node in self.store.iteritems():
            if selector.startswith("."):
                classes = node.data('class')
                if classes and selector[1:] in classes:
                    results.append(path)
                    print path

        print " Querying directory of {}".format(self.root)
        print "\t\tSelector {}".format(selector)
        print "\t\t{} results in {}s".format(len(results),
                                             time.clock() - clock)

    def stats(self):
        """Return statistics over indexed content

        Statistics:
            Number of each contained class
            Number of nodes
            Time to traverse everything
            Time to traverse a directory

        """

        raise NotImplemented

    def compute(self):
        """Traverse a hierarchy and record content with metadata

        Example:
            All non-hidden folders are stored alongside a Node
            for simplified access to potential metadata.

            >>> "/projects/spiderman/.meta/Project.class"

            This Node contains Node.data('class') == 'Project'

        """

        clock = time.clock()

        for base, dirnames, filenames in os.walk(self.root):
            for dirname in fnmatch.filter(dirnames, ".*"):
                dirnames.remove(dirname)

            for dirname in dirnames:
                path = os.path.join(base, dirname)
                node = Node(path)

                meta = os.path.join(path, '.meta')
                for _, _, files in os.walk(meta):
                    for basename in files:
                        try:
                            value, key = basename.split(".")
                            if not key in node._data:
                                node._data[key] = list()
                            node._data[key].append(value)

                        except ValueError:
                            pass

                relpath = os.path.relpath(path, self.root)
                relpath = "/" + relpath.replace("\\", "/")
                self.store[relpath] = node

        self.stats['timetaken'] = time.clock() - clock
        self.stats['count'] = len(self.store)


if __name__ == '__main__':
    ROOT = r"C:\studio"
    ROOT = r"C:\studio\content\jobs\test2"

    # index = Index(ROOT)
    # index.compute()
