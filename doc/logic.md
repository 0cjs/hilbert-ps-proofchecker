Notes on Logic
==============

References:
- \[hirst] Hirst and Hirst, [_A Primer for Logic and Proof_][hirst],
  §1 Propositional Calculus.
- Metamath, [Proof Explorer Home Page][mm-home].
- Nishant.


Terminology
-----------

### Propositions and Formulae

__Propostitional variables__  (typ. _a, b, c, p, q, r,_ etc.) stand for a
proposition and cannot be substituted. __Metavariables__ (typ. φ, ψ, χ, φ₁,
φ₂, etc.) are used in __schemas__ which allow you to generate a proposition
by substituting another proposition (atomic or compound) for a
metavariable. (Generally, upper case letters are used for variables when
they represent sets and the like.)

A __formula__ is a simple (atomic) proposition or a __compound proposition__
made from simple propositions and __propositional connectives.__

Formulae with a dyadic connective at the root of the AST refer to that as
the __main connective.__ I'm not clear on whether a monadic connective is
the main connective in, e.g., ¬(φ → ψ).

A formula will have either variables or metavariables (the latter making it
a schema), but never both.

### Logics, Proof Systems, etc.

A __logic__ has three parts: _syntax,_ _semantics_ and a _proof system_
(one of the latter two may be omitted in some logics).
- The __syntax__ is required in all logics, and is the usual thing computer
  geeks know, usually given as a grammar or an ADT.
- The __semantics__ gives values to the propositions (true/false, sets,
  etc.).
- The __proof system__ is a set of __axioms__ and __inference rules.__ The
  axioms may be presented explicitly or __instantiated__ from __axiom
  schemas__ via substitution.

The statement _γ₁, γ₂, … ⊢ φ_ says that a __theorem__ _φ_ can be proved
from the __theory__ _γ₁ …,_ (basically a set of _assumptions_ or "extra"
axioms) and the axioms and inferences in a given proof system. A subscript
may be placed after the turnstile to indicate the proof system in use if it
needs to be distinguished.

### Proofs

A __proof__ is a non-empty sequence of formulae, each of which has a
justification, ending with a __theorem,__ where each formula is:
* a formula that follows from previous formula(s) in the list via an
  interference rule (only MP in our case)
* an assumption from the theory (you can't substitute on these!)
* an axiom (often generated via instantiation of an axiom schema)
* a lemma (i.e., the theorem from another proof or an instantiated theorem
  from a proof schema)

A proof can be viewed as a set of __steps__ each of which includes the
formula it derives, the justification used for that derivation, and the
substitutions used on the schema, if a schema is used. Typically printed
proofs show only the end formula.

In some proof systems, such as the ones used in this repo, all proofs are
also proof schemas. (This is not something you can take for granted; it
depends on the (system in use.) Proofs (actually, just proof schemas) may
be "re-used" by referencing the proof, giving a set of substitutions, and
writing the substituted version as ⊢ … ; as with axioms schemas, this is
_instantiation._

### Other

Logics should have certain properties:
- __Sound:__ A relationship between the proof system and the semantics.
- __Consistent:__ A property of the proof system, that it cannot prove
  "false."
- __Complete:__ Optional, but somtimes nice to have. (Gödel had some things
  to say about this.) A relationship between the proof system and the
  semantics. Roughly, "Anything that can be shown to be semantically true
  can also be proved."

See [[hirst]] §1.9 for more details.


Metamath
--------

Todo:
- Clean up this section.
- Read more of the [Metamath home page][mm-home].

In [Metamath][mm-home]:
- `⊢`: the following expression is provable
- `wff`: the following expression is a well-formed formula
- Substitution (from end of video):
  - Black Constants; match themselves
  - Variables:
    - Blue wff (Well-formed formula): T/F expression; φ, ψ, χ, ‥.
    - Red set variable (subst. another set var): x, y, z, ….
    - Purple class variable: a collection of zero or more sets; A, B, C, ….

### Variables

The "standard" variables used by metamath can be gleaned from [[mmascii]].
E.g., it lists together and in order, φ, ψ, χ, …. Note that the two-letter
ASCII forms are _not_ the [RFC 1345] standard [digraphs]

#### Stuff from the site?

Axiom schemas and inference rule:
- A1:             φ → (ψ → φ)                         (𝜑 → (𝜓 → 𝜑))
- A2: (φ → (ψ → χ)) → ((φ → ψ) → (φ → χ))
- A3:     (¬ψ → ¬φ) → (φ → ψ)
- MP: m: φ;
      M: (φ → ψ));
      ∴: ψ

Sample: [[mm-idALT]]

    Step Hyp  Ref   Expression
      1       A1    (𝜑 → (𝜑 → 𝜑))
      2       A1    (𝜑 → ((𝜑 → 𝜑) → 𝜑))
      3       A2    ((𝜑 → ((𝜑 → 𝜑) → 𝜑)) → ((𝜑 → (𝜑 → 𝜑)) → (𝜑 → 𝜑)))
      4  2,3  MP    ((𝜑 → (𝜑 → 𝜑)) → (𝜑 → 𝜑))
      5  1,4  MP    (𝜑 → 𝜑)

    Step Hyp  Ref   Expression
      1       A1                 φ → (ψ → φ)
      2       A1                 φ → ((φ → φ) → φ)          ⊣ ψ = (φ → φ)
      3       A2     (φ → (ψ → χ)) → ((φ → ψ) → (φ → χ))    ⊣ χ = φ
      4  2,3  MP     m  φ → (ψ → φ)                         ⊣ ψ = (φ → φ)
                     M (φ → (ψ → χ)) → ((φ → ψ) → (φ → χ))  ⊣ χ = φ
                     ∴ (φ → ψ) → (φ → χ)
      5  1,4  MP     φ → φ                                  ⊣ χ = φ

(The first version does not show up in urxvt, presuambly because the italic
Greek Unicode characters such as U+1D711 (italic φ) are not in the font I'm
using, though the terminal can display italic Greek characters just fine
with markup, e.g., _φ._ I need to look into this.)



<!-------------------------------------------------------------------->
<!-- Metamath references are named either for the page stem itself
     (prefixed with `mm-` if it doesn't start with an `mm` or, where that's
     not particularly clear, `mm-X` where `X` is something more clear that
     I've picked. -->

[RFC 1345]: https://datatracker.ietf.org/doc/html/rfc1345
[digraphs]: https://en.wikipedia.org/wiki/Digraphs_and_trigraphs_(programming)
[hirst]: http://www.appstate.edu/~hirstjl/primer/hirst.pdf

[mm-home]: https://us.metamath.org/mpeuni/mmset.html
[mm-idALT]: https://us.metamath.org/mpeuni/idALT.html
[mmascii]: https://us.metamath.org/mpeuni/mmascii.html
