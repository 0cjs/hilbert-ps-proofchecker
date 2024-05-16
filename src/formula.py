''' Formulas are expressions consisting of a *simple proposition,*
    which is just a variable, or a *compound proposition* of variables
    connected by *connectives.*

    Variable names here are restricted to single characters. This
    restriction could be removed, but might introduce problems with certain
    logics where placing things adjacent to each other is an implicit
    operation, e.g., where ``pq`` is considered to mean ``p⋅q``.

    Formulas may also be *schemas* from which formulas are *instantiated,*
    in which case the variables are *metavariables.* (Formulas never mix
    variables and metavariables.) Instantiation is done by substituting a
    formula (which can of course be a simple variable) for each
    metavariable. This is often done by giving each variable in the schema
    an *index.* We do not currently support any of this, beyond allowing
    the use of integer indexes as variables. (A string representing an
    integers, e.g., ``'1'`` is not allowed as a variable.)

    A formula is represented by the `F` class which holds a `binarytree`
    expressing its `abstract syntax tree`_ (AST), with connectives at the
    internal nodes and variables at the leaf nodes.

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
    * Consider how to indicate whether a `Formula` is a schema or not,
      including possibly a translation system between metavariable names
      and indices (``φ → (ψ → φ)`` to ``1 → (2 → 1)``).
    * Fix equality so that it considers two formulae to be equal even if
      they don't have the same variable names, as long as the variables
      names could be matched via subtitution. But it's not clear to me
      (cjs) if this is correct for non-schema formulae, and probably requires
      some discussion about schema vs. non-schema representation.
    * It would be neat to check that a `Formula` is a tautology.
      (PySAT may help if the formulas get complex.) But, per Nishant,
      the check is NP-complete, so not cheap.

    .. _abstract syntax tree: https://en.wikipedia.org/wiki/Abstract_syntax_tree
'''
from    binarytree  import Node
from    enum  import Enum
from    functools  import lru_cache
from    typing  import Optional, Union

Value = Union[int, str]
''' For some reason binarytree types ``NodeValue`` as `Any`, though with a
    comment mentioning ``Union[float, int, str]``. `Any` isn't useful to
    us, so we define our own Value, and drop `float` from it since we
    never want to use that as a value.

    XXX Actually, probably only 1-char `str`s should be allowed as `Value`s
    for a formula, and ints should be allowed only in axiom schema, and
    not (instantiated) axioms or hypotheses. See the item under
    "Future work" in the module docstring.
'''

def NO(obj):
    ''' Convenience constructor for negating a formula. This accepts
        anything that can be given to the `right` parameter of `F`.

        ``NO`` happens to be the standard (RFC 1345) digraph for ``¬``.
    '''
    return F('¬', None, obj)

class F:
    ''' A propositional formula represented as an AST of `binarytree.Node`s,
        each of which is:
        - a leaf node whose value is a variable or metavariable name/index, or
        - an internal node which is a monadic or dyadic connective.

        This is named ``F`` rather than ``Formula`` as that gives a
        reasonably nice Polish notation syntax (embedded in Python) for
        construction and viewing with `repr()`:

        >>> str(F('→', F('→', NO(ψ), NO(φ)), F('→', φ, ψ)))
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

    def __init__(self, vc: Union["F", Value], left=None, right=None):
        ''' Propositional formula constructor. This takes a propositional
            value or connective `vc` and, optionally, left and right
            sub-nodes for the AST, which may be formulae of this class,
            `binarytree.Node`s of an formula AST, or a plain variable to be
            turned into a node.

            `vc` must be a valid variable or connective;
            see `valtype()` below for information on what is valid.

            `left` and `right` may be:
            - values of this class;
            - AST node values with a `value` property; or
            - `str` or `int` values that are variables (i.e., where
              `valtype()` will return `VAR`).

            Formulae ought to be immutable, but Python doesn't have very
            good facilities for doing this, so we do our best by ensuring
            that we make copies of `left` and `right` (via `Node.clone()`)
            so at least they're not shared. This doesn't, however, prevent
            anybody from poking at our internal variables, even though they
            start with an underscore as a hint that developers should not
            do this.
        '''
        left  = self._nodify(left)
        right = self._nodify(right)

        if isinstance(vc, self.__class__):
            vc = vc._tree.value

        ty = self.valtype(vc)
        self._tree : Node = Node(vc)
        self._tree.type = ty
        if ty == self.VAR:
            if left or right:
                raise ValueError(f'AST node {repr(vc)} may not have children')
        elif ty == self.MONADIC:
            self._tree.right = right
            if left or not right:
                raise ValueError(
                    f'AST monadic node {repr(vc)} must have only right child'
                        ' (left={left}, right={right}')
        elif ty == self.DYADIC:
            self._tree.left = left
            self._tree.right = right
            if not left or not right:
                raise ValueError(
                    f'AST dyadic node {repr(vc)} must have two children'
                        ' (left={left}, right={right}')
        else:
            raise self.InternalError()

        #   Just in case we've constructed something weird or someone's
        #   managed to sneak something in.
        self._tree.validate()

    @staticmethod
    def _nodify(x) -> Optional[Node]:
        ''' Return a (cloned) `binarytree.Node` AST node from `x` if it is
            one or we can make one from it. This lets users using `left`
            and `right` parameters to the constructor pass in other formula,
            AST nodes, or values from which these can be constructed.

            This clones nodes in order to avoid aliasing problems.

            - Given `None`, we return `None`.
            - Given a `binarytree.Node`, we return a clone of it.
            - Given a formula `F`, we return a clone of its internal tree.
            - Otherwise we call `F()` to attempt to build a valid node
              that we can return.

            In all cases this will give us a value that `binarytree.Node`
            will accept as a `left` or `right` value. (It enforces these
            values being instances of `binarytree.Node`.)
        '''
        if x is None:               return None
        if isinstance(x, Node):     return x.clone()
        if isinstance(x, F):        return x._tree.clone()
        'anything else:';           return F(x)._tree.clone()

    #   XXX The following has various typing issues because of the
    #   conflict between the duck typing it started with and the
    #   addition of type signatures later on. We need to come back
    #   to this after some further development and sort it out.
    @staticmethod
    def valtype(obj: Union["F",Node,Value]) -> NodeType:
        ''' Determine whether a node is a `VAR`, `MONADIC` or `DYADIC`,
            raising `ValueError` if it's none of the above.

            The argument may be:
            - an `int` > 0, denoting a variable index;
            - a (Unicode) `str` denoting a variable name or connective; or
            - an object with a `value` attribute (e.g. an AST `Node`), in
              which case the value will be checked,
            - a formula `F`, in which case the top node's value will be
              checked.

            The length of strings is currently asserted to be 1; it's not
            clear yet if we really care about keeping that.

            Note that due to a quirk of Python, `True` is also a variable
            index because it's a subclass of `int` with value 1. (`False`
            is a subclass of `int` with value 0, and thus can never be
            a variable index.)

            XXX This could do better error checking, but really ought to be
            replaced with a proper parser that can parse full expressions.
        '''
        #   XXX This first line to get the `Node` out of an `F` somehow
        #   feels not terribly nice; let's think of a way to clean this up.
        obj = getattr(obj, '_tree', obj)
        val = getattr(obj, 'value', obj)

        #   Python has no "natural numbers" typeclass or similar idea
        #   (as far as cjs is aware), so we allow only `int`s as indices.
        if isinstance(val, int):
            if val > 0:
                #   We do not currently distinguish between variables,
                #   metavariables and indices.
                return F.VAR
            else:
                raise ValueError(f'variable index {val} must be > 0')
        #   In contrast to the above, we don't really care whether the
        #   variables a `str`s, `bytestrs`, or anything else the end
        #   user cares to use, so long as we can distinguish between
        #   letters, numbers, and anything else.
        if hasattr(val, 'isalpha') and hasattr(val, 'isnumeric'):
            if len(val) != 1:   # type: ignore [arg-type]
                raise ValueError(f'length must be 1: {repr(val)}')
            if val == '¬':          return F.MONADIC
            if val.isalpha():       return F.VAR
            if not val.isnumeric(): return F.DYADIC
        raise ValueError(f'bad value: {repr(val)}')

    def __eq__(self, other) -> bool:
        ''' Return `True` if two formulae are the same, *including
            variable names.* Technically we should probably be
            indicating equality if the variables can be made the same
            through subsitution, though that's not entirely clear.
            (A domain expert needs to be consulted about this.) @public
        '''
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._receq(self._tree, other._tree)

    def _receq(self, x: Node, y: Node) -> bool:
        ' Recursive `binarytree.Node` value comparison for `__eq__()`. '
        if x is None and y is None: return True
        if x is None  or y is None: return False
        if x.value != y.value:      return False
        return self._receq(x.left,  y.left) \
           and self._receq(x.right, y.right)

    def __repr__(self) -> str:
        ''' Somewhat hacky repr, though good enough for the moment.
            Consider removing the ``F()`` around variables, since
            those can be passed in as just strings, and perhaps even
            print a `NO` constructor in the output here.

            But at least this is better than
            ``<formula.F object at 0x7fac64d61550>``.
        '''
        return self._recrep(self._tree)

    def _recrep(self, node: Node) -> str:
        ''' Recursive generation of a string in repr()-ish format the value
            of a given `binarytree.Node` and its children. Just for the use
            of `__repr__()`.
        '''
        s = 'F(' + repr(node.value)
        if not node.left and not node.right:
            return s + ')'          # no optional args
        if node.left:
            s += ', ' + self._recrep(node.left)
        if node.right:
            s += ', '
            if not node.left:   s += 'right='
            s += self._recrep(node.right)
        return s + ')'

    def __str__(self) -> str:
        ''' Pretty-print the AST an expression with appropriate parentheses
            and spacing.
        '''
        tree = self._tree
        s = self._strF(tree)
        if self.valtype(tree) == self.DYADIC:
            return s[1:-1]      # strip off outer parens
        else:
            return s

    @staticmethod
    def _strF(n: Node) -> str:
        ''' This takes a `binarytree.Node` `n` and returns the string
            representation of the formula expression.

            This assumes that the tree structure is correct for
            the `valtype()`s of each node.
        '''
        s   = F._strF
        typ = F.valtype(n)
        if typ == F.VAR:        return str(n.value)
        if typ == F.MONADIC:    return '¬' + s(n.right)
        return f'({s(n.left)} {str(n.value)} {s(n.right)})'

####################################################################
#   Variables, for convenience.
#
#   These allow us to use just e.g. ``φ`` in Python code, rather than
#   having to type ``'φ'`` as a quoted string. The names and their
#   RFC 1345 digraphs (entered with Ctrl-K <c1><c2>) are:
#
#   - phi f*,  psi q*,  chi *f, theta h*, tau t*,  eta y*,  zeta z*
#
#   This brings up an issue with our naming of the formula class: ``F`` is
#   also something people would reasonably want to use as a variable.
#   Perhaps it should be renamed to, e.g., ``F_``. In which case we might
#   also rename `NO` to ``N_``.
#
#   XXX I can't see a way to docstring this without making a mess of the code.

φ, ψ, χ, θ, τ, η, ζ = map(F, 'φψχθτηζ')
A, B, C, D, E       = map(F, 'ABCDE')
