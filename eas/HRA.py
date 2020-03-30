from eas import BaseEA, selection
import numpy as np
from random import shuffle, choice


class HRA(BaseEA):
    def __init__(self, _np, n, upperxs, lowerxs, factors, **kwargs):
        BaseEA.__init__(self, _np, n, upperxs, lowerxs, factors, **kwargs)
        self.k = 6 # choice(list(range(1, self.n - 1)))

    def fit(self, gen):
        for i in range(gen):
            self.append_best_fitness()

            # 打乱下标
            shuffled_indexes = self.shuffle_index()
            # 将个体划分成两个组，这里只记录个体的下标索引
            a_indexes = shuffled_indexes[:self.n // 2]
            b_indexes = shuffled_indexes[self.n // 2:]

            for a_index in a_indexes: # 对 group a 中的个体做更新操作
                # ##### 步骤 1 - 操作 1 #####
                # 随机选 k 个维的下标
                selected_indexes = self.shuffle_index()[:self.k]
                # 公式（1）中的 r，为 n 维向量，分量取值 [0, 1]
                r = np.random.uniform(0, 1, size=self.n)
                # 随机从 group b 中选取一个下标
                random_b_index = choice(b_indexes)

                # 新生成个体 trial_solution
                trial_solution = self.create_solution(all_zero=True)
                # 按公式（1）生成解向量
                trial_solution.vector = r * self.solutions[a_index].vector + \
                                        (1 - r) * self.solutions[random_b_index].vector
                # 公式（2）的定义在于各分量的替换
                # 替换规则：
                #   1. 若下标在 selected_indexes 中，则使用新生成的分量
                #   2. 若下标不在 selected_indexes 中，则使用原始的分量
                # 说明：trial_solution.vector 各分量全为新生成的，故程序中使用相反的逻辑，
                #      对不在 selected_indexes 的下标的分量赋值解向量上的原始分量
                restore_indexes = [j for j in list(range(self.n)) if j not in selected_indexes]
                trial_solution.vector[restore_indexes] = self.solutions[a_index].vector[restore_indexes]
                # 修正新生成个体向量分量取值
                trial_solution.amend_vector(self.upperxs, self.lowerxs, boundary_strategy=self.boundary_strategy)
                # 比较适应值，将较优的留下
                self.solutions[a_index], lost = self.compare(self.solutions[a_index], trial_solution)

                # lost == -1 表示新生成个体次于原个体
                # 按公式（3）进行更新
                if lost == -1:
                    a_fitness = self.solutions[a_index].apply_fitness_func(self.ff)
                    b_fitness = self.solutions[random_b_index].apply_fitness_func(self.ff)

                    if (self.optimal_minimal and a_fitness < b_fitness) or (
                            not self.optimal_minimal and a_fitness > b_fitness): # a 优于 b
                        trial_solution.vector = r * self.solutions[a_index].vector + \
                                                (1 - r) * (2 * self.solutions[a_index].vector - self.solutions[random_b_index].vector)
                    else: # b 优于 a
                        trial_solution.vector = r * self.solutions[random_b_index].vector + \
                                                (1 - r) * (2 * self.solutions[random_b_index].vector - self.solutions[a_index].vector)

                trial_solution.amend_vector(self.upperxs, self.lowerxs, boundary_strategy=self.boundary_strategy)
                # 比较适应值，将较优的留下
                self.solutions[a_index], _ = self.compare(self.solutions[a_index], trial_solution)

    def shuffle_index(self):
        indexes = list(range(self.n))
        shuffle(indexes)
        return indexes