
.. _quickstart:

Quickstart
==========

This page will guide you through setting up cQuery and running your first query. If you experience any problems here or are looking for more information about each step, head on the the :doc:`tutorial` for a full overview or :doc:`example` to experience a demo project.

Install
-------

.. code-block:: bash

    $ pip install git+https://github.com/abstractfactory/cquery

.. note:: cQuery is a pure-Python library and as such will require an installation of `Python`_.

.. note:: cQuery has been tested on Python 2.7.7 on Windows 8.1.

Some Content
------------

.. code-block:: bash

    $ cd c:/projects
    $ mkdir spiderman/assets/Peter
    $ mkdir spiderman/assets/Goblin

    $ mkdir spiderman/shots/1000
    $ mkdir spiderman/shots/2000

Tag
---

.. note:: cQuery ships with an executable. On Windows, you may have to add the Python27\\scripts directory to your PATH.

.. code-block:: bash

    $ cd spiderman/assets
    $ cquery Asset.class --tag --root=Peter
    $ cquery Asset.class --tag --root=Goblin
    $ cd ../shots
    $ cquery Shot.class --tag --root=1000
    $ cquery Shot.class --tag --root=2000

Query
-----

.. code-block:: bash

    $ cd ..
    $ cd ..
    $ cquery .Asset
    c:/projects/spiderman/assets/Peter
    c:/projects/spiderman/assets/Goblin

And that’s it. Now you can tag and query via the command-line.

Python
------

From Python, you could query like this:

.. code-block:: python

    import os

    import cquery
    for match in cquery.matches(os.getcwd(), selector='.Asset'):
        print match


Next we'll have a look at a more thorough version of this quickstart.

.. _`Python`: http://python.org