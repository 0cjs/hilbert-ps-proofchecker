''' Formulas are expressions consisting of a *simple proposition,*
    which is just a variable, or a *compound proposition* of variables
    connected by *connectives.*

    Variable names here are restricted to single characters. This
    restriction could be removed, but might introduce problems with certain
    logics where placing things adjacent to each other is an implicit
    operation, e.g., where ``pq`` is considered to mean ``p⋅q``.

    We do not currently support *schemas* from which formulae can be
    *instantiated,* in which case the variables would be *metavariables,*
    often described by an *index.* (Variables and metavariables can never
    be mixed in one object; it's either a formula with variables or a
    schema with metavariables.)

    A formula is represented by the `Fm` class which is a binary tree
    expressing the `abstract syntax tree`_ (AST), of the formula, with
    connectives at the internal nodes and variables at the leaf nodes.

    Many of the functions operating on this AST are recursive, and thus the
    total size of the formula they can process (technically, its depth)
    is limited by the size of the Python stack. This shouldn't be an issue
    for anything readable by humans, but if we need to handle truly huge
    formulae, we need to look at using iteration with heap data structures
    to track our position in the formula.

    Future work:
    * XXX Resolve the tension between a 'formula' and a 'schema.' Possibly
      a formula should never be a schema, but a schema should be a separate
      class that you cons with a formula, so that we always know what
      we're using where.
    * A parser to generate a `Formula` from e.g. ``φ → (ψ → φ)``.
    * Consider how to indicate whether a `Formula` is a schema or not or,
      more likely create a separate schema class, including possibly a
      translation system between metavariable names and indices
      (``φ → (ψ → φ)`` to ``1 → (2 → 1)``).
    * It would be neat to check that a `Formula` is a tautology.
      (PySAT may help if the formulas get complex.) But, per Nishant,
      the check is NP-complete, so not cheap.

    .. _abstract syntax tree: https://en.wikipedia.org/wiki/Abstract_syntax_tree
'''
from    enum  import Enum
from    functools  import lru_cache
from    typing  import Optional, Union

def No(fm):
    ''' Convenience constructor for negating a formula. This accepts
        anything that can be given to the `right` parameter of `Fm`.

        (``NO`` happens to be the standard (RFC 1345) digraph for ``¬``,
        so this is at least close).
    '''
    return Fm('¬', None, fm)

def Im(fma, fmc):
    ''' Convenience constructor for constructing an implication ``A → C``,
        where `fma` is the antecedent and `fmc` is the consequent. These
        take anything that can be given to the `left` and `right`
        parameters of `Fm`.

        It's not entirely clear how useful this is in larger expressions,
        where having an explicit arrow helps with readability, but for
        smaller expressions this seems helpful maybe?
    '''
    return Fm('→', fma, fmc)

class Fm:
    ''' A propositional formula represented as an AST. Each `Fm` is:
        - a leaf node whose value is a variable name, or
        - an internal node which is a monadic, connective with a right
          child or dyadic connective, with left and right children.

        This is named ``Fm`` rather than ``Formula`` as a short name gives
        a reasonably nice Polish notation syntax (embedded in Python) for
        construction and viewing with `repr()` and `str()`:

        >>> repr(Fm('→', 'A', Fm('→', B, No(C))))
        "Fm('→', Fm('A'), Fm('→', Fm('B'), Fm('¬', right=Fm('C'))))"

        >>> str(Fm('→', Fm('→', No(ψ), No(φ)), Fm('→', φ, ψ)))
        '(¬ψ → ¬φ) → (φ → ψ)'

        See `__init__()` for construction details.
    '''

    #   We use an Enum here mainly because it gives nice repr in error output.
    NodeType = Enum('NodeType', ['VAR', 'MONADIC', 'DYADIC', ])
    ' Variable or connective. '
    VAR      = NodeType.VAR     ;'Node type is a variable or metavariable.'
    MONADIC  = NodeType.MONADIC ;'Node type is a monadic conective. (¬)'
    DYADIC   = NodeType.DYADIC  ;'Node type is a dyadic connective. (→, ↔, etc.)'

    class InternalError(RuntimeError): '@private'

    def __init__(self, vc: Union["Fm", str], left=None, right=None):
        ''' Propositional formula constructor. This takes a propositional
            value or connective `vc` and, optionally, left and right
            sub-nodes for the AST.

            `vc` must be a valid variable or connective; see `valtype()`
            below for information on what is valid.

            `left` and `right` may be values of this class or plain
            variable names.

            Formulae ought to be immutable, but Python doesn't have very
            good facilities for doing this. We do our best by making sure
            that that the `value`, `type`, `left`, and `right` attributes
            are read-only. This doesn't prevent anybody from poking at our
            internal variables, but those do start with an underscore as a
            hint that developers should not do this.
        '''
        self._left:  Optional["Fm"] = self._nodify(left)
        self._right: Optional["Fm"] = self._nodify(right)
        self._value: str            = getattr(vc, 'value', vc) # type: ignore [arg-type]
        self._type:  "Fm.NodeType"  = self.valtype(vc)

        ty = self._type; left = self._left; right = self._right
        if ty == self.VAR:
            if left is not None or right is not None:
                raise ValueError(f'AST node {repr(vc)} may not have children')
        elif ty == self.MONADIC:
            if left is not None or right is None:
                raise ValueError(
                    f'AST monadic node {repr(vc)} must have only right child'
                        ' (left={left}, right={right}')
        elif ty == self.DYADIC:
            if left is None or right is None:
                raise ValueError(
                    f'AST dyadic node {repr(vc)} must have two children'
                        ' (left={left}, right={right}')
        else:
            raise self.InternalError()

    @staticmethod
    def _nodify(x) -> Optional["Fm"]:
        ''' Return an AST node (i.e., an `Fm` or `None`) from `x` if it is
            one or we can make one from it. This lets users using `left`
            and `right` parameters to the constructor pass in any of
            `None`, an `Fm` or a string containing a variable name.
        '''
        if x is None:               return None
        if isinstance(x, Fm):       return x
        'anything else:';           return Fm(x)

    @property
    def value(self) -> str:
        ' The value of this node in the AST representing this formula. '
        return self._value

    @property
    def type(self) -> NodeType:
        ' The type of this node in the AST representing this formula. '
        return self._type

    @property
    def left(self):
        ' The left subtree of this node in the AST representing this formula. '
        return self._left

    @property
    def right(self):
        ' The right subtree of this node in the AST representing this formula. '
        return self._right

    #   XXX The following has various typing issues because of the
    #   conflict between the duck typing it started with and the
    #   addition of type signatures later on. We need to come back
    #   to this after some further development and sort it out.
    @staticmethod
    def valtype(obj: Union["Fm",str]) -> NodeType:
        ''' Determine whether a node is a `VAR`, `MONADIC` or `DYADIC`,
            raising `ValueError` if it's none of the above.

            The argument may be:
            - a (Unicode) `str` denoting a variable name or connective; or
            - a formula `Fm`, in which case the top node's value will be
              checked.

            The length of strings is currently asserted to be 1; it's not
            clear yet if we really care about keeping that.

            XXX This could do better error checking, but really ought to be
            replaced with a proper parser that can parse full expressions.
        '''
        val = getattr(obj, 'value', obj)

        #   In contrast to the above, we don't really care whether the
        #   variables a `str`s, `bytestrs`, or anything else the end
        #   user cares to use, so long as we can distinguish between
        #   letters, numbers, and anything else.
        if hasattr(val, 'isalpha') and hasattr(val, 'isnumeric'):
            if len(val) != 1:   # type: ignore [arg-type]
                raise ValueError(f'length must be 1: {repr(val)}')
            if val == '¬':          return Fm.MONADIC
            if val.isalpha():       return Fm.VAR
            if not val.isnumeric(): return Fm.DYADIC
        raise ValueError(f'bad value: {repr(val)}')

    def __eq__(self, other) -> bool:
        ''' Return `True` if two formulae are the same, *including variable
            names.* Note that two formulae instantiated from the same schema
            with different substitutions are different formula. @public
        '''
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value  == other.value \
            and self.left  == other.left \
            and self.right == other.right

    def __repr__(self) -> str:
        ''' A somewhat noisy `repr` that puts `Fm()` constructors everywhere.
            It might be reasonable to remove the `Fm()` around variable
            names (except at the root of the AST), since they can be passed
            directly as strings, and perhaps even print convenience
            constructors (`No`, `Im`) here.
        '''
        left = self.left; right = self.right
        s = 'Fm(' + repr(self.value)
        if not left and not right:
            return s + ')'          # no optional args
        if left:
            s += ', ' + repr(left)
        if right:
            s += ', '
            if not left:  s += 'right='
            s += repr(right)
        return s + ')'

    def __str__(self) -> str:
        ''' Pretty-print the AST an expression with appropriate parentheses
            and spacing.
        '''
        if self.type == Fm.VAR:
            return self.value
        elif self.type == Fm.MONADIC:
            if self.right.type == Fm.DYADIC:
                return self.value + '(' + str(self.right) + ')'
            else:
                return self.value + str(self.right)
        elif self.type == Fm.DYADIC:
            if self.left.type == Fm.DYADIC:
                s = '(' + str(self.left) + ')'
            else:
                s = str(self.left)
            s += ' ' + self.value + ' '
            if self.right.type == Fm.DYADIC:
                s += '(' + str(self.right) + ')'
            else:
                s += str(self.right)
            return s
        else:
            raise self.InternalError()

####################################################################
#   Variables, for convenience.
#
#   These allow us to use just e.g. ``φ`` in Python code, rather than
#   having to type ``'φ'`` as a quoted string. The names and their
#   RFC 1345 digraphs (entered with Ctrl-K <c1><c2>) are:
#
#   - phi f*,  psi q*,  chi *f, theta h*, tau t*,  eta y*,  zeta z*
#
#   XXX I can't see a way to docstring this without making a mess of the code.

φ, ψ, χ, θ, τ, η, ζ = map(Fm, 'φψχθτηζ')
A, B, C, D, E, F, G = map(Fm, 'ABCDEFG')
P, Q, R, S, T,      = map(Fm, 'PQRST')
