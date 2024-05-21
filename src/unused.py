''' Remove unused steps from a proof.
'''

from    enum  import Enum
from    typing  import List, Set

####################################################################
#   Data structures suggested by someone else; I am dubious about these.

class StepType(Enum):
    A1 = '1'
    A2 = '2'
    A3 = '3'
    MP = '4'

class PropFormula: ...

class ProofStep:
    def __init__(self, name: StepType, assumptions: list[int]):
        self.assumptions: list[int] = assumptions
        self.substitutions: dict[int, PropFormula] = {}
        self.name: StepType = name

    ####################################################################
    #   The following are all convenience methods for rmunused().

    @property
    def notMP(self):
        return self.name != StepType.MP

    @property
    def min(self):
        ' Convenience method; fails if this is not an `MP` step. '
        return self.assumptions[0]

    @property
    def maj(self):
        ' Convenience method; fails if this is not an `MP` step. '
        return self.assumptions[1]

    ####################################################################
    #   The following are convenience methods for testing.

    def __eq__(x, y):
        if not isinstance(y, type(x)): return NotImplemented
        return          x.name == y.name \
           and x.substitutions == y.substitutions \
           and   x.assumptions == y.assumptions

    def __repr__(self) -> str:
        ''' For convenience in examining test failures, return a
            representation matching the constructors below.
        '''
        if self.name == StepType.MP:
            min, maj = self.assumptions
            return f'MP({min},{maj})'
        return str(self.name.name)

####################################################################
#   Convenience Constructors
#
#   These give us easy construction of the minimal set of steps
#   we need to test rmunused().

A1 = ProofStep(StepType.A1, [])
A2 = ProofStep(StepType.A2, [])

def MP(min: int, maj: int):
    return ProofStep(StepType.MP, [min, maj])

####################################################################

def rmunused(steps: List[ProofStep]) -> List[ProofStep]:
    ''' This is a simplified version of problem 2 that focuses only on the
        "graph" part of the "minify" problem by removing any steps that are
        not referenced by the final step.

        Note that, unlike standard mathematical notation, the steps here
        are numbered from 0. This is for simplicity of implementation in
        this exercise, and is probably not what we'd want to do in a real
        proof system. (But who knows. I don't.)

        Another part of the problem appears to be asking to remove
        duplicate instantiations of axiom schema, which is not too tough,
        but nothing to do with graphs. (It gets tougher if you have to deal
        with error checking, such as substitutions for variable indices
        that are not in the axiom schema.)

        The full description asks for removal of *all* redundancy, which is
        a lot more difficult, since I believe it's possible to have
        redundant steps that look different due to different variable names
        but actually are not. However, it's difficult for me to come up
        with an example, so I may be wrong.

        Further, part of the question says to raise an exception, unless
        "the input constitutes a proof of ϕₙ in PS." which seems to imply
        a *valid* proof, which then means you need to verify it. Or, if
        it's not supposed to imply that, what is something here that is
        not a "proof" of ϕₙ? Something invalid in the data structure?
    '''
    stepcount = len(steps)
    if stepcount == 0:      return []           # Empty proof: no redundancy.
    if steps[-1].notMP:     return steps[-1:]   # If last step is not an MP,
                                                #   no previous steps needed.

    #   Last step is MP; trace it back, finding every dependency.
    def trace(i: int) -> Set[int]:
        s = steps[i]
        if s.notMP:  return set([i])
        return set([i]).union(trace(s.min)).union(trace(s.maj))
    depset = trace(stepcount-1)
    newidx = dict(zip(
        sorted(depset),
        range(0, len(depset))))

    def updateMP(step: ProofStep) -> ProofStep:
        if step.notMP:  return step
        return MP(newidx[step.min], newidx[step.maj])

    newsteps = []
    for i in newidx:
        newsteps.append(updateMP(steps[i]))
    return newsteps
