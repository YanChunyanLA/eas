# -*- coding:utf-8 -*-
# @Time : 2020/4/6 17:28
# @Author : a2htray
# @File : graph.py
# @Desc : 简易做图

import matplotlib.pyplot as plt
import numpy as np
import math

seed = 0.8
max_gen = 3000
x = np.arange(0, max_gen + 1)
print(x)


def f(x):
    return seed - np.exp((x / max_gen * np.log(seed)))


plt.plot(x, f(x))
plt.show()