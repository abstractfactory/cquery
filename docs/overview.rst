Overview
========

cQuery is a library for metadata queries within a file-system, built to solve the issue of quickly finding and filtering content. It's designed to simplify the development of tools surrounding absolute paths on a file-system, without actually specifying absolute paths, but we're also looking into additional uses, such as a making it into a fully-fledged search engine.

How it works
------------

Given a directory such as:

.. code-block:: bash

    $ /projects/spiderman/assets/Peter/animLow

cQuery answers the questions:

    - What is my Asset?
    - What is my Project?
    - What rigs do I have?
    - Am I Orange?
    - How many shaders do I contain?

Quick example
-------------

Here is how it might look when tagging and querying a content hierarchy for a feature animation project.

.. code-block:: bash

    $ cd spiderman/assets
    $ cquery .Asset --tag --root=Peter
    $ cquery .Asset --tag --root=Goblin
    $ cd ../shots
    $ cquery .Shot --tag --root=1000
    $ cquery .Shot --tag --root=2000
    $ cd ..
    $ cd ..
    $ cquery .Asset
    c:/projects/spiderman/assets/Peter
    c:/projects/spiderman/assets/Goblin

Selectors
---------

The idea of selectors are adopted from CSS3 and its use in jQuery (from which the name cQuery was derived). jQuery allows users to operate on the Document Object Model, or DOM, using CSS3 selectors to locate the appropriate Nodes. Similarly, cQuery operates on the Content Object Model, or COM, using CSS3 selectors to locate the appropriate folders.

Up or Down
----------

Starting from a root directory, a query can either be made up or down. To find descending matches of a given directory, you would use DOWN. To instead query for ascending matches, you would use UP. To query one-self only, you would use NONE.

Here is how that might look when used in Python:

.. code-block:: python

    >>> # Find the associated project of the asset Peter
    >>> first_match("/projects/spiderman/assets/Peter",
    ...             selector='.Project', direction=UP)
    >>>
    >>> # Find all textures
    >>> for match in matches("/projects/spiderman/assets/Peter",
    ...             selector='.Texture', direction=DOWN):
    ...     print match
    >>>
    >>> # Is this asset a Hero?
    >>> True if first_match("/projects/spiderman/assets/Peter",
    ...                     selector='.Hero', direction=NONE) else False


Architecture
------------

cQuery works upon directories tagged with metadata to indicate its class, ID or name. The tagged directories may then be queried, either from outside a hierarchy looking in or from within a hierarchy looking out.

For tagging, cQuery uses the Open Metadata specification [1]_, the process is quite simple - for each subdirectory within a directory, recursively look for a file by name stored within the Open Metadata container. If a match is found, return the absolute path to said directory. The name of this file is the "selector" argument of your query.

Example:

.. code-block:: bash

    $ cquery .Asset  # Search for the file "Asset.class"

Performance
-----------

cQuery operates on the hard-drive and is a seek-only algorithm and as such doesn't perform any reads. Despite this however, disk-access is (seemingly) the prime bottle-neck. A cQuery prototype has been implemented in both Python and Go for performance comparisons, here are some results:

**Python**

.. code-block:: python

    # Scanning a hierarchy of 3601 items
    # 1 queries, 7 matches in 1.494072 seconds
    # 1 queries, 7 matches in 1.480471 seconds
    # 1 queries, 7 matches in 1.477589 seconds
    #   Average time/query: 1.484044 seconds

    # Scanning a hierarchy of 47715 items
    # 1 queries, 14 matches in 19.888399 seconds
    # 1 queries, 14 matches in 20.078811 seconds
    # 1 queries, 14 matches in 19.879660 seconds
    #   Average time/query: 19.948957 seconds

**Go**

.. code-block:: python

    # Scanning a hierarchy of 3601 items
    # 1 queries, 7 matches in 1.425702 seconds
    # 1 queries, 7 matches in 1.420373 seconds
    # 1 queries, 7 matches in 1.419541 seconds
    #   Average time/query: 1.421872 seconds

    # Scanning a hierarchy of 47715 items
    # 1 queries, 14 matches in 18.015012 seconds
    # 1 queries, 14 matches in 17.951607 seconds
    # 1 queries, 14 matches in 17.994924 seconds
    #   Average time/query: 17.987181 seconds


For some more encouraging results in file-system search and indexing, here are some resources:

- http://www.voidtools.com/
- http://rlocate.sourceforge.net/
- http://www.lesbonscomptes.com/recoll/
- http://grothoff.org/christian/doodle/
- http://xapian.org/

.. [1] For more information on Open Metadata, see here https://github.com/abstractfactory/openmetadata
