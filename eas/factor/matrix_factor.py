from .factor import Factor
from eas import helper
import numpy as np

# 矩阵因子
# 实则产生一个对角方阵
# 对角线上的元素为实际的因子值
class MatrixFactor(Factor):
    def __init__(self, gen, gen_func, N):
        Factor.__init__(self, gen, gen_func)
        self.N = N

def create_matrix_factor(gen, gen_func, N):
    return MatrixFactor(gen, gen_func, N)

class ConstantMatrixFactor(MatrixFactor):
    def __init__(self, c, gen, N):
        MatrixFactor.__init__(self, gen, self.constant, N)
        self.c = c
    
    def constant(self, g):
        return np.diag(np.array([self.c] * self.N))

class RandomMatrixFactor(MatrixFactor):
    def __init__(self, l, gen, N, has_direct=False):
        MatrixFactor.__init__(self, gen, self.random, N)
        self.l = l
        self.has_direct = has_direct

        if not helper.check_is_range(self.l, 2):
            raise ValueError('the length of the range must be 2')

    def random(self, g):
        factor = np.random.uniform(self.l[0], self.l[1], size=self.N)
        directors =  np.random.choice([-1, 1], size=self.N)
        return np.diag(factor) if not self.has_direct else np.diag(factor * directors)