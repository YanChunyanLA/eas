import eas
import time
import numpy as np
from eas import HRO, selection, TrialSolution, target
from eas.factor import RandomFactor
from eas.boundary import Boundary
import matplotlib.pyplot as plt
import math

time_str = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))

eas.log_flag = True

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

TrialSolution.TRIAL_LIMIT = TRIAL

hro = HRO(NP, N, U, L, factors,
          optimal_minimal=True,
          fitness_func=target.bent_cigar,
          boundary_strategy=Boundary.BOUNDARY,
          solution_class='TrialSolution')

hro.register_strategy('selection', selection.random)
hro.set_log_file(log_file)

hro.fit(GEN)

# 画图操作
plt.scatter(np.arange(1, GEN + 1), [math.log(v) for v in hro.best_fitness_store])
plt.xlabel('Gen')
plt.ylabel('log(f(x))')
plt.savefig('./storages/graphs/HRO-target-function-01-r1[-1--1]-r2[-1--1]-r3[0--1]-%s.png' % time_str)
plt.show()