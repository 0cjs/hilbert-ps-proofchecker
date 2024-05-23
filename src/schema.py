''' A `Schema` is a formula generator. It consists of a formula `Fm` whose
    variables are known as *metavariables* and a substitution routine that
    replaces each metavariable, at every occurance of it, with an arbitrary
    formula.

    A list of `Schema` are usually used as the "axioms" (actually, *axiom
    schema*) in a logic system.
'''

from    formula  import *
from    typing  import Optional, Sequence

class Schema:

    def __init__(self, fm:Fm):
        self._fm:Fm = fm

    def __str__(self) -> str:
        return str(self.fm)

    @property
    def fm(self) -> Fm:
        ' The formula for this schema. '
        return self._fm

    @property
    def metavars(self) -> str:
        ''' Return a sequence of the metavariables in this schema, in index
            order (i.e., the order in which they appear in the formula
            `Fm`, left to right).
        '''
        return self._fm.vars

    def sub(self, subs:Optional[Sequence[Fm]] = None) -> Fm:
        ''' Return a new formula `Fm` with each metavariable in this schema
            substituted by its corresponding formulae `Fm` at the same
            index in `subs`. If `subs` is not given or is `None`, the
            metavariables will be substituted with variables of the same
            name.
        '''
        if subs is None:  subs = tuple(map(Fm, self.metavars))
        if len(subs) != len(self.metavars):
            raise ValueError(f'substitution list ({", ".join(map(str, subs))})'
                f' does not match metavariable list {repr(self.metavars)}')
        def _sub(f):
            if f is None:  return None
            if f.type is not Fm.VAR:
                return Fm(f.value, _sub(f.left), _sub(f.right))
            else:
                f = subs[self.metavars.index(f.value)]
                return Fm(f.value, f.left, f.right)
        return _sub(self.fm)

    def subm(self, **subdict:dict[str,Fm]) -> Fm:
        ''' Given a `dict` mapping metavariable names to formulae, return a
            new formula `Fm` with all metavariables in this schema
            substituted with their corresponding formulae in the mapping.
            Missing metavariable names will be substituted with variables
            of the same name.

            XXX (This is not currently implemented. We need to consider
            what error checking needs to be done with this.)
        '''
        raise NotImplementedError()
