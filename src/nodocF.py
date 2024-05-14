from    binarytree  import Node
from    enum  import Enum
from    functools  import lru_cache

def NO(obj):
    return F('¬', None, obj)

class F:
    nodetype = Enum('NodeType', ['VAR', 'MONADIC', 'DYADIC', ])
    VAR = nodetype.VAR
    MONADIC = nodetype.MONADIC
    DYADIC = nodetype.DYADIC

    class InternalError(RuntimeError): pass

    def __init__(self, vc, left=None, right=None):
        left  = self.nodify(left)
        right = self.nodify(right)

        ty = self.nodetype(vc)
        self._tree = Node(vc)
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

        self._tree.validate()

    @staticmethod
    def nodify(x):
        if x is None:               return None
        if isinstance(x, Node):     return x.clone()
        if isinstance(x, F):        return x._tree.clone()
        'anything else:';           return F(x)._tree.clone()

    @staticmethod
    def nodetype(obj):
        val = getattr(obj, 'value', obj)

        if isinstance(val, int):
            if val > 0: return F.VAR
            else:       raise ValueError(f'variable index {val} must be > 0')
        if hasattr(val, 'isalpha') and hasattr(val, 'isnumeric'):
            if len(val) != 1: raise ValueError(f'length must be 1: {repr(val)}')
            if val == '¬':          return F.MONADIC
            if val.isalpha():       return F.VAR
            if not val.isnumeric(): return F.DYADIC
        raise ValueError(f'bad value: {repr(val)}')

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._receq(self._tree, other._tree)

    def _receq(self, x, y):
        if x is None and y is None: return True
        if x is None  or y is None: return False
        if x.value != y.value:      return False
        return self._receq(x.left,  y.left) \
           and self._receq(x.right, y.right)

    def __repr__(self):
        return self._recrep(self._tree)

    def _recrep(self, node):
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

    def __str__(self):
        tree = self._tree
        s = self._strF(tree)
        if self.nodetype(tree) == self.DYADIC:
            return s[1:-1]      # strip off outer parens
        else:
            return s

    @staticmethod
    def _strF(n, depth=0):
        ''' This takes a `binarytree.Node` `n` and returns the string
            representation of the formula expression.

            This assumes that the tree structure is correct for
            the `nodetype()`s of each node.
        '''
        s   = F._strF
        typ = F.nodetype(n)
        if typ == F.VAR:        return str(n.value)
        if typ == F.MONADIC:    return '¬' + s(n.right)
        return f'({s(n.left)} {str(n.value)} {s(n.right)})'
