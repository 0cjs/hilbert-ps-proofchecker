Explainer for this Repo
=======================

Since the code and documentation here is intended to be read by people
unfamiliar with my (cjs's) development style, in both the code and
documentation (and particularly this document) I eschew my usual concision
and tend towards rather verbose explanations of what I'm doing and why.

Much of this information in this file is already available in the commit
logs (but is easier to read here); other parts of it make many of my
conventions explicit. However, reading through the Git log from the start
forward should present a readable story about what's been done and why.

This is probably considerably more detailed than expected, but since our
only communication right now is via e-mail and rare videoconferences, I
felt it wise to err on the safe side. (I would not normally document
anything to this degree, unless there was a particular need for it.)

### Top-level Files

This and the following section cover the build and test system. It was
probably faster to set this up than to write up this explanation; it's
something I do frequently and for which I have several standard tools I've
built to help me with this.

[`Test`] is a script at the top level of most ever repo I create; all a
developer has to do is clone the repo and run it (e.g., with `./Test`) and
it handles setting up any virtual environments necessary, finding or
building all dependencies (or at least informing the developer in a clear
manner what dependencies are missing), and running all of the automated
tests. It also takes parameters for doing clean builds, determining what
subset of the tests to run, and so on. (In this case a `-c` at the start of
the arguments will do a "clean" build, and the other parameters are passed
on to `pytest` so you can, e.g., `./Test src/binarytree.pt -vv -k tree` to
run, in fairly verbose mode, all the tests in that file with names matching
"tree.")

This is also of course suitable for running on build servers (such as
GitHub actions); having the build servers and developers able to run the
exact same test suites in the same way aids debugging and reduces the
chance that errrors will make it through to the build servers.

More sophisticated examples of a top-level `Test` script script can be
found in projects like [pactivate], [dent], [pytest_pt], [r8format], and
[dot-home].

[`pactivate`], from the [pactivate] project, is a bootstrap/activation
script for Python virtual environments that has minimal dependencies (pip
and virtualenv are not required) and does the heavy lifting to get from
nothing but a Python interpreter to a running virtual environment with all
dependencies (listed in [`requirements.txt`]) installed. It works on Linux,
Windows and MacOS, though the latter two platforms have not been as
extensively tested.

[`pyproject.toml`] is present both to hold pytest configuration and, in
this case, to hold the comments indicating that this is not a repo designed
to be built into a Python distribution package. (This is a file that they
would have to read were they trying to do this.)

### Source Files: Infrastructure

[`src/pytest_pt.py`] is a pytest plugin from my own project [pytest_pt].
That repo could be brought in as a submodule, or even as a Python
distribution package if I packed that up, but it's generally been
easier in my projects simply to copy the file over.

This does two useful things:

1. It gives slightly nicer filenames to tests, and lets you put tests right
   next to the source files without them being included in distribution
   packages. (I have a fairly strong belief that tests should be as close
   to the code as possible. In particular, I rather dislike the idea of a
   separate top-level `tests/` directory that completely separates them
   from the code; for developers looking at a code file it's much easier to
   open its corresponding test file if it's right there, rather than off in
   a distant directory. And it also serves as a reminder right in front
   of them that they almost never should be touching a code file without
   considering its tests.)

2. pytest_pt has a custom module loader that uses `importlib`, and
   generates module names that are guaranteed never to clash with modules
   loaded via an `import` statement, which avoids [various problems
   described here][so 50169991]. In modern versions of pytest (since
   version 6 or 7, perhaps?) there are now pytest options you can set to do
   something similar, but it's not clear that they give quite as much
   isolation that this does, and anyway this saves you worrying about those
   options.

[`src/conftest.py`] simply sets up some configuration for all code in its
directory and below; in this case it just activates the `pytest_pt` plugin
above.

### Source Files: `binarytree` library

[`src/binarytree.pt`] is a set of tests for the third-party `binarytree`
library that I use for ASTs; thus it has no corresponding `.py` file. The
tests are not because I don't trust the behaviour of `binarytree` (it
already has plenty of its own tests), but because this is how I usually
explore the behaviour of a library that I've not used before. The tests
also serve to document some specific library behaviour used by my code in a
fairly obvious way, rather than being buried in the (extensive) library
documentation.



<!-------------------------------------------------------------------->
[`Test`]: ../Test
[`pactivate`]: ../pactivate
[`pyproject.toml`]: ../pyproject.toml
[`requirements.txt`]: ../requirements.txt
[`src/binarytree.pt`]: ../src/binarytree.pt
[`src/conftest.py`]: ../src/conftest.py
[`src/pytest_pt.py`]: ../src/pytest_pt.py

[pytest_pt]: https://github.com/cynic-net/pytest_pt
[so 50169991]: https://stackoverflow.com/a/50169991/107294

[dent]: https://github.com/cynic-net/dent
[dot-home]: https://github.com/dot-home/dot-home
[pactivate]: https://github.com/cynic-net/pactivate
[pytest_pt]: https://github.com/cynic-net/pytest_pt
[r8format]: https://github.com/mc68-net/r8format
