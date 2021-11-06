# -*- coding:utf-8 -*-
# Date: 2021/11/6
# Created by: a2htray
# Description: 种群实现

import typing
from .typing import LimitType, FitnessType, ObjectiveFuncType
from eas.base import create_indexed_solution


class Population:
    def __init__(self, m: int, n: int, ulimit: LimitType = 1.0, llimit: LimitType = 0.0):
        self.m = m
        self.n = n
        # 当前种群的代数
        self.iter_index = 0
        self.solutions = [
            create_indexed_solution(i, self.n, ulimit, llimit) for i in range(self.m)
        ]
        self._fitness_list: typing.List[FitnessType] = [None] * self.m

    def apply(self, func: ObjectiveFuncType):
        self._fitness_list = [
            solution.apply(func).fitness() for solution in self.solutions
        ]

        return self

    def fitness_list(self) -> typing.List[FitnessType]:
        if self._fitness_list[0] is None:
            raise Exception('please apply a objective function first')
        return self._fitness_list

    def rebuild_solution(self, i: int):
        self.solutions[i].rebuild()

    def rebuild_index(self):
        """
        重新构建解的下标
        :return:
        """
        for i in range(self.m):
            self.solutions[i].set_index(i)





