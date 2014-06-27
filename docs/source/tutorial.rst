Tutorial
========

This page is meant as a more thourough version of the :doc:`quickstart`. If you haven't been through it yet, it is recommended that you do so before proceeding.

Process
-------

cQuery is meant to be simple and to depend on as little knowledge and setup as possible. As such, to get started with cQuery there are three steps to fulfill:

1. Install cQuery
2. Tag content
3. Query content

Once set up, a more general workflow may look like this:

1. Tag content
2. Query content
   
Tagging is performed via Open Metadata - a decentralised metadata storage and retrieval library for Python.

Installation
------------

The algorithm used by cQuery is minimal and simple and although we use Open Metadata to associate metadata to folders we with to include in a query, Open Metadata doesn't quite get to flex its muscles at the moment as queries only cover plain names of files (<name>.class and <name>.id specifically) however the plan is to expose cQuery to all of what Open Metadatas has to offer. To allow users to query not only names but contents of files; be it plain text documents, stereoscopic images or complex 3d geometry.

To get started, install Open Metadata and cQuery like this:

.. code-block::bash
    $ pip install git+https://github.com/abstractfactory/openmetadata
    $ pip install git+https://github.com/abstractfactory/cquery.git


Setup
-----

cQuery is designed as a Python library and although the plan is to involve other languages too, we'll set it up so that you can work with it via the command-line. That way we can play around with cQuery and get a feel for its potential.

The plan is to have cQuery be available via PyPI and come with its own platform-independent executable. But until then, we will construct our own.

The cQuery Python package is designed to be used as a Command-line Interface (cli), so all we need to do is expose this to a command-line.

Windows
~~~~~~~

Save this file somewhere in your PATH so that it can be accessed via a command-line.

**cquery.bat**

.. code-block:: bash

    @echo off
    python -m cquery %* --verbose

Content
-------

cQuery is designed to work with tens of millions of subdirectories but for the purposes of this tutorial, let's stick with a minimal set of possible matches.

.. code-block:: bash

    $ cd c:/projects
    $ mkdir spiderman/assets/Peter
    $ mkdir spiderman/assets/Goblin

    $ mkdir spiderman/shots/1000
    $ mkdir spiderman/shots/2000


Advanced
--------

.. note:: The following is on the roadmap for cQuery but isn't part of it yet. We are looking for contributors interested in file-based search optimisations - if that's you, contact us. If you know anyone, spread the word.

cQuery is designed to facilitate very large content hierarchies (> 20 million individual directories) and as such provides a few alternatives for optimisation.

No Optimisations
~~~~~~~~~~~~~~~~

Per default, cQuery is designed to work out-of-the-box with little or no setup. This means making every query live and will in some cases be cause for a noticable slowdown depending on the amount of directories are involved in a query. For upwards queries, this is usually not noticeable (~0.001s/level) but downwards queries could potentially touch millions of targets and as such may take several minutes to complete.

Local Daemon
~~~~~~~~~~~~~~

The simplest level of optimisation is one that indexes results during a query. Once a query has been performed, the results are stored in the currently running process and help speed up subsequent queries.

Dedicated Daemon
~~~~~~~~~~~~~~~~~~

The next level of optimistation involves running a dedicated daemon that performs an either live, at a fixed interval or at events. The dedicated daemon has the advantage of being persistent across runs and facilitating a multi-user setup.

Central Deamon
~~~~~~~~~~~~~~

Finally, the central deamon, like the dedicated daemon, is persistent but as opposed to the dedicated deamon the central daemon facilitates a multi-user/multi-site usage.


.. _cquery.py: https://github.com/abstractfactory/cquery/blob/master/python/cquery.py