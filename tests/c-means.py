# -*- coding:utf-8 -*-
# @Time : 2020/4/5 15:38
# @Author : a2htray
# @File : c-means.py
# @Desc : 测试代码

import numpy as np
import matplotlib.pyplot as plt

random_state = 42
np.random.seed(random_state)

# 目标函数，最小化
f = lambda w: np.sum([x**2 for x in w])
# 列向量的维数
M = 2
# 列向量的个数
N = 20

# MxN 矩阵，用于表示可行解集合
W = 100 - 100 * np.random.rand(N, M)
W_with_name = np.column_stack((W, np.arange(N).astype(int)))


plt.subplots_adjust(wspace=0.3, hspace=0.3)

for gen in range(4):
    # 计算适应值
    fvalues = [f(w) for w in W_with_name[:, 0:2]]
    tmp = np.column_stack((W_with_name, fvalues))
    W_with_name, _ = np.split(tmp[np.argsort(-tmp[:, -1])], [-1], axis=1)
    ax = plt.subplot(2, 2, gen + 1)
    # 画图
    plt.title("%d GEN" % (gen + 1))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.scatter(W_with_name[:, 0], W_with_name[:, 1])
    # for i in range(N):
    #     plt.text(W_with_name[i, 0], W_with_name[i, 1], W_with_name[i, 2])

    for i in range(N):
        t = 1 / N * np.mean(W_with_name[:,0:2], axis=0)

        if f(t) <= f(W_with_name[i,0:2]):
            W_with_name[i, 0:2] = t
plt.show()
