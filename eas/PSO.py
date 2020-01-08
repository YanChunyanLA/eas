from .base import BaseEA

class PSO(BaseEA):
    def __init__(self, NP, N, U, L, factors):
        BaseEA.__init__(self, NP, N, U, L, factors)