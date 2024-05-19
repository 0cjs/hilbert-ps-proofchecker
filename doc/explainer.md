Explainer for this Repo
=======================

Note: if you have already read an earlier version of this file, you may
find it more convenient to look at the changes since that version using Git
log, which should produce fairly clear results that you can follow forward.
The command you want is the following, substituting the commit ID or ref of
interest:

    git log 9fef604^.. --reverse --patch doc/explainer.md

Note that the commits _after_ the one you specify will be shown; to show
the commit/ref you specify as well, use a `^` after it to start with its
parent.

### Introduction

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
on to `pytest` so you can, e.g., `./Test src/formula.pt -vv -k valtype` to
run, in fairly verbose mode, all the tests in that file with names matching
"valtype.")

This is also of course suitable for running on build servers (such as
GitHub actions); having the build servers and developers able to run the
exact same test suites in the same way aids debugging and reduces the
chance that errors will make it through to the build servers.

More sophisticated examples of a top-level `Test` script script can be
found in projects like [pactivate], [dent], [pytest-pt], [r8format], and
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

### Dependencies

I've written a plugin for pytest called [pytest-pt][pypi-pytest-pt] that I
use here. (This is listed in `requirements.txt`, so `pactivate` installs
this directly from PyPI.) This does two useful things:

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

2. pytest-pt has a custom module loader that uses `importlib`, and
   generates module names that are guaranteed never to clash with modules
   loaded via an `import` statement, which avoids [various problems
   described here][so 50169991]. In modern versions of pytest (since
   version 6 or 7, perhaps?) there are now pytest options you can set to do
   something similar, but it's not clear that they give quite as much
   isolation that this does, and anyway this saves you worrying about those
   options.

The remaining dependencies in `requirements.txt` are discussed where they
are used; you can search from here or just read on.

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
to use initially. It was initially useful, but was removed in a later
refactoring because it wasn't pulling its weight. See the "remove
binarytree" commit for details.

In case you're curious about them from the history, the no-longer-existing
`src/binarytree.pt` as a set of tests for the third-party `binarytree`
library that was previously used for ASTs; thus it had no corresponding
`.py` file. The tests were there not because I don't trust the behaviour of
`binarytree` (it already has plenty of its own tests), but because this is
how I usually explore the behaviour of a library that I've not used before.
The tests also served to document some specific library behaviour used by
my code in a fairly obvious way, rather than being buried in the
(extensive) library documentation.

[`src/formula.py`] implements my formula class in Python, with accompanying
tests in [`src/formula.pt`]. It lets you do, e.g., this:

    >>> str(Fm('→', Fm('→', No(ψ), No(φ)), Fm('→', φ, ψ)))
    (¬ψ → ¬φ) → (φ → ψ)

(The above is directly from the docstring for class `Fm` and is also a test
that's executed by pytest, using doctest.)

This is actually a lot more code and documentation than I'd normally write
for a simple request (though you did say, the request was open-ended), but
I was really wanting to get the `str()` display working nicely (see below)
and anyway there were a few other things in this that served as useful bits
of research for some of my other projects.

The code is extensively documented in docstrings in the source file. HTML
documentation etc. can be produced from this using [Sphinx] or similar;
this project uses [pdoc] and places the generated documentation under
`.build/hdoc/`. If you'd like to see a "just the code" version of
`formula.py`, you can look at [`src/nodocF.py`]; I was curious to see what
this looked like myself, so I left this version of the code in the repo.

For notes on code style and formatting, see § [Coding Style].

The `Fm` class and the additional `No` (negation) and `Im` (implication)
convenience constructors are named with extremely short names because
they're what I'm currently directly using those to construct formulae (in
Polish notation); more details on this are in the class docstring.

This does considerable syntax checking; much of this was driven by wanting
to write a `__str__()` method that gives a nice representation of formulae
as mathematicians like to see them, which was demonstrated above.

### Documentation

§"Data Structures" above (and this file, of course) is the best example here
of the sort of documentation I produce. Documentation generated by [pdoc] from
Python docstrings is found under [`.build/hdoc/`] after running the
top-level build/test script `Test`. (I chose pdoc because it's simple
and seems to do what's necessary here; this isn't necessarily what I'd
use in a production project.)

Regarding CI, see the sub-section [CI and Automatic Builds] below.

### Architecture

For what I've got so far on this relatively simple project, I don't feel
the need for any diagrams in the documentation, but I personally find it
easy to visualise graphs, ASTs, architectures and the like in my head. I'm
open to suggestions here.

There has been some use during testing of rendered binary trees from the
`binarytree` library; if you have a look at `test_NO()` in
[`src/formula.pt`] you'll see that there's a `print(t)` there that shows
the tree if the test fails. Try adding an `assert 0` to the end of the test
to see the diagram that it prints when the test fails.

### Coding Style

The code formatting is mostly along the lines of [PEP 8], but I do not
hesitate to violate PEP 8 standards when I feel another formatting can
provide better readability or more concision.

(I hate it when people say "write code to look like English'; they should
go off and write COBOL where they can type `ADD X TO Y GIVING Z` instead of
the "confusing" and "mathematical" `z = x+y`.)

The first thing code needs to be readable is to be written as much as
possible in the "language" of the application domain. This makes every
large program essentially its own language of sorts embedded in the general
programming language in which it's written; you can think of all projects
as having their own embedded [DSL] to at least some degree.

I tend towards as concise as possible a code style since generally more
time is spent reading than writing code. How concise I can be depends
greatly on who's reading the code and the assumptions you and the reader
share; a style suitable to be read by someone with little familiarity with
the domain or the programming language will include a lot of information
that's simply noise that interferes with reading for someone deeply
familiar with both. In other words, there is no one style that will suit
everyone: code style needs to be adapted to the team. (It seems to me that
math is very much like this, too.)

### UX/DX (User Experience/Developer Experience)

There's obviously an easy-to-use CLI to build and test the project:
`./Test`. There's further discussion of this at the start of this file in
the [Top-level Files] section.

#### Testing

Currently the following testing is done by default:
- mypy type checks
- pytest tests in `.pt` files
- docstring `>>>` annotations in `.py` files

The latter two are both working fine, and test selection etc. can be
done by passing `pytest` arguments to the `Test` script.

The last time I tried using mypy was about six years ago, and for
command-line use it was far too slow for my application. That speed problem
seems to have been fixed in modern versions of mypy, probably due to having
caching, interface files, etc., so it's obviously time for me to take it up
again.

The mypy type checking is still a work in progress. Earlier on to get it
passing at all (with no type hints in my source code yet), I had to deal
with the `binarytree` library, which was giving the usual "missing library
stubs or py.typed marker" error. I chose to deal with this by building
local stubs for the library (`stubgen -o mypy-stubs -p binarytree` and
adding `# type: ignore` to the `graphviz` import) and commiting those. I've
left them there as samples, but I would normally have removed these when
removing the `binarytree` dependency.

I've also added a few type annotations to [`src/formula.py`], but I'm not
convinced that they're all that useful there. (They probably would have
helped more if I'd had them available from the start.) `src/*.pt` tests are
also all type checked, though I don't use type annotations at all there at
the moment.

I'm familiar with other tools for checking test code coverage and the like,
but I don't feel any of them are worth the time to install in this project,
at least at the moment.

#### CI and Automatic Builds

This is in addition to the briefer discussion in §[Top-level Files] above.

I always do continuous integration (CI) in its [original sense][fowler].
I've not set up a "CI" server for this project because it's quite small and
the full build and test runs in a couple of seconds. I would normally
expect that each developer would be running the full set of tests (both on
`main` and on development branches) frequently; with this level of
discipline a CI server that does this independently isn't necessary.

That's not to say a CI server is never useful; there are various situations
where it can be helpful. Examples include where a full build/test cycle
takes a significant amount of time, where a full test requires resources
that most developers don't have, where you have inexperienced developers
contributing to the project (e.g., via PRs), or where you just can't
convince your developers to regularly run all the tests. (Though in this
last case you probably have bigger problems than needing a CI server.)

But it's important to remember that CI is a _process,_ not a tool, and
simply dropping a CI server (which is just a tool) into a project doesn't
necessarily provide any improvement at all.

The core thing here that gives this project CI is not a server, but that
the top-level `Test` script does all building and testing: if that succeeds
you know it's likely that the system (with any changes you may have made)
is working.

In addition to the discussion in above, I think it's worth mentioning that
_the_ most important thing to achieve continuous integration is to ensure
that developer have quick and easy access on their development machine to
all tests, to the greatest degree possible, anyway. Developers should _not_
have to dig through YAML files in a `.github/workflows/` directory or
similar to figure out how to test things. And, of course, once you have a
test system that's easily run interactively by developers, that's also
easily run by a CI server if you want one.

The other important part of a test framework, if the whole thing doesn't
run in a couple of seconds or less, is to give developers the ability to
easily focus in and run just a small portion of the tests. The point of
this is to close to as small a time period as possible the feedback loop of
developer makes change → developer tests change → developer sees results →
repeat. Making it easy for developers to run just the tests that are
related (or so they believe) to the change they're making makes the loop
quicker and thus directly increases productivity. It's normal for me to be
running my currently selected set of tests several times per minute or more;
I have a system that automatically runs them every time I save a file.

A CI server is almost the antithesis of this: it requires you to create a
commit, push it, wait for the system to set up and run the tests on the
server (where, note, you can't select a subset of tests to run) and then
have you look at a web page or whatever to see what went wrong. At that
point, you have an error that you need to replicate on your development
machine anyway, and by this time at least several minutes have elapsed.
Better to find these problems while you're coding, before you commit, than
have to wait for all of this. (That's not to say that CI servers aren't
useful; just that one should focus on getting as many problems as possible
caught _before_ a CI server would ever see them.)



<!-------------------------------------------------------------------->

<!-- References in this repo's documentation -->
[Coding Style]: #coding-style
[CI and Automatic Builds]: #ci-and-automatic-builds
[Top-level Files]: #top-level-files

<!-- References to files in this repo -->
[`.build/hdoc/`]: ../.build/hdoc/
[`Test`]: ../Test
[`doc/TODO.md`]: ../doc/TODO.md
[`pactivate`]: ../pactivate
[`pyproject.toml`]: ../pyproject.toml
[`requirements.txt`]: ../requirements.txt
[`src/conftest.py`]: ../src/conftest.py
[`src/formula.pt`]: ../src/formula.pt
[`src/formula.py`]: ../src/formula.py
[`src/nodocF.py`]: ../src/nodocF.py

[so 50169991]: https://stackoverflow.com/a/50169991/107294

<!-- cjs's projects -->
[dent]: https://github.com/cynic-net/dent
[dot-home]: https://github.com/dot-home/dot-home
[pactivate]: https://github.com/cynic-net/pactivate
[pytest-pt]: https://github.com/cynic-net/pytest_pt
[r8format]: https://github.com/mc68-net/r8format

<!-- Third-party Python packages and docs -->
[PEP 8]: https://peps.python.org/pep-0008/
[Sphinx]: https://www.sphinx-doc.org/
[anytree]: https://pypi.org/project/anytree/
[binarytree]: https://pypi.org/project/binarytree/
[pdoc]: https://pypi.org/project/pdoc/
[pypi-pytest-pt]: https://pypi.org/project/pytest-pt/
[pytest-mypy]: https://pypi.org/project/pytest-mypy/

<!-- Other References -->
[fowler]: https://martinfowler.com/articles/continuousIntegration.html
[DSL]: https://en.wikipedia.org/wiki/Domain-specific_language
