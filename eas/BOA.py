from eas import helper, TrialSolution, BaseEA, selection
import numpy as np
import random
import copy


# paper
# 谢安世1,2, 于永达1, 黄思明2
# 一种基于标杆管理的优化算法
class BOA(BaseEA):
    def __init__(self, _np, n, upperxs, lowerxs, factors, **kwargs):
        BaseEA.__init__(self, _np, n, upperxs, lowerxs, factors, **kwargs)
        self.global_solution = None

    def fit(self, gen):
        for g in range(gen):
            self.append_best_fitness()

            # 按适应值排序
            self.solutions.sort(key=lambda s: s.apply_fitness_func(self.ff))
            # 若求最大问题，需要将解向量集合反转
            # 保持第一个解为当前最优解
            if not self.optimal_minimal:
                self.solutions.reverse()

            for i in range(self.np):
                # 计算适应值
                self.solutions[i].apply_fitness_func(self.ff)

            # 全局最优为 None
            # 种群当前最优解优于全局最优时
            # 需要对全局最优重新赋值
            if (self.global_solution is None) or (self.global_solution.fitness > self.solutions[0].fitness and self.optimal_minimal) or \
                    (self.global_solution.fitness < self.solutions[0].fitness and not self.optimal_minimal):
                self.global_solution = copy.deepcopy(self.solutions[0])

            # 计算当前种群适应值平均值
            fitness_mean = sum([s.fitness for s in self.solutions]) / self.np

            # for i in range(self.np):










