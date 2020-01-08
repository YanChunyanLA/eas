from .base import BaseEA

class DE(BaseEA):
    def __init__(self, NP, N, U, L, factors):
        BaseEA.__init__(self, NP, N, U, L, factors)

    def check_factors(self):
        factor_keys = [
            'cr'
        ]

        for k in self.factor_keys:
            if k not in self.factors:
                raise('lost the factor')