
Quickstart
==========

This page will guide you through setting up cQuery and running your first query.

1. Install Open Metadata and cQuery
-----------------------------------

.. code-block:: bash

    $ pip install git+https://github.com/abstractfactory/openmetadata
    $ pip install git+https://github.com/abstractfactory/cquery

2. Make executables for the command-line interface
--------------------------------------------------

Both the Open Metadata and cQuery packages can be run as command-line interfaces, but we’ll have to expose them to the console somehow.

Executables for Windows
~~~~~~~

Save these two files and place them somewhere in your PATH so that they can be accessed via a command-line.

**cquery.bat**

.. code-block:: bash

    @echo off
    python -m cquery %* --verbose


**openmetadata.bat**

.. code-block:: bash

    @echo off
    python -m openmetadata %*

Executables for Unix
~~~~

- cquery

.. code-block:: bash

    $ to be continued

- openmetadata

.. code-block:: bash

    $ to be continued

Both Open Metadata and cQuery will install the executables automatically sometime in the future, I’m just not sure how to go about it at the moment. Does anyone have any experience with this? Let us know!

3. Make content hierarchy, for testing purposes
-----------------------------------------------

.. code-block:: bash

    $ cd c:\projects
    $ mkdir spiderman\assets\Peter
    $ mkdir spiderman\assets\Goblin

    $ mkdir spiderman\shots\1000
    $ mkdir spiderman\shots\2000

4. Tag
------

.. code-block:: bash

    $ cd spiderman\assets\Peter
    $ openmetadata Asset.class --value=None
    5. Query

    $ cd ..
    $ cd ..
    $ cquery .Asset
    c:\projects\spiderman\assets\Peter

And that’s it. :) Now you can tag and query via the command-line. In code, you would query like this:

6. Query in-code
----------------

.. code-block:: python

    import os

    import cquery
    for match in cquery.matches(os.getcwd(), selector='.Asset'):
        print match