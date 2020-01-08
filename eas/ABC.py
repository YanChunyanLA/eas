from .base import BaseEA

class ABC(BaseEA):
    def __init__(self, NP, N, U, L, factors):
        BaseEA.__init__(self, NP, N, U, L, factors)