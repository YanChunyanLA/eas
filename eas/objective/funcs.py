# -*- coding:utf-8 -*-
# Date: 2021/11/6
# Created by: a2htray
# Description: 目标函数

import numpy as np


def shpere(xs: np.array) -> float:
    return sum([x for x in xs])


def bent_cigar(xs: np.array):
    return xs[0]**2 + 10**6 * sum([x**2 for x in xs[1:]])
