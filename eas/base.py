logflag = False

class BaseEA(object):
    def __init__(self, NP, N, U, L, factors):
        self.NP = NP # 种群个体数量
        self.N = N # 个体维数
        self.U = U # 各维数值上限
        self.L = L # 各维数值下限
        self.factors = factors
        self.is_minimal = True

    def check_factors(self):
        raise('method check_factors must be reimplemented')

    def is_maximal(self):
        self.is_minimal = False