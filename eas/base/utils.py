# -*- coding:utf-8 -*-
# Date: 2021/11/6
# Created by: a2htray
# Description: 帮助方法

import typing
import numpy as np
from .typing import LimitType


def right_limit(limit: LimitType, n: int) -> np.array:
    """
    返回正确的限制
    :param limit: 原限制
    :param n: 限制的元素个数
    :return: 正确的限制
    """
    if isinstance(limit, float):
        return np.array([limit]*n, dtype=float)

    if isinstance(limit, typing.Iterable):
        return np.array(limit, dtype=float)

    raise Exception('limit must be one of types, float and Iterable[float] supported')


def init_vector(n: int, ulimit: np.array, llimit: np.array) -> np.array:
    """
    生成指定区间内的随机解
    :param n: 元素个数
    :param ulimit: 上限
    :param llimit: 下限
    :return: 返回 np.array 表示的向量
    """
    return (ulimit - llimit) * np.random.random(n) + llimit


