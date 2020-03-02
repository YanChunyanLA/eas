from .base import BaseEA
from eas import selection
import random


class PRO(BaseEA):
    def __init__(self, _np, n, upperxs, lowerxs, label_size, factors, **kwargs):
        BaseEA.__init__(self, _np, n, upperxs, lowerxs, factors, **kwargs)
        self.label_size = label_size
        self.group_size = int(self.np / self.label_size)

    def get_factor_keys(self):
        return [
            'r1',
            'r2',
        ]

    def fit(self, gen):
        for i in range(gen):
            self.append_best_fitness()
            self.rate_stage(i)
            self.learn_stage(i)
            self.promote_stage(i)

    def rate_stage(self, gen):
        """评级阶段
        """

        # 按照 fitness 对可行解集合中的元素进行排序
        # 从小到大
        self.solutions.sort(key=lambda s: s.apply_fitness_func(self.fitness_func))

        # 如果目标函数为求最大值，则对集合元素进行反转
        # 最终结果为从大到小
        if not self.optimal_minimal:
            self.solutions.reverse()

        # 用于得到传入的因子对象
        factors = self.get_factors()

        # 对所有可能解进行评级操作
        for i in range(self.label_size):
            for j in range(self.group_size):
                index = i * self.group_size + j
                self.solutions[index].add_label(i)

                if self.solutions[index].should_be_fired():
                    s_index = selection.random(0, self.group_size, size=1, excludes=[index])
                    a_index = selection.random(self.group_size, self.group_size * 2, size=1, excludes=[index])

                    new_solution = self.create_solution(all_zero=True)
                    new_solution.vector = (factors['r1'] * self.solutions[s_index].vector + factors['r2'] * self.solutions[a_index].vector) / (factors['r1'] + factors['r2'])
                    new_solution.amend_vector(self.upperxs, self.lowerxs, boundary_strategy=self.boundary_strategy)
                    new_solution.change_vector(new_solution.vector, mean=True, gen=gen)

                    self.solutions[index] = new_solution


    def learn_stage(self, gen):
        """学习阶段，组间学习
        """
        for i in range(self.label_size):
            for j in range(self.group_size):
                # 集合中解向量的下标
                index = i * self.group_size + j
                # 选中的组下标
                group_index = selection.random(0, self.label_size, size=1, excludes=[i])
                # 需要从选中组中随机抽取两个个体
                s1, s2 = selection.random(
                    group_index * self.group_size,
                    (group_index + 1) * self.group_size, size=2
                )
                # 对新生成的解向量进行验证
                # 如果适应值适于原先的，则进行替换
                trial_solution = self.create_solution(all_zero=True)

                rate = self.solutions[index].get_learn_rate(gen)
                for k in range(self.n):
                    trial_solution.vector[k] = self.solutions[index].vector[k] + \
                                                rate * (self.solutions[s1].vector[k] - self.solutions[s2].vector[k])

                # trial_solution.vector = self.solutions[index].vector + self.solutions[index].get_learn_rate(gen) * (self.solutions[s1].vector - self.solutions[s2].vector)

                trial_solution.amend_vector(self.upperxs, self.lowerxs, boundary_strategy=self.boundary_strategy)
                # 传入 mean=True 的函数在于：改变解向量的同时记录之前个体的解向量的平均值（各分量的平均值）
                trial_solution.change_vector(trial_solution.vector, mean=True, gen=gen)

                self.solutions[index], _ = self.compare(self.solutions[index], trial_solution)

    def promote_stage(self, gen):
        """提升阶段: 自我学习
        """

        for i in range(self.np):
            # 在 PRO 中，每个解向量自身会有一个随机的学习率
            # 按迭代次数的增加向降低
            learn_rate = self.solutions[i].get_learn_rate(gen)

            self.solutions[i].vector = self.solutions[i].vector + \
                                       learn_rate * \
                                       (self.solutions[i].mean_vector - self.solutions[i].vector)

            self.solutions[i].amend_vector(self.upperxs, self.lowerxs, boundary_strategy=self.boundary_strategy)
            self.solutions[i].change_vector(self.solutions[i].vector)