# -*- coding:utf-8 -*-
# Date: 2021/11/7
# Created by: a2htray
# Description: 优化算法的配置类的实现

import abc
from .typing import LimitType, ObjectiveFuncType, LimitCheck


class EA(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def run(self):
        pass

    @abc.abstractmethod
    def cur_iteration(self) -> int:
        pass

    @abc.abstractmethod
    def population(self):
        pass


def default_on_initialize(ea: EA):
    pass


def default_on_iterate_start(ea: EA):
    pass


def default_on_iterate_finish(ea: EA):
    pass


class EAConfig:
    def __init__(self, m: int, n: int, ulimit: LimitType, llimit: LimitType, objective_func: ObjectiveFuncType,
                 iteration: int, limit_check: LimitCheck = LimitCheck.upper):
        self._m = m
        self._n = n
        self._ulimit = ulimit
        self._llimit = llimit
        self._objective_func = objective_func
        self._iteration = iteration
        self._limit_check = limit_check
        # 算法初始化完成回调函数
        self.on_initialize = default_on_initialize
        # 算法迭代开始回调函数
        self.on_iterate_start = default_on_iterate_start
        # 算法迭代结束回调函数
        self.on_iterate_finish = default_on_iterate_finish

    @property
    def m(self):
        return self._m

    @property
    def n(self):
        return self._n

    @property
    def ulimit(self):
        return self._ulimit

    @property
    def llimit(self):
        return self._llimit

    @property
    def objective_func(self):
        return self._objective_func

    @property
    def iteration(self):
        return self._iteration

    @property
    def limit_check(self):
        return self._limit_check
