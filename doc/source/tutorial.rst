Tutorial
========

For this tutorial you will need cQuery, for queries, and Open Metadata for the manipulation of metadata.

Installing Open Metadata
------------------------

Open Metadata is an Open Source library for the association and manipulation of metadata for folders on a file-system. cQuery uses a certain class of metadata entries as predicates for it's queries; namely `<name>.class` and `<name>.id`

Installing cQuery
-----------------

Drop `cquery.py`_ into your a directory visible to Python, such as in your PYTHONPATH. Alternatively, you may use the Go version in which case you'll have to compile it.

.. _cquery.py: https://github.com/abstractfactory/cquery/blob/master/python/cquery.py