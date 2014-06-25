.. _overview:

Overview
========

cQuery is a jQuery-inspired library for schema-less directory structures.

Reasoning
---------

cQuery doesn't solve the issue of data-modeling. When defining a :term:`schema`, you map a digital landscape onto metaphors more easily understood than their digital counterpart. You then build tools upon this map, with the intent that the landscape rarely, ideally never, changes. Although this works and has worked for a long time, change, as we all know, is inevitable and schema's, as you can imagine, simply doesn't cope - a change to a schema, depending on its magnitude, may well break your tools.

Again, cQuery doesn't solve the issue of data-modeling, data-modeling is inherently a human problem, not a technical one. What cQuery does however is move the barrier at which change starts to affect the work you build upon it so that you are free to start building long before you know how your digital landscape will end up looking.

See also
    - Data and Reality, William Kent

How it works
------------

Given a directory such as:

    `/projects/spiderman/assets/Jackie/animLow`

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