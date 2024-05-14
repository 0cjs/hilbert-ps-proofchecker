Hirst System L vs. Hilbert System PS
====================================

Hirst System L and Hilbert system PS share the MP inference rule and
Axioms 1 and 2:

- Axiom 1: `A → (B → A)`
- Axiom 2: `(A → (B → C)) → ((A → B) → (A → C))`

Let's make sure that these are tautologies:

    A → (B → A)         (A → (B → C)) → ((A → B) → (A → C))
    ───────────         ───────────────────────────────────
    t T  t T t           t T  t T t   T   t T t  T  t T t
    t T  f T t           t F  t F f   T   t T t  F  t F f
    f T  t F f           t T  f T t   T   t F f  T  t T t
    f T  f T f           t T  f T f   T   t F f  T  t F f
      ●    ○             f T  t T t   T   f T t  T  f T t
                         f T  t F f   T   f T t  T  f T f
                         f T  f T t   T   f T f  T  f T t
                         f T  f T f   T   f T f  T  f T f
                           ○          ●          ○

### Axiom 3

Axiom 3 is different.
- System L Axiom 3: `(¬B → ¬A) → ((¬B → A) → B)`
-       PS Axiom 3: `(¬B → ¬A) → (A → B)`

They should both be tautologies:

    (¬B → ¬A) → ((¬B → A) → B)          (¬B → ¬A) → (A → B)
    ──────────────────────────          ───────────────────
     ft T ft  T   ft T t  T t            ft T ft  T  t T t
     tf F ft  T   tf T t  F f            tf F ft  T  t F f
     ft T tf  T   ft T f  T t            ft T tf  T  f T t
     tf T tf  T   tf F f  T f            tf T tf  T  f T f
        ○     ●           ○                 ○     ●    ○


Proofs
------

We should be able to prove each in the other system.

#### System L: ⊢ (¬B → ¬A) → (A → B)

    1. (¬B → ¬A) → ((¬B → A) → B)                     { A:=A, B:=B } Axiom 3
    2. ...
    x. (¬B → ¬A) → (A → B)`

Can I do a "reverse deduction theorem" and prove that? ¬B → ¬A ⊢ A → B

    1. ¬B → ¬A                                                         Given
    2. (¬B → ¬A) → ((¬B → A) → B)                     { A:=A, B:=B } Axiom 3
    3. (¬B → A) → B                                                   1,2 MP
    4. ...
    x. (A → B)

#### PS: (¬B → ¬A) → ((¬B → A) → B)

    1. ...
    x. (¬B → ¬A) → ((¬B → A) → B)
