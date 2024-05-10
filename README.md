hilbert-ps-proofchecker
=======================

This project implements a proof checker for Hilber PS logic.

This README provides a quick overview suitable for those just wanting
general information about what's in this repo; for details of why
everything is the way it is, see [`doc/explainer.md`].

### Directories and Files

- `doc/`: Documentation not specific to the code itself, especially
  mathematical background information and cjs's notes.
  - `doc/hirst.pdf`: Hirst and Hirst, [_A Primer for Logic and Proof_][hirst].
    The first chapter of this appears to cover, at an introductory level,
    the basic domain for the proof checking problem.
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
[hirst]: http://www.appstate.edu/~hirstjl/primer/hirst.pdf
[mm-home]: https://us.metamath.org/mpeuni/mmset.html
