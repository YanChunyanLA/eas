from .base import BaseEA
from eas import helper, Solution
import numpy as np
import eas
import random


# paper
# Price, Kenneth V. "Differential evolution: a fast and simple numerical 
# optimizer. " Proceedings of North American Fuzzy Information Processing. 
# IEEE, 1996.
class DE(BaseEA):
    def __init__(self, _np, n, upperxs, lowerxs, factors, **kwargs):
        BaseEA.__init__(self, _np, n, upperxs, lowerxs, factors, **kwargs)
        self.check_factors()

        # 必须为 2 的倍数
        self.selection_n = 4

    def check_factors(self):
        BaseEA.check_factors(self)

    def get_factor_keys(self):
        return [
            'cr',
            'f',
        ]
    
    def set_selection_n(self, n):
        if n % 2 != 0:
            raise ValueError('selection number must be a multiple of 2')
        
        self.selection_n = n

    def fit(self, gen):
        f_is_matrix_factor = BaseEA.is_matrix_factor(self.factors['f'])

        for i in range(gen):
            self.append_best_fitness()

            # 选择基解向量
            fitness_list = [s.apply_fitness_func(self.fitness_func) for s in self.solutions]
            base_index = self.strategies['selection_base'](fitness_list, self.optimal_minimal)
            base_solution = self.solutions[base_index]

            # 每一次迭代都需要重新生成一次因子
            factors = self.get_factors()

            for j in range(self.np):
                # 选择用于 crossover 的解向量的下标集合
                indexes = self.strategies['selection'](0, self.n, self.selection_n)
                # len_of_indexes = len(indexes)

                # 用于保存生成的测试向量
                trial_solution = self.create_solution(all_zero=True)

                for k in range(self.n):
                    if random.random() < factors['cr'] or k == self.n -1:
                        # 计算分量的差
                        difference = self.compute_difference(k, indexes)
                        trial_solution.vector[k] = base_solution.vector[k] + \
                                                   helper.factor_multiply(f_is_matrix_factor, factors['f'], difference)
                    else:
                        trial_solution.vector[k] = self.solutions[j].vector[k]

                trial_solution.amend_vector(self.upperxs, self.lowerxs, boundary_strategy=self.boundary_strategy)
                self.solutions[j], _ = self.compare(self.solutions[j], trial_solution)

    def compute_difference(self, target_index, indexes):
        difference = 0.0
        for i in range(0, len(indexes), 2):
            difference += helper.difference(
                self.solutions[indexes[i]].vector[target_index],
                self.solutions[indexes[i + 1]].vector[target_index])

        return difference
