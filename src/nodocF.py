from    enum  import Enum
from    functools  import lru_cache
from    typing  import Optional, Union

def No(fm):
    return Fm('¬', None, fm)

def Im(fma, fmc):
    return Fm('→', fma, fmc)

class Fm:
    NodeType = Enum('NodeType', ['VAR', 'MONADIC', 'DYADIC', ])
    VAR      = NodeType.VAR
    MONADIC  = NodeType.MONADIC
    DYADIC   = NodeType.DYADIC

    class InternalError(RuntimeError): '@private'

    def __init__(self, vc: Union["Fm", str], left=None, right=None):
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
        if x is None:               return None
        if isinstance(x, Fm):       return x
        'anything else:';           return Fm(x)

    @property
    def value(self) -> str: return self._value

    @property
    def type(self) -> NodeType: return self._type

    @property
    def left(self): return self._left

    @property
    def right(self): return self._right

    @staticmethod
    def valtype(obj: Union["Fm",str]) -> NodeType:
        val = getattr(obj, 'value', obj)

        if hasattr(val, 'isalpha') and hasattr(val, 'isnumeric'):
            if len(val) != 1:   # type: ignore [arg-type]
                raise ValueError(f'length must be 1: {repr(val)}')
            if val == '¬':          return Fm.MONADIC
            if val.isalpha():       return Fm.VAR
            if not val.isnumeric(): return Fm.DYADIC
        raise ValueError(f'bad value: {repr(val)}')

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value  == other.value \
            and self.left  == other.left \
            and self.right == other.right

    def __repr__(self) -> str:
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

φ, ψ, χ, θ, τ, η, ζ = map(Fm, 'φψχθτηζ')
A, B, C, D, E, F, G = map(Fm, 'ABCDEFG')
