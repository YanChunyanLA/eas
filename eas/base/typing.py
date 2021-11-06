# -*- coding:utf-8 -*-
# Date: 2021/11/6
# Created by: a2htray
# Description: 类型定义

import numpy as np
import typing

# LimitT 解向量限制类型
LimitType = typing.TypeVar('LimitType', float, typing.Iterable[float])
# FitnessType 适应值类型
FitnessType = typing.TypeVar('FitnessType', float, None)
# ObjectiveFuncType 适应值类型
ObjectiveFuncType = typing.Callable[[np.array], float]

