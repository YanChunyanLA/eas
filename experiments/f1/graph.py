import matplotlib.pyplot as plt
import numpy as np
import math

data = np.loadtxt(
    './storages/logs/PRO-function-01-2020-02-24-13-46-45-summary.tsv',
    delimiter=',',
    dtype=float
)

for i in range(5):
    for j in range(10):
        plt.subplot(5, 10, i * 10 + j + 1)
        plt.plot(np.arange(1, 3000 + 1), [math.log10(v) for v in data[i * 10 + j]])
        # 画图操作
        plt.xlabel('Gen')
        plt.ylabel('log10(f(x))')

# plt.savefig('./storages/graphs/PRO-target-function-01-r1[-1--1]-r2[-1--1]-%s.png' % time_str)
plt.show()
