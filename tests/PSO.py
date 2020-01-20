import eas
from eas import PSO, selection, TrialSolution, target
from eas.factor import ConstantFactor, LinearFactor
from eas.boundary import Boundary
import numpy as np
import matplotlib.pyplot as plt
import math
import time

time_str = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))

eas.log_flag = True

log_file = open(
    './storages/logs/PSO-target-function-01-r1[-1--1]-r2[-1--1]-%s.tsv' % time_str,
    mode='ab')

NP = 60
N = 4
U = np.array([100] * N)
L = np.array([-100] * N)
u = np.array([5] * N)
l = np.array([-5] * N)
gen = 3000
TRIAL = 8

factors = {
    'w': ConstantFactor(0.8, gen),
    'r1': ConstantFactor(0.1, gen),
    'r2': ConstantFactor(0.1, gen),
}

# factors = {
#     'w': LinearFactor([0, 0.8], gen),
#     'r1': LinearFactor([0, 0.01], gen),
#     'r2': LinearFactor([0, 0.01], gen),
# }

TrialSolution.TRIAL_LIMIT = TRIAL

pso = PSO(NP, N, U, L, u, l, factors,
          optimal_minimal=True,
          fitness_func=target.bent_cigar,
          boundary_strategy=Boundary.BOUNDARY,
          solution_class='VelocitySolution')

pso.set_log_file(log_file)

pso.fit(gen)
# print(abc.history_best_fitness)

# 画图操作
plt.plot(np.arange(1, gen + 1), [math.log(v) for v in pso.best_fitness_store])
plt.xlabel('Gen')
plt.ylabel('log(f(x))')
plt.savefig('./storages/graphs/ABC-target-function-01-r1[-1--1]-r2[-1--1]-%s.png' % time_str)
plt.show()
