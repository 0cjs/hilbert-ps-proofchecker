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

### Data Structures

Representing formulas is pretty simple, depending on the language; the
obvious way to do this is via an abstract syntax tree. In Haskell,

    newtype  Var = Char
    newtype   Op = Char
    data Formula = Var | MonadicOp Op Formula | DyadicOp Op Formula Formula

Or, if you want nice accessors:

    data Formula = Var
                 | MonadicOp { op ∷ Op, right ∷ Formula }
                 | DyadicOp  { op ∷ Op,  left ∷ Formula, right ∷ Formula }

(Note that this data structure is recursive; a `Formula` that is a
`MonadicOp` or `DyadicOp` includes `Formula` substructures.)

Doing this in Python isn't quite so simple, and needs a lot more error
checking. This could possibly be mitigated to some or even a large degree
by using Python's new type annotations and a type checker. I've not looked
into this in detail yet; last I checked about six years ago the stand-alone
type checker was far too slow to use standalone, though a bit of more
recent experience with it wasn't so bad.

Tree data structures and functions to manipulate them are not hard to build
in Python, but I usually look around first to see if there's a decent
library available that's appropriate for the application that might save
more work than it creates. [anytree] seems to be the most popular, but is
not quite suitable for us because it is designed for an arbitrary numbers
of children per node, which means it doesn't have things such as an
in-order iterator. [binarytree] is also pretty popular and is what I chose
to use here.

[`src/binarytree.pt`] is a set of tests for the third-party `binarytree`
library that I use for ASTs; thus it has no corresponding `.py` file. The
tests are not because I don't trust the behaviour of `binarytree` (it
already has plenty of its own tests), but because this is how I usually
explore the behaviour of a library that I've not used before. The tests
also serve to document some specific library behaviour used by my code in a
fairly obvious way, rather than being buried in the (extensive) library
documentation.

[`src/formula.py`] implements my formula class in Python, with accompanying
tests in [`src/formula.pt`]. It lets you do, e.g., this:

    >>> str(F('→', F('→', NO('ψ'), NO('φ')), F('→', 'φ', 'ψ')))
    (¬ψ → ¬φ) → (φ → ψ)

(The above is directly from the docstring for class `F` and is also a test
that's executed by pytest, using doctest.)

This is actually a lot more code and documentation than I'd normally write
for a simple request (though you did say, the request was open-ended), but
I was really wanting to get the `str()` display working nicely (see below)
and anyway there were a few other things in this that served as useful bits
of research for some of my other projects.

The code is extensively documented in docstrings in the source file; HTML
documentation etc. can be produced from this using [Sphinx] or similar
tools; this is in progress. (If you're wanting a "just the code" version
you can look at [`src/nodocF.py`]; I was curious to see what this looked
like myself, so I left this version of the code in the repo.)

The code formatting is mostly along the lines of [PEP 8], but I do not
hesitate to violate PEP 8 standards when I feel another formatting can
provide better readability or more concision. (Regarding conscision, I hate
it when people say "write code to look like English'; they should go off
and write COBOL where they can type `ADD X TO Y GIVING Z` instead of the
"confusing" and "mathematica' `z = x+y`.)

The `F` class and the additional `NO` constructor are named with extremely
short names because they're what I'm currently directly using those to
construct formulae (in Polish notation); more details on this are in the
class docstring.

This does considerable syntax checking; much of this was driven by wanting
to write a `__str__()` method that gives a nice representation of formulae
as mathematicians like to see them, which was demonstrated above.



<!-------------------------------------------------------------------->
[`Test`]: ../Test
[`pactivate`]: ../pactivate
[`pyproject.toml`]: ../pyproject.toml
[`requirements.txt`]: ../requirements.txt
[`src/binarytree.pt`]: ../src/binarytree.pt
[`src/conftest.py`]: ../src/conftest.py
[`src/formula.pt`]: ../src/formula.pt
[`src/formula.py`]: ../src/formula.py
[`src/pytest_pt.py`]: ../src/pytest_pt.py
[`src/nodocF.py`]: ../src/nodocF.py

[pytest_pt]: https://github.com/cynic-net/pytest_pt
[so 50169991]: https://stackoverflow.com/a/50169991/107294

[dent]: https://github.com/cynic-net/dent
[dot-home]: https://github.com/dot-home/dot-home
[pactivate]: https://github.com/cynic-net/pactivate
[pytest_pt]: https://github.com/cynic-net/pytest_pt
[r8format]: https://github.com/mc68-net/r8format

[PEP 8]: https://peps.python.org/pep-0008/
[Sphinx]: https://www.sphinx-doc.org/
[anytree]: https://pypi.org/project/anytree/
[binarytree]: https://pypi.org/project/binarytree/
