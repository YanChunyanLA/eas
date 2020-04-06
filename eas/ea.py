# -*- coding:utf-8 -*-
# @Time : 2020/4/2 13:52
# @Author : a2htray
# @File : ea.py
# @Desc : 所有算法的基类

import numpy as np
from eas.boundary import Boundary
from eas.helper import init_vector


class EA:
    def __init__(self,
                 _np: int,
                 n: int,
                 ub,  # upper boundary
                 lb,  # low boundary
                 procedure: callable,
                 max_gen: int = 500,
                 optimal_minimal: bool = True,
                 boundary_strategy=Boundary.BOUNDARY,
                 random_state: int = None
                 ):
        self.np = _np
        self.n = n
        self.ub = np.array(ub)
        self.lb = np.array(lb)
        self.procedure = procedure
        self.max_gen = max_gen
        self.optimal_minimal = optimal_minimal
        # bs: Boundary Strategy
        self.bs = Boundary.make_strategy(boundary_strategy)
        self.random_state = random_state
        if self.random_state:
            np.random.seed(self.random_state)
        # sc: Solution Collection
        self.sc = np.array([init_vector(self.n, self.ub, self.lb) for _ in range(self.np)])
        # fc: fitness Collection
        self.fc = None
        # hbsc: history best solution collection
        self.hbsc = []
        self.fsort = True
        self.fappend = True

    def equip_procedure(self, s):
        return self.procedure(s)

    def equip_procedure_all(self) -> np.ndarray:
        return np.array([self.equip_procedure(s) for s in self.sc])

    def sort(self):
        flag = 1 if self.optimal_minimal else -1
        self.fc = self.equip_procedure_all()
        sorted_indexes = np.argsort(flag * self.fc)
        self.sc = self.sc[sorted_indexes]
        self.fc = self.fc[sorted_indexes]

    def combine(self) -> np.ndarray:
        """合并解向量和适应值"""
        return np.column_stack((self.sc, self.fc))

    def get_hbsc(self):
        """历史最优"""
        if len(self.hbsc) == 0:
            raise ValueError('Run fit first')

        return np.array(self.hbsc).flatten()

    def get_cbs(self) -> int:
        """当前最优"""
        self.fc = self.equip_procedure_all()
        return (np.argmin if self.optimal_minimal else np.argmax)(self.fc)

    def fit(self):
        for g in range(self.max_gen):
            if self.fsort:
                self.sort()
            if self.fappend:
                self.hbsc.append(self.fc[0])
            self.run(g)

    def run(self, g):
        raise NotImplementedError('Implement run method in subclass')

    def better_than(self, i, s) -> bool:
        """比较适应值"""
        score = self.equip_procedure(s)
        if self.optimal_minimal:  # 如果是求小
            if self.fc[i] > score:
                return False
            else:
                return True
        else:
            if self.fc[i] < score:
                return False
            else:
                return True

    def get_probabilities(self):
        fc = self.equip_procedure_all()
        fc_sum = np.sum(fc)
        # probabilities 小变大，大变小，和不变
        t = np.abs(fc / fc_sum - (1 if self.optimal_minimal else 0))
        return t / np.sum(t)

    def get_current(self):
        """返回最优解的下标，最优解，适应值"""
        fc = self.equip_procedure_all()
        index = (np.argmin if self.optimal_minimal else np.argmax)(fc)
        return index, self.sc[index], fc[index]

    def return_better(self, s1, s2):
        score1 = self.equip_procedure(s1)
        score2 = self.equip_procedure(s2)
        if self.optimal_minimal:  # 如果是求小
            if score1 > score2:
                return s2
            else:
                return s1
        else:
            if score1 > score2:
                return s1
            else:
                return s2