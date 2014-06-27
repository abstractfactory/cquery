
.. _quickstart:

Quickstart
==========

This page will guide you through setting up cQuery and running your first query.

Install
-------

.. note:: Both cQuery and Open Metadata are pure-Python libraries and as such will require an installation of `Python`_. Tested on 2.7.7.

.. code-block:: bash

    $ pip install git+https://github.com/abstractfactory/openmetadata
    $ pip install git+https://github.com/abstractfactory/cquery

Command-line
------------

To run cQuery from a command-line, we’ll expose it to the console.

For Windows
~~~~~~~~~~~

Save this file somewhere in your PATH so that it can be accessed via a command-line.

**cquery.bat**

.. code-block:: bash

    @echo off
    python -m cquery %* --verbose

For Unix
~~~~~~~~

**cquery**

.. code-block:: bash

    $ to be continued

cQuery will install its executable automatically sometime in the future, I’m just not sure how to go about it at the moment. Does anyone have any experience with this? Let us know!

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