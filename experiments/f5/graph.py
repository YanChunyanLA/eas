import matplotlib.pyplot as plt
import numpy as np
import math
import time

algorithm_name = 'GA'

time_str = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))

data = np.loadtxt(
    './storages/logs/%s-function-01-2020-02-25-15-06-41-summary.tsv' % algorithm_name,
    delimiter=',',
    dtype=float
)
for i in range(5):
    for j in range(10):
        plt.subplot(5, 10, i * 10 + j + 1)
        plt.plot(np.arange(1, 3000 + 1), [v for v in data[i * 10 + j]])
        # 画图操作
        plt.xlabel('Gen')
        plt.ylabel('f(x)')

plt.savefig('./storages/graphs/%s-function-05-%s-summary.png' % (algorithm_name, time_str))
plt.show()
