# -*- coding:utf-8 -*-
# Date: 2021/11/6
# Created by: a2htray
# Description: 杂交水稻育种算法

import numpy as np
from eas.base import Population, EAConfig, EA
from .utils import choice_better


def check_m_div3(m: int):
    if m % 3 != 0:
        raise Exception('HRO: the passing n must be a multiple of 3')


class HRO(EA):
    def population(self):
        return self._population

    def cur_iteration(self) -> int:
        return self._cur_iteration

    def __init__(self, config: EAConfig):
        # HRO 算法的解的个数必须是 3 的倍数
        check_m_div3(config.m)

        self.config = config
        self._population = Population(self.config.m, self.config.n, self.config.ulimit, self.config.llimit)
        # 用于表示当前的迭代数
        self._cur_iteration = 0

    def run(self):
        for _ in range(self.config.iteration):
            fitness_list = self._population.apply(self.config.objective_func).fitness_list()
            print(np.argsort(fitness_list))
            m_idxs, r_idxs, s_idxs = self._partition()

            self._hybridization(m_idxs, s_idxs)

    def _partition(self):
        i = self.config.m // 3
        fitness_list = self._population.apply(self.config.objective_func).fitness_list()
        sorted_idxs = np.argsort(fitness_list)
        m_idxs = sorted_idxs[0:i]
        r_idxs = sorted_idxs[i:2*i]
        s_idxs = sorted_idxs[2*i:]

        return m_idxs, r_idxs, s_idxs

    def _hybridization(self, m_idxs, s_idxs):
        """杂交，更新 S
        更新 S 的逻辑：遍历属于每一个 sterile 的解，逐一更新解中的向量
        随机取属于 maintainer 的解，选择等位分量(基因)，按公式进行计算新的分量(基因)
        更新单个分量，则进行贪婪选择较优者
        """
        for si in s_idxs:  # 遍历属于每一个 sterile 的解
            origin_sterile_solution = self._population.get_solution(si)
            print('原始第 %d 个 sterile 解：fitness=%f' % (si, origin_sterile_solution.apply(self.config.objective_func).fitness()))
            sterile_solution = origin_sterile_solution.copy()

            for cj in range(self.config.n):  # 遍历每一个分量

                mi = np.random.choice(m_idxs)
                maintainer_solution = self._population.get_solution(mi)

                r1, r2 = np.random.uniform(low=-1, high=1, size=2)
                while r1 + r2 == 0:  # 极端情况
                    r1, r2 = np.random.uniform(low=-1, high=1, size=2)

                x_s, x_m = sterile_solution.get_value(cj), maintainer_solution.get_value(cj)
                sterile_solution.set_value(cj, (r1 * x_s + r2 * x_m) / (r1 + r2))
                # 越界行为可能会发生，若发生，则对其进行调整
                sterile_solution.may_adjust_value(cj, self.config.limit_check)

                print('第 %d 个 sterile 解更新第 %d 个分量后：fitness=%f' % (si, cj, sterile_solution.apply(self.config.objective_func).fitness()))

                better_solution = choice_better(
                    self.config.objective_func,
                    self._population.get_solution(si),
                    sterile_solution,
                )

                print('第 %d 个 sterile 解更新第 %d 个分量后，选择的较优解：fitness=%s' % (si, cj, better_solution.apply(self.config.objective_func).fitness()))

                self._population.set_solution(si, better_solution)

                print('第 %d 个 sterile 解更新第 %d 个分量后，重新设置的解：fitness=%s' % (si, cj, self._population.get_solution(si).apply(self.config.objective_func).fitness()))












