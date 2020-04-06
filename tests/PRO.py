# -*- coding:utf-8 -*-
# @Time : 2020/4/2 10:01
# @Author : a2htray
# @File : PRO.py
# @Desc : DESC

from eas import PRO
import sys
from eas.target import fs
import matplotlib.pyplot as plt
from math import log10
import pandas as pd
import numpy as np

random_state = 42
_np = 60  # 种群个数
n = 10
max_gen = 500

ea = PRO(_np, n, [100] * n, [-100] * n,
         max_gen=max_gen,
         gnum=3,
         nc=8,
         procedure=fs[sys.argv[1]],
         random_state=random_state)
# print("==== initial solutions ====")
# print(ea.sc)
# print('==== learn rate seeds ====')
# print(ea.learn_rate_seeds)
# print('==== mean solutions ====')
# print(ea.mean_solutions)
ea.fit()
print('==== after ea.fit() ====')
df = pd.DataFrame(
    np.column_stack((ea.fc, ea.assess_record, ea.sc, ea.mean_solutions)),
    columns=['fv', 'nc'] + ['x' + str(i+1) for i in range(n)] + ['mean_x' + str(i+1) for i in range(n)])
print(df)

fig, ax = plt.subplots(1, 1)
ax.plot([log10(x) for x in ea.hbsc], 'r')
plt.show()
