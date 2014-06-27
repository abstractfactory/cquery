.. _reference:

Reference
==========

cQuery consists of a single function: :func:`cquery.matches()` and takes at least two arguments: a `root` and `selector`. The root determines from where within a hierarchy to start a query whereas the `selector` determines what to query for. Additional functions are either helpers
or conveinence measures.

.. autosummary::
   :nosignatures:
   
   ~cquery.matches
   ~cquery.first_match
   ~cquery.convert


cquery.lib
----------

.. automodule:: cquery.lib

.. autofunction:: cquery.lib.matches
.. autofunction:: cquery.lib.first_match
.. autofunction:: cquery.lib.convert

cquery.cli
----------

.. automodule:: cquery.cli
.. autofunction:: cquery.cli.main