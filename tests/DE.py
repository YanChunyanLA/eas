import eas
from eas import DE, selection, Solution
from eas.factor import RandomFactor, ConstantFactor
import numpy as np
import matplotlib.pyplot as plt
import math
import time

time_str = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))

eas.log_flag = True
eas.boundary_strategy_flag = 'boundary'

log_file = open(
    './storages/logs/DE-target-function-01-cr0.3-f0.5-%s.tsv' % time_str,
    mode='ab')

NP = 60
N = 4
U = np.array([100] * N)
L = np.array([-100] * N)
GEN = 3000
factors = {
    'cr': ConstantFactor(0.3, GEN),
    'f': ConstantFactor(0.5, GEN),
}

de = DE(NP, N, U, L, factors)
# 设置目标函数

# target function 01
def func01(xs):
    return xs[0]**2 + 10**6 * sum([x**2 for x in xs[1:]])

de.set_fitness_func(func01)
de.set_log_file(log_file)
de.register_strategy('selection', selection.random)
de.register_strategy('selection_base', selection.best)

de.fit(GEN)

# 画图操作
plt.scatter(np.arange(1, GEN + 1), [math.log(v) for v in de.best_fitness_store])
plt.xlabel('Gen')
plt.ylabel('log(f(x))')
plt.savefig('./storages/graphs/DE-target-function-01-cr0.3-f0.5-%s.png' % time_str)
plt.show()