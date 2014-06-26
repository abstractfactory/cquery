Overview
========

cQuery is a library for file-system based metadata queries.

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

.. note::

    cQuery currently supports three selectors; class, ID and name. To search for a class, prefix your selector with a dot (.). To do the equivalent but for an ID, use hash (#). To search by name, do not include a prefix. When searching by name, matches are returned via a user-defined suffix, as opposed to the built-in class and ID (.class and .id respectively).

    For example, the results of these two queries are identical::

        $ cquery .Female
        $ cquery Female.class

Selectors
---------

The idea of selectors are adopted from CSS3 and its use in jQuery (from which the name cQuery was derived). jQuery allows users to operate on the Document Object Model, or DOM, using CSS3 selectors to locate the appropriate Nodes. Similarly, cQuery operates on the Content Object Model, or COM, using CSS3 selectors to locate the appropriate folders.

Up or Down
----------

Starting from a root directory, a query can either be made up or down. To find descending matches of a given directory, you would use DOWN. To instead query for ascending matches, you would use UP. To query one-self only, you would use NONE.

Example:
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

