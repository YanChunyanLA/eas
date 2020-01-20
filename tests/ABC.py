import eas
from eas import ABC, selection, TrialSolution, target
from eas.factor import RandomMatrixFactor
from eas.boundary import Boundary
import numpy as np
import matplotlib.pyplot as plt
import math
import time

time_str = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))

eas.log_flag = True

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

TrialSolution.TRIAL_LIMIT = TRIAL

abc = ABC(NP, N, U, L, factors,
          optimal_minimal=False,
          fitness_func=target.bent_cigar,
          boundary_strategy=Boundary.BOUNDARY,
          solution_class='TrialSolution')

abc.register_strategy('selection', selection.random)
abc.set_log_file(log_file)

abc.fit(GEN)
# print(abc.history_best_fitness)

# 画图操作
plt.plot(np.arange(1, GEN + 1), [math.log(v) for v in abc.best_fitness_store])
plt.xlabel('Gen')
plt.ylabel('log(f(x))')
plt.savefig('./storages/graphs/ABC-target-function-01-r1[-1--1]-r2[-1--1]-%s.png' % time_str)
plt.show()
