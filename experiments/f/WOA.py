# -*- coding:utf-8 -*-
# @Time : 2020/4/2 15:00
# @Author : a2htray
# @File : WOA.py
# @Desc : 实验脚本

import time
from eas.target import fs
import numpy as np
from eas import WOA
import sys
from eas import experiment

# 常规参数项
# 参数项
func_key = sys.argv[1]
n = int(sys.argv[2])
lb = np.array([-600] * n)  # 向量各分量下限
ub = np.array([600] * n)  # 向量各分量上限

# 开始
time_str = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
log_file = open(
    './storages/logs/WOA-%s-%d-%d-%d.csv' \
    % (func_key,
       n,
       int(sys.argv[3]),
       int(sys.argv[4])
       ),
    mode='ab')

for i in range(int(sys.argv[4])):
    print('round %d start: ' % (i + 1))
    ea = WOA(_np=experiment.NP,
             n=n,
             lb=lb,
             ub=ub,
             procedure=fs[func_key],
             optimal_minimal=True,
             max_gen=int(sys.argv[3]),
             boundary_strategy=experiment.BOUNDARY)

    ea.fit()
    np.savetxt(log_file, np.array(ea.get_hbsc()).T[np.newaxis], delimiter=',')

    print('round %d end: ' % (i + 1))

log_file.close()