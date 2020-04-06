# -*- coding:utf-8 -*-
# @Time : 2020/4/2 10:01
# @Author : a2htray
# @File : SSE.py
# @Desc : DESC

from eas import DE
from eas.target import fs
import sys
import matplotlib.pyplot as plt
from math import log10

random_state = None
_np = 30  # 种群个数
n = 30
max_gen = 500

ea = DE(_np, n, [100] * n, [-100] * n,
         max_gen=max_gen,
         procedure=fs[sys.argv[1]],
         random_state=random_state)
ea.fit()
fig, ax = plt.subplots(1, 1)
ax.plot([log10(x) for x in ea.hbsc], 'r')
plt.show()


