hilbert-ps-proofchecker
=======================

This project implements a proof checker for Hilber PS logic.

This README provides a quick overview suitable for those just wanting
general information about what's in this repo; for details of why
everything is the way it is, see [`doc/explainer.md`].

### Building and Running the Tests

Running `./Test` at the top level will build everything (including
documentation) and run all tests.

This needs nothing more than a Python interpreter: the test script
bootstraps the pip package manager and virtualenv package and builds, under
`.build/`, a virtual environment into which all required packages
(including pytest) are installed. It then runs `pytest` to execute all of
the tests. Any command-line parameters you give to `Test` are passed on to
pytest, with the exception of `-c` as the first parameter which will do a
clean(-ish) build by removing any existing virtual environment and object
files under `.build/`.

The generated HTML documentation is placed under `.build/hdoc`.

(For reasons of time, this has not been tested under Windows, but in theory
it should work the same as it does on Unix so long as you're running the
script in MINGW Bash, which is installed along with [Git for Windows][gfw].)

For more on this, see [`doc/explainer.md`].

### Directories and Files

- `doc/`: Documentation not specific to the code itself, especially
  mathematical background information and cjs's notes.
  - `doc/hirst.pdf`: Hirst and Hirst, [_A Primer for Logic and Proof_][hirst].
    The first chapter of this appears to cover, at an introductory level,
    the basic domain for the proof checking problem.
  - `doc/explainer.md`: Many gory details about exactly how this project
    is set up and works.
  - `doc/logic.md`: cjs's notes on logic, proof systems and the like.
    Nishant helped a lot in answering questions about this; other sources
    include Hirst above and [Metamath][mm-home]. Corrections and
    clarifications are greatly appreciated!
  - `doc/*.md`: The remainder of the files are cjs's personal notes on the
    Hirst book above, exercises from it, and so on.. These are here mainly
    because it's most convenient to store them with the rest of the
    material in this repo, but you should feel free to look through them if
    you like.



<!-------------------------------------------------------------------->
[`doc/explainer.md`]: ./doc/explainer.md
[gfw]: https://gitforwindows.org/

[hirst]: http://www.appstate.edu/~hirstjl/primer/hirst.pdf
[mm-home]: https://us.metamath.org/mpeuni/mmset.html
