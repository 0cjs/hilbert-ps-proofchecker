Project To-do File
==================

When adding more testing, consider the benefit vs. time tradeoff.
On a slow machine, pytest takes 0.5s, pdoc 1.5s.

#### mypy

Probably worth using now that it's got caching; clean run is 8s; cached run
is 1.5s. Fixes needed before it can be used:
- `binararytree` has [missing library stubs][mypy-stubs].



<!-------------------------------------------------------------------->
[mypy-stubs]: https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-library-stubs-or-py-typed-marker
