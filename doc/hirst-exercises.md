Completed Exercises from Hirst
==============================

#### 1.1 Building Blocks

_Example_ (p5 bottom), worked out myself and confirmed against result on
next page.

    (a ∨ b) ∧ c     a ∨ (b ∧ c)
    ───────────────────────────
     t T t  T t     t T  t T t
     t T t  F f     t T  t F f
     t T f  T t     t T  f F t
     t T f  F f     t T  f F f
     f T t  T t     f T  t T t
     f T t  F f     f F  t F f
     f F f  F t     f F  f F t
     f F f  F f     f F  f F f

#### 1.2 Tautologies and Contradictions

1. Show a → (b → a) is a tautology.

       a → (b → a)       Happens to be PS axiom 1!
       ───────────
       t T  t t t        All entries in main connective
       t T  f t t        are T, ∴ is a tautology.
       f T  t f f
       f T  f t f

2. Show that (a → (b → c)) → ((a → b) → (a → c)) is a tautology

       (a → (b → c)) → ((a → b) → (a → c))   Happens to be PS axiom 2!
       ───────────────────────────────────
        t T  t T t   T   t T t  T  t T t     All entries in main connective (●)
        t F  t F f   T   t T t  F  t F f     are T, ∴ is a tautology.
        t T  f T t   T   t F f  T  t T t
        t T  f T f   T   t F f  T  t F f
        f T  t T t   T   f T t  T  f T t
        f T  t F f   T   f T t  T  f T f
        f T  f T t   T   f T f  T  f T t
        f T  f T f   T   f T f  T  f T f
          ○          ●          ○

3. Show that (¬b → ¬a) → ((¬b → a) → b) is a tautology

       (¬b → ¬a) → ((¬b → a) → b)
       ──────────────────────────
        ft T ft  T   ft T t  T t         All entries in main connective (●)
        tf F ft  F   tf T t  F f         are T, ∴ is a tautology.
        ft T tf  T   ft T f  T t
        tf T tf  T   tf F f  T f
           ○     ●           ○

   This looks like something you'd prove using the axioms and MP for
   Hilbert PS logic, too, though it looks a bit difficult for me at the
   moment. I suspect a simpler intro to that is upcoming, so I'll leave
   this for now.

4. Show that p ↔ (p → ¬p) is a contradiction.

       p ↔ (p → ¬p)
       ────────────
       t F  t F ft       All entries in main connective (●)
       f F  f T tf       are F, ∴ is a contradiction.

5. Show that p ∧ p is a contingency.

       p ∧ p
       ─────
       t T t         Entries in main connective (●)
       f F f         differ, ∴ is a contingency.

6. Classify formulae (a) through (f). Some here I reason about it in order
   to try to develop intuition about `→` (I'm not nearly as used to that as
   `∧` etc. because it's not a digital logic thing), and because I'm a bit
   tired of typing out truth tables.

   a. (p ∧ q) → p: contingency

          (p ∧ q) → p
          ───────────
           t T t  T t
           t F f  F t
           f F t  T f
           f F f  T f
                  ●

   b. p → (p ∨ q): tautology
      - {pT} and thus RHS is true via `∨`
      - {pF} and thus RHS is true via `F → *`

   c. (p ∨ q) → (p ∧ q): contingency
      - one F one T gives T → F = F
      - both T      gives T → T = T

   d. p ↔ ¬p: contradiction

         p ↔ ¬p
         ──────
         t F ft
         f F tf

   e. p → (¬p → (q ∧ ¬q)): tautology

       p → (¬p → (q ∧ ¬q))
       ───────────────────
       t T  ft T    F
       t T  ft T    F
       f T  tf F    F
       f T  tf F    F
         ●     ○

   f. (p → q) ∨ (q → p): tautology

       (p → q) ∨ (q → p)
       ──────────────────
        t T t  T  t T t
        t F f  T  f T t
        f T t  T  t F f
        f T f  T  f T f

#### 1.3 Logical Equivalence

_Example_ (p11 top): Show that p → q is logically equivalent to ¬q → ¬p.

    p → q   ↔   ¬q → ¬p
    ─────  ───  ────────
    t T t   T   ft T ft
    t F f   T   tf F ft
    f T t   T   ft T tf
    f T f   T   tf T tf

Exercises 1-4 skipped because it's fairly tedious XNORing, and I think
I've got the idea that logical equivalence is XNOR.)

#### 1.4 Contrapositives and Converses

_Proof_ of contrapositive theorem (p.12 top):

    P → Q   ↔   ¬Q → ¬P         show logical equivalence
    ───────────────────
    t T t   T   ft T ft         1. Note that ○ cols are exactly the same
    t F f   T   tf F ft            for any values of P and Q.
    f T t   T   ft T tf         2. And of course this means the iff is
    f T f   T   tf T tf            a tautology (all T). □
      ○     ●      ○

1. Write contrapositives:

   a.  p → q                        ¬q → ¬p
   b.  (p ∨ r) → q                  ¬q → ¬(p ∨ r)
   c.  (a ∧ b) → (c ∨ d)            ¬(c ∨ d) → ¬(a ∧ b)
   d.  If Waldo likes trout,        If Elmer is not a sailor,
       then Elmer is a sailor.      then Waldo does not like trout.
   e.  If 0 ≠ 1,                    If 4 is not a prime,
       then 4 is a prime.           then 0 = 1.
   f.  If tap-dancing is foolish,   If I don't want to be a fool,
       then I want to be a fool.    then tap-dancing is not foolish.

2. Write converses:


   a.  p → q                        q → p
   b.  (p ∨ r) → q                  q → (p ∨ r)
   c.  (a ∧ b) → (c ∨ d)            (c ∨ d) → (a ∧ b)
   d.  If Waldo likes trout,        If Elmer is a sailor,
       then Elmer is a sailor.      then Waldo likes trout.
   e.  If 0 ≠ 1,                    If 4 is a prime,
       then 4 is a prime.           then 0 ≠ 1.
   f.  If tap-dancing is foolish,   If I want to be a fool,
       then I want to be a fool.    then tap-dancing is foolish.

3. Show that a → b is not logically equivalent to its converse.

        a → b   ↔   b → a
        ─────────────────
        t T t   T   t T t       1. ○ cols are not the same, thus
        t F f   F   f T t       2. iff is not a tautology (has F) □
        f T t   F   t F f
        f T f   T   f T f
          ○     ●     ○

4. Show that a → a is logically equivalent to its converse.

   "Clearly."

5. Find a formula that is logically equivalent to its converse and one that
   is not. You could be imaginative and pick examples other than those in
   exercises 3 and 4.

   Not logically equiv: a → (b → a)

       a → (b → a)   ↔   (b → a) → a     show ¬ logical equivalence
       ─────────────────────────────
       t T  t T t    T    t T t  T t     1. Note that ○ cols are not the same
       t T  f T t    T    f T t  T t        for all values of a and b.
       f T  t F f    T    t F f  T f     2. And of course this means the iff is
       f T  f T f    F    f T f  F f        not a tautology (not all T). □
         ○           ●           ○

#### 1.5 Analysis of Arguments

_Example_ p.13, "Show that p;  p → q  │ q is logically valid."

    (p ∧ (p → q))   →   q       assert ∧ of all props → q is a tautology
    ─────────────────────
    t  T  t T t     T   t       ● is all true, ∴ tautology, ∴ valid □
    t  F  t F f     T   f
    f  F  f T t     T   t
    f  F  f T f     T   f
       ○            ●   ○

Interesting insight from the above: the more Fs you can get for the main
connective on the left side, the less you have to care about whether the
conclusion evaluates to T or F.

1. Show the following are valid:

   a. Modus Tollens: a → b;  ¬b  │ ¬a

       ((a → b) ∧ ¬b)  →  ¬a
       ─────────────────────
         t T t  F ft   T  ft
         t F f  F tf   T  ft
         f T t  F ft   T  tf
         f T f  T tf   T  tf
                ○      ●  ○

   b. Constructive Dilemma: p → r;  q → r;  p ∨ q  │ r

       (p → r) ∧ (q → r) ∧ (p ∨ q)  →  r
       ─────────────────────────────────
       etc.

   c. Hypothetical Syllogism: p → q;  q → r  │ p → r

   d. Disjunctive Syllogism: s ∨ t;  ¬s  │ t

2. Is the following logically valid?  
   C = chancellor knows; P = provost knows; T = we're in trouble.  
   Argument: C;  ¬C → P; P → T  | T

       ((C  ∧  (¬C → P))  ∧  (P → T))  →  T
       ────────────────────────────────────
         t  T   ft T t    T   t T t    T  t     yes; logically valid
         t  T   ft T t    F   t F f    T  f
         t  T   ft T f    T   f T t    T  t
         t  T   ft T f    T   f T f    T  f
         f  F   tf T t    F   t T t    T  t
         f  F   tf T t    F   t F f    T  f
         f  F   tf F f    F   f T t    T  t
         f  F   tf F f    F   f T f    T  f
            ⊙             ○            ●  ○

3. Is the following logically valid?  
   R = when it rains; H = wear a hat  
   Argument: R → H;  ¬R  │ ¬H

4-7. (skipped)

#### 1.6 A Proof System

My try at proving Theorem L3 (p.18): A → (B → C), A → B ⊢ A → C:

    1. (A → (B → C)) → ((A → B) → (A → C))      { A:=A, B:=B, C:=C } Axiom 2
    2. A → (B → C)                                                     Given
    3. (A → B) → (A → C)                                              1,2 MP
    4. A → B                                                           Given
    5. A → C                                                          3,4 MP

As well as different ordering of lines (they start with the hypotheses),
I reverse the order of "arguments" to MP. According to Nishant, there's
no real standard for this.

(Side note: from reading the L1 proof, a general trick trick seems to be to
use manipulations (just substitutions, really) of axioms to get useful α →
β expressions where β is something you want, and then further manipulations
to get an α that the lets you use MP to assert the β.)

Exercises; prove these (re-use of lemmas is allowed):

Axioms and existing theorems for re-use:

    A1:                     ⊢             A → (B → A)
    A2:                     ⊢ (A → (B → C)) → ((A → B) → (A → C))
    A3:                     ⊢     (¬B → ¬A) → ((¬B → A) → B)`
    L1:                     ⊢             A → A
    L2:                     ⊢      (¬B → B) → B
    L3:  A → (B → C), A → B ⊢             A → C
    L4:   A → ((B → A) → C) ⊢             A → C

Theorem L5. B ⊢ A → B

    1.  B → (A → B)                                   { A:=B, B:=A } Axiom 1
    2.  B                                                              Given
    3.  A → B                                                         1,2 MP

Theorem L6. A → (B → C), B ⊢ A → C

    1. A → (B → C)                                                     Given
    2. B                                                               Given
    3. (A → (B → C)) → ((A → B) → (A → C))      { A:=A, B:=B, C:=C } Axiom 2
    4. (A → B) → (A → C)                                              1,3 MP
    5. B → (A → B)                                    { A:=B, B:=A } Axiom 1
    6. A → B                                                          2,5 MP
    7. A → C                                                          4,6 MP
                                                         (or 1,6 Theorem L3)

    • (Spent an hour spinning on this one because I mistyped an `A` as a `B`!)

Theorem L7. A → (B → C) ⊢ B → (A → C)

    1. A → (B → C)                                                     Given
    2. (A → (B → C)) → ((A → B) → (A → C))      { A:=A, B:=B, C:=C } Axiom 2
    3. (A → B) → (A → C)                                              1,2 MP

    d. (A → C) → (B → (A → C))                      { A:=A→C, B:=B } Axiom 1

    a. A → (C → A)                                                        A1
    a. (A → (C → A)) → ((A → C) → (A → A))                                A2
    a. (A → C) → (A → A)                                              x,x MP

    b. (A → (B → C)) → ((A → B) → (A → C))      { A:=A, B:=B, C:=C } Axiom 2

    c. B → (A → B)                                    { A:=B, B:=A } Axiom 1
    c. (B → (A → B)) → ((B → A) → (B → B))      { A:=B, B:=A, C:=B } Axiom 2
    c. (B → A) → (B → B)                                              x,x MP


    X. B → (A → C)

Theorem L8. A → B, B → C ⊢ A → C

Theorem L9. P → R ⊢ P → (Q → R)

Theorem L10. ⊢ (¬B → ¬A) → (A → B)

Theorem L11. ⊢ ¬¬B → B

Theorem L12. ⊢ B → ¬¬B

#### 1.7 The Deduction Theorem
#### 1.8 Generalizing L
#### 1.9 Soundness and Completeness of L
#### 1.10 Modifying L

1. Show that Meredith's axiom is a tautology.

       ((((A → B) → (¬C → ¬D)) → C) → E) → ((E → A) → (D → A))
       ───────────────────────────────────────────────────────
           1 3 1  4  21 3 21   5 1  ○ 1  ●   1 2 1  ○  1 2 1
       ───────────────────────────────────────────────────────
           t T t  T  ft T ft   T t  T t  T   t T t  T  t T t
           t T t  T  ft T ft   T t  F f  T   f T t  T  t T t
           t T t  T  ft T tf   T t  T t  T   t T t  T  f T t
           t T t  T  ft T tf   T t  F f  T   f T t  T  f T t
           t T t  F  tf F ft   T f  T t  T   t T t  T  t T t
           t T t  F  tf F ft   T f  F f  T   f T t  T  t T t
           t T t  T  tf T tf   T f  T t  T   t T t  T  f T t
           t T t  T  tf T tf   T f  F f  T   f T t  T  f T t
           t F f  T  ft T ft   T t  T t  T   t T t  T  t T t
           t F f  T  ft T ft   T t  F f  T   f T t  T  t T t
           t F f  T  ft T tf   T t  T t  T   t T t  T  f T t
           t F f  T  ft T tf   T t  F f  T   f T t  T  f T t
           t F f  T  tf F ft   T f  T t  T   t T t  T  t T t
           t F f  T  tf F ft   T f  F f  T   f T t  T  t T t
           t F f  T  tf T tf   T f  T t  T   t T t  T  f T t
           t F f  T  tf T tf   T f  F f  T   f T t  T  f T t
           f T t  T  ft T ft   T t  T t  T   t F f  T  t F f
           f T t  T  ft T ft   T t  F f  T   f T f  F  t F f
           f T t  T  ft T tf   T t  T t  T   t F f  T  f T f
           f T t  T  ft T tf   T t  F f  T   f T f  T  f T f
           f T t  F  tf F ft   T f  T t  T   t F f  T  t F f
           f T t  F  tf F ft   T f  F f  T   f T f  F  t F f
           f T t  T  tf T tf   T f  T t  T   t F f  T  f T f
           f T t  T  tf T tf   T f  F f  T   f T f  T  f T f
           f T f  T  ft T ft   T t  T t  T   t F f  T  t F f
           f T f  T  ft T ft   T t  F f  T   f T f  F  t F f
           f T f  T  ft T tf   T t  T t  T   t F f  T  f T f
           f T f  T  ft T tf   T t  F f  T   f T f  T  f T f
           f T f  F  tf F ft   T f  T t  T   t F f  T  t F f
           f T f  F  tf F ft   T f  F f  T   f T f  F  t F f
           f T f  T  tf T tf   T f  T t  T   t F f  T  f T f
           f T f  T  tf T tf   T f  F f  T   f T f  T  f T f
       ───────────────────────────────────────────────────────

Not actually all that bad to do by hand with Vim visual blocks and
some careful regexp searches to find the `t → f` cases.

2. Write down two instances of Meredith's axiom.

3. Prove the following using Kleene's axiom system:

   a. A → A

   b. A → A, B → C ⊢ A → C

   c. A → B, ⊢ ¬B → ¬A

#### 1.11 Assessing Propositional Calculus

1. Formalise an argument in propositional calculus:

       Socrates is a man.
       All men have ugly feet.
       ─────────────────────────
       Socrates has ugly feet.

       ???   S, M → U  ∴ S → U

2. Is the above valid? Should it be?

   I think, no, can't do it in propositional calculus.

