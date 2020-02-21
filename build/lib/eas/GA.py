from .base import BaseEA

class GA(BaseEA):
    def __init__(self, _np, n, upperxs, lowerxs, factors):
        BaseEA.__init__(self, _np, n, upperxs, lowerxs, factors)