# -*- coding:utf-8 -*-
# Date: 2021/11/9
# Created by: a2htray
# Description: 不对外帮助方法

from eas.base.typing import ObjectiveFuncType
from eas.base import Solution


def choice_better(objective_func: ObjectiveFuncType, s1: Solution, s2: Solution):
    if s1.apply(objective_func).fitness() < s2.apply(objective_func).fitness():
        return s1

    return s2
