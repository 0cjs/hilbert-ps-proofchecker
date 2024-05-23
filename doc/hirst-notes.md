Notes on Hirst, _A Primer for Logic and Proof_
==============================================

These notes are for cjs; they would normally go in his personal notes
repo, [[sedoc]], but are left here for easier review and reference.

See [`hirst.pdf`][local] or [[hirst]] for the book itself. All page
references are to this (printed page numbers as `p.#` and PDF page numbers
as `P.#`) unless otherwise noted.

#### Handy Unicode Chars/Digraphs

All my usual ones (†=custom vimrc), plus:
- †`|>`        8614  " ↦ Rightwards Arrow From Bar (maplet, \mapsto)
-  `fS` U+25A0 9632  " ■ Black Square (\blacksquare)
-  `OS` U+25A1 9633  " □ White Square (\square)

#### Personal Notes

This worked really well for me (cjs) because in particular it uses stuff
I'm already very used to:
- Truth tables (just like logic gates, though some ALU functions are not
  ones normally used in ALUs)
- Mappings


§1 Propositional Calculus
-------------------------

This chapter describes "system L," which is very similar to the "Hilbert
System PS" (HPS). Axiom 3 is different.

The variables and metavariables are usually named _a, b, …_ or _p, q, …_;
it seems arbitrary which set they choose for any particular statement. The
mathematical standard (used on the [Metamath Proof Explorer][mm]) seems to
be [_φ, ψ, χ, …_][mm asc].

### §1.1 - §1.5:  Building Blocks, etc.

__Propositions__ here are boolean-valued expressions (`T`/`F`). Simple
propositions are denoted by variables (`A`, `B`, `a`, `b`, `p`, `q`, etc.);
or _compound propositions_ are variables and connectives, per below. (This
para derived from §1.1-1.6.)

There are five __propositional connectives.__ (pp.2-4) Order of evaluation
is via parens, then from first to last below, and then left to right. (p.6)
These are the standard logical operators, as used e.g. in [ALU]s.

    ¬   negation (monadic; all others are dyadic)
    ∧   AND
    ∨   OR
    →   implication
    ↔   biconditional (iff, XNOR)

Standard truth tables can be constructed for these. [[hirst]] orders things
completely opposite the standard digital logic order: T precedes F and
earliest letter is MSB.

    A B │ A → B
    ────┼───────
    t t │   T
    t f │   F
    f t │   T
    f f │   T

Abbreviated truth tables are constructed as follows:

    p q │ p→q │ ¬(p → q)    ¬(p → q)
    ────┼─────┼─────────    ────────
    F F │  T  │  F          F F T F
    F T │  T  │  F          F F T T
    T F │  F  │  T          T T F F
    T T │  T  │  F          F T T T
    ────┼─────┼─────────    ────────
    1 2    3     4          4 1 3 2

__Compound propositions__ have a __main connective,__ i.e., the final one
resolved in tables like the above. (E.g., #4 in the example directly above.)

Types of compound propositions:
- __Tautology:__
  - True regardless of values of propositions.
  - Truth table main connective is all `T`.
- __Contradiction:__
  - False regardless of values of propositions.
  - Truth table main connective is all `F`.
- __Contingency:__
  - Requires evaluation of proposition values.
  - Truth table main connective is mix of `T`/`F`.

__Logical Equivalence:__ (p.10)
- If A ↔ B is a tautology, A and B are logically equivalent.
- Share truth tables whose last columns match (not nesc. others!).

The __contrapositive__ of _P → Q_ is _¬Q → ¬P._ __Contrapositive theorem:__
Every formula is logically equivalent to its contrapositive. Useful in
proofs when you can prove the contrapositive more easily. (p.11)

The __converse__ of _P → Q_ is _Q → P._ (Note: not nesc. logically
equivalent.) Proving both a statement and its converse proves the
biconditional. (p.12)

An __argument__ is a list of propositions _P₁, P₂, …, Pₙ_ that
allegedly imply a conclusion :

     P₁
     P₂
     …
     Pₙ
    ────
     Pₙ₊₁

It's __logically valid__ if (P₁ ∧ P₂ ∧ … ∧ Pₙ) → Pₙ₊₁ is a tautology.
(§1.5 p.13)

### §1.6 A Proof System

Proofs here are done in __the system L.__ A proof is a sequence of
formulae with jusitifcations; each line is:
- an axiom of L (which is instantiated from an axiom schema);
- result of applying Modus Ponens (MP);
- a __hypothesis__ or a given formula, `G₁` etc.; or
- a _lemma._

Note that _hypothesis_ is used differently here from standard terminology
where it's an _assumption_ from the _theory._ In Metamath a hypothesis is a
reference to a previous line in an application of an inference rule.

L has three axioms and one inference rule:
- Axiom 1: `A → (B → A)`
- Axiom 2: `(A → (B → C)) → ((A → B) → (A → C))`
- Axiom 3: `(¬B → ¬A) → ((¬B → A) → B)`
- __Modus Ponens__ (MP): if A and A → B are lines, B can be a later line.

Theorem L1 ⊢ A → A proof (p.17); straight copy for reference:

    1. A → ((A → A) → A)                                    Axiom 1
                                               A := A; B := (A → A)

    2. (A → ((A → A) → A)) → ((A → (A → A)) → (A → A))      Axiom 2
                                    A := A, B := (A → A) and C := A

    3. ((A → (A → A)) → (A → A))                       Modus Ponens
                                                      Lines 1 and 2

    4. A → (A → A))                                         Axiom 1
                                                  A := A and B := A

    5. A → A                                           Modus Ponens
                                                      Lines 3 and 4

Introducing a variation of the above book format for concision in this file:

    1. A → ((A → A) → A)                        { A:=A, B:=(A → A) } Axiom 1
    2. (A → ((A → A) → A)) → ((A → (A → A)) → (A → A))
                                          { A:=A, B:=(A → A), C:=A } Axiom 2
    3. ((A → (A → A)) → (A → A))                                      1,2 MP
    4. A → (A → A))                                   { A:=A, B:=A } Axiom 1
    5. A → A                                                          3,4 MP

Technically the proof is just the _propositions_ above; the
__justifications__ (axiom or MP) and "additional information" (substitution
values; line references for MP) are not included.

Once a theorem has been proved, we can use it (actually, an _instance_ of
it, with any substitutions you like) as a __lemma__ in further proofs, e.g
Theorem L2: ⊢ (¬B → B) → B:

    1. ¬B → ¬B                                          { A:=¬B } Theorem L1
    2. (¬B → ¬B) → ((¬B → B) → B)                     { A:=B, B:=B } Axiom 3
    3. ((¬B → B) → B)                                                 1,2 MP

The _hypotheses_ (givens) an be used only exactly as stated, without
substitutions. E.g., A → (B → C), A → B ⊢ A → C:

    1. (A → (B → C)) → ((A → B) → (A → C))      { A:=A, B:=B, C:=C } Axiom 2
    2. A → (B → C)                                              Hypothesis 1
    3. (A → B) → (A → C)                                              1,2 MP
    4. A → B                                                    Hypothesis 2
    5. A → C                                                          3,4 MP

Note that if you re-use a proof (schema) in another proof, you _must_
include all the (substituted) assumptions ("hypotheses," in this book) from
the proof schema as assumptions of the new proof.

### 1.7 The Deduction Theorem

[Quick scan from here onward. --cjs]

Deduction Theorem (Herbrand 1930):
-   If: G₁, …, Gₙ, A ⊢ B
- then: G₁, …, Gₙ    ⊢ A → B.

Not a theorem _of_ System L but _about_ system L:
- If we have proof of P ⊢ Q,
- then a proof ⊢ P → Q exists.

Since it's a not system L inference rule, axiom or theorem, it's
technically incorrect to use it as a justification of a line.
And we can live without it.

How it works: we can always convert a proof G₁, … Gₙ, A ⊢ B into
a proof G₁, … Gₙ, ⊢ A → B. This can be done systematically by
proving (A → B) → M for every line M of the original proof.

### 1.8 Generalizing L

So far, only ¬ and → used. To add the other connectives:
- A ∧ B abbreviates ¬(A → ¬B).
- A ∨ B abbreviates (¬A) → B.
- A ↔ B abbreviates ¬((A → B) → ¬(B → A)).

### 1.9 Soundness and Completeness of L

__Soundness:__ if ⊢ A then A is a tautology. (Everything proved is a
tautology. Anything that can be proved via System L can also be proved by a
truth table.)

__Completeness:__ if A is a tautology, then ⊢ A. (We can assert ⊢ A without
producing a proof; this is a _non-constructive existence proof._)

__Consistency:__ There is no formula A such that both ⊢ A and ⊢ ¬A.
(By soundness theorem, ⊢ A is a tautology, ¬A is a contradiction, not a
tautology, so System L cannot prove ¬A.)

### 1.10 Modifying L

Adding a tautological axiom is pointless, because by the completeness
theorem all tautologies can be proved in System L.

Adding a non-tautological axiom will break consistency (unsound).

Discarding an axiom: none of the axioms can be proved from the other two,
and since System L is consistent the negation of an axiom can't be proved
using the other two either. (Each axiom is _independent_ of the others,
though this can be very challenging to prove.) Thus, discarding an axiom
makes System L incomplete.

Starting from scratch: examples given of:
- Kleene's Axiom System for Propositional Calculus. (Stephen Cole Kleene,
  _Introduction to metamathematics,_ 1952.)
- Meredith’s Axiom System for Propositional Calculus:
  - Just one axiom and MP.
  - ((((A → B) → (¬C → ¬D)) → C) → E) → ((E → A) → (D → A))
  - PITA, hard even to recognise instances of the axiom.

### 1.11 Assessing Propositional Calculus

System L is nice. But propositional calculus doesn't help with things like
"if _n_ > 0 then _n_ + 1 > 0"; a simple P → Q hides the _n._ To fix that we
need a logical system that includes variables. (Presumably that's the
predicate calculus in the next chapter.)



<!-------------------------------------------------------------------->
[ALU]: https://github.com/0cjs/sedoc/blob/master/EE/gate.md
[hirst-loc]: ./hirst.pdf
[hirst]: http://www.appstate.edu/~hirstjl/primer/hirst.pdf
[sedoc]: https://github.com/0cjs/sedoc

[mm]: https://us.metamath.org/mpeuni/mmset.html
[mm asc]: https://us.metamath.org/mpeuni/mmascii.html
