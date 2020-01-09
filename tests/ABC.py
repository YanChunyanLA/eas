import eas
from eas import ABC, selection
from eas.factor import ConstantMatrixFactor, RandomMatrixFactor
import numpy as np
import matplotlib.pyplot as plt
import math
import time
import random

time_str = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))

eas.log_flag = True
eas.boundary_strategy_flag = 'boundary'

log_file = open(
    './storages/logs/ABC-target-function-01-r1[-1--1]-r2[-1--1]-%s.tsv' % time_str,
    mode='ab')

NP = 60
N = 4
U = np.array([100] * N)
L = np.array([-100] * N)
GEN = 3000
TRIAL = 8

factors = {
    'r1': RandomMatrixFactor([-1.0, 1.0], GEN, N, has_direct=False),
    'r2': RandomMatrixFactor([-1.0, 1.0], GEN, N, has_direct=False),
}

abc = ABC(NP, N, U, L, TRIAL, factors)
abc.register_strategy('selection', selection.random)
abc.set_log_file(log_file)

# target function 01
def func01(xs):
    return xs[0]**2 + 10**6 * sum([x**2 for x in xs[1:]])

abc.set_fitness_func(func01)
abc.fit(GEN)
print(abc.history_best_fitness)

# 画图操作
plt.scatter(np.arange(1, GEN + 1), [math.log(v) for v in abc.history_best_fitness])
plt.xlabel('Gen')
plt.ylabel('log(f(x))')
plt.savefig('./storages/graphs/ABC-target-function-01-r1[-1--1]-r2[-1--1]-%s.png' % time_str)
