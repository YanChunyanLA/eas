import numpy as np
import random
import eas
from eas.factor import MatrixFactor
from .solution import Solution

class BaseEA(object):
    __SOLUTION_CLASS__ = Solution # default solution derived from Solution

    def __init__(self, NP, N, U, L, factors):
        self.NP = NP # 种群个体数量
        self.N = N # 个体维数
        self.U = U # 各维数值上限
        self.L = L # 各维数值下限
        self.factors = factors
        self.is_minimal = True
        self.fitness_func = None
        self.solutions = [BaseEA.__SOLUTION_CLASS__.create(self.N, self.U, self.L) for _ in range(self.NP)]
        self.strategies = {}
        self.history_best_fitness = [] # 第一代中最优的适应值
        self.log_file = None

        self.check_dimension()

    def set_fitness_func(self, fitness_func):
        self.fitness_func = fitness_func

    def set_log_file(self, log_file):
        self.log_file = log_file

    def check_dimension(self):
        if len(self.U) != self.N or len(self.L) != self.N:
            raise ValueError('dimension does not match')

    def check_factors(self):
        for k in self.get_factor_keys():
            if k not in self.factors:
                raise ValueError('lost the factor')

    def get_factor_keys(self):
        raise ValueError('method get_factor_keys must be reimplemented')

    def fit(self, gen):
        raise ValueError('method fit must be reimplemented')

    def is_maximal(self):
        self.is_minimal = False

    def append_best_fitness(self):
        '''每一次迭代中，需要将最优适应值保存
        存入 self.history_best_fitness 列表中
        '''
        fitness_list = [s.apply_fitness_func(self.fitness_func) for s in self.solutions]
        fitness = min(fitness_list) if self.is_minimal else max(fitness_list)

        if eas.log_flag:
            self.log_best_vector(self.solutions[fitness_list.index(fitness)].vector, fitness)

        self.history_best_fitness.append(fitness)

    def get_factors(self):
        factors = []
        for key in self.factors.keys():
            factors.append(self.factors[key].next())
        return dict(zip(self.factors.keys(), factors))

    def register_strategy(self, key, strategy):
        self.strategies[key] = strategy

    def log_best_vector(self, best_vector, fitness):
        if self.log_file == None:
            raise ValueError('need to set log file, if you want to use log activities')
        np.savetxt(self.log_file, np.append(best_vector, [fitness], axis=0)[np.newaxis], delimiter=',')

    @staticmethod
    def is_matrix_factor(factor):
        return MatrixFactor.is_matrix_factor(factor)

    def __del__(self):
        try:
            self.log_file.close()
        except:
            pass
