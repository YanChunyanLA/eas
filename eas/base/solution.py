# -*- coding:utf-8 -*-
# Date: 2021/11/6
# Created by: a2htray
# Description: 算法的解的实现

import typing
import numpy as np
from .typing import LimitType, FitnessType, ObjectiveFuncType
from .utils import right_limit, init_vector


class Solution:
    """算法的解
    """

    def __init__(self, n: int, ulimit: LimitType = 1.0, llimit: LimitType = 0.0):
        self._n = n
        self._ulimit: np.array = right_limit(ulimit, self._n)
        self._llimit: np.array = right_limit(llimit, self._n)
        self.values: np.array = init_vector(self._n, self._ulimit, self._llimit)
        self._fitness: FitnessType = None
        # 解在集合中的下标
        self.index: int = -1

    def raw(self) -> typing.List[float]:
        return self.values.tolist()

    def fitness(self) -> float:
        if self._fitness is None:
            raise Exception('please apply an objective function first')
        return self._fitness

    def rebuild(self):
        self.values = init_vector(self._n, self._ulimit, self._llimit)

    def apply(self, func: ObjectiveFuncType):
        self._fitness = func(self.values)
        return self

    def set_index(self, i: int):
        self.index = i

    def __str__(self) -> str:
        if self._fitness is None:
            f_str = 'N/A'
        else:
            f_str = '%f' % float(self._fitness)

        return ','.join(map(lambda d: str(d), self.values)) + ',' + f_str


def create_indexed_solution(i: int, n: int, ulimit: LimitType = 1.0, llimit: LimitType = 0.0) -> Solution:
    """
    返回带下标的解
    :param i:
    :param n:
    :param ulimit:
    :param llimit:
    :return:
    """
    s = Solution(n, ulimit, llimit)
    s.set_index(i)
    return s



