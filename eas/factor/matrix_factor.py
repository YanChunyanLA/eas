# -*- coding: utf-8 -*-
# author: a2htray
# description: matrix factors of the numerical operation

from eas.factor import Factor
from eas import helper
import numpy as np


class MatrixFactor(Factor):
    """matrix factor
    virtually, the output is a diagonal matrix
    """
    def __init__(self, gen, gen_func, N):
        Factor.__init__(self, gen, gen_func)
        self.N = N
    
    @staticmethod
    def is_matrix_factor(obj):
        return isinstance(obj, MatrixFactor)


def create_matrix_factor(gen, gen_func, N):
    return MatrixFactor(gen, gen_func, N)


class ConstantMatrixFactor(MatrixFactor):
    """constant matrix factor
    """
    def __init__(self, c, gen, N):
        """
        :param c: a constant value
        :param gen: total number of iterations
        :param N: number of dimension
        """
        MatrixFactor.__init__(self, gen, self.constant, N)
        self.c = c
    
    def constant(self, g):
        return np.diag(np.array([self.c] * self.N))


class RandomMatrixFactor(MatrixFactor):
    """constant matrix factor
    """
    def __init__(self, l, gen, n, has_direct=False):
        """
        :param l: the boundaries, iterable object, its size is 2
        :param gen: total number of iterations
        :param n: number of dimension
        :param has_direct: the flag indicating whether the output has a direct coefficient
        """
        super(RandomMatrixFactor, self).__init__(gen, self.random, n)
        self.l = l
        self.has_direct = has_direct

        if not helper.check_is_range(self.l, 2):
            raise ValueError('the length of the range must be 2')

    def random(self, g):
        factor = np.random.uniform(self.l[0], self.l[1], size=self.N)
        directors = np.random.choice([-1, 1], size=self.N)
        return np.diag(factor) if not self.has_direct else np.diag(factor * directors)