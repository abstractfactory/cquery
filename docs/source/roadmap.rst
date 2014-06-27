Roadmap
=======

We aim cQuery to be suitable for content hierarchies of any depth and width at 10 queries/second. cQuery should work without any setup and may additionally be set up with an indexing daemon. The daemon would either run locally or remotely and maintain a live representation of either all or pre-defined hierarchies. The daemon would optimise common queries. It should be possible to query via the daemon directly, so as to allow the daemon to persist the entire index in-memory for additional performance gain.

- Support most of DOM
- Average query in <0.1 seconds
- 