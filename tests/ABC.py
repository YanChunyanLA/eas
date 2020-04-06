# -*- coding:utf-8 -*-
# @Time : 2020/4/2 10:01
# @Author : a2htray
# @File : WOA.py
# @Desc : DESC

from eas import ABC
from eas.target import fs
import sys
import numpy as np
import matplotlib.pyplot as plt
from math import log10

random_state = None
_np = 60  # 种群个数
n = 10
max_gen = 100

ea = ABC(_np, n, [100] * n, [-100] * n,
         nc=10,
         max_gen=max_gen,
         procedure=fs[sys.argv[1]],
         random_state=random_state)

ea.fit()
print(ea.get_hbsc())
print(np.column_stack((ea.sc, ea.ncs, ea.fc)))
fig, ax = plt.subplots(1, 1)
ax.plot([log10(x) for x in ea.hbsc], 'r')
plt.show()


