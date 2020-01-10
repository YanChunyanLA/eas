import eas
import time
import numpy as np
from eas import HRO, selection, TrialSolution, BaseEA
from eas.factor import RandomFactor
import matplotlib.pyplot as plt
import math

time_str = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))

eas.log_flag = True
eas.boundary_strategy_flag = 'boundary'

log_file = open(
    './storages/logs/HRO-target-function-01-%s.tsv' % time_str,
    mode='ab')

NP = 60
N = 4
U = np.array([100] * N)
L = np.array([-100] * N)
GEN = 3000
TRIAL = 8

factors = {
    'r1': RandomFactor([-1.0, 1.0], GEN, N),
    'r2': RandomFactor([-1.0, 1.0], GEN, N),
    'r3': RandomFactor([0.0, 1.0], GEN, N),
}

BaseEA.__SOLUTION_CLASS__ = TrialSolution
TrialSolution.TRIAL_LIMIT = TRIAL

hro = HRO(NP, N, U, L, factors)
hro.register_strategy('selection', selection.random)
hro.set_log_file(log_file)

# target function 01
def func01(xs):
    return xs[0]**2 + 10**6 * sum([x**2 for x in xs[1:]])

hro.set_fitness_func(func01)
hro.fit(GEN)

# 画图操作
plt.scatter(np.arange(1, GEN + 1), [math.log(v) for v in hro.history_best_fitness])
plt.xlabel('Gen')
plt.ylabel('log(f(x))')
plt.savefig('./storages/graphs/HRO-target-function-01-r1[-1--1]-r2[-1--1]-r3[0--1]-%s.png' % time_str)
plt.show()