.. _reference:

Reference
==========

cQuery consists of a single function: :func:`cquery.matches()` and takes at least two arguments: a `root` and `selector`. The root determines from where within a hierarchy to start a query whereas the `selector` determines what to query for.

.. autosummary::
   :nosignatures:
   
   ~cquery.matches
   ~cquery.first_match


cquery.py
----------------

.. automodule:: cquery

.. autofunction:: cquery.matches
.. autofunction:: cquery.first_match
