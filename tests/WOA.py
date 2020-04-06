# -*- coding:utf-8 -*-
# @Time : 2020/4/2 10:01
# @Author : a2htray
# @File : WOA.py
# @Desc : DESC

from eas import WOA
from eas.target import fs
import sys

random_state = 42
_np = 60  # 种群个数
n = 30
max_gen = 500

ea = WOA(_np, n, [100] * n, [-100] * n,
         max_gen=max_gen,
         procedure=fs[sys.argv[1]],
         random_state=random_state)

ea.fit()
print(ea.hbsc)


