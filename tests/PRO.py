import eas
import time
import numpy as np
from eas import PRO, selection, LabelSolution, BaseEA
from eas.factor import RandomFactor
from eas.target import bent_cigar
import matplotlib.pyplot as plt
import math

time_str = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))

# eas.log_flag = True
eas.boundary_strategy_flag = 'boundary'

log_file = open(
    './storages/logs/PRO-target-function-01-%s.tsv' % time_str,
    mode='ab')



NP = 60
N = 4
U = np.array([100] * N)
L = np.array([-100] * N)
GEN = 3000
NC = 8

factors = {
    'r1': RandomFactor([-1.0, 1.0], GEN, N),
    'r2': RandomFactor([-1.0, 1.0], GEN, N),
}

BaseEA.__SOLUTION_CLASS__ = LabelSolution
LabelSolution.LABEL_SIZE = NC
LabelSolution.GEN = GEN

pro = PRO(NP, N, U, L, NC, factors)
pro.register_strategy('selection', selection.random)
pro.set_fitness_func(bent_cigar)

pro.fit(GEN)
print(len(pro.history_best_fitness))

# 画图操作
plt.plot(np.arange(1, GEN + 1), [math.log(v) for v in pro.history_best_fitness])
plt.xlabel('Gen')
plt.ylabel('log(f(x))')
plt.savefig('./storages/graphs/PRO-target-function-01-r1[-1--1]-r2[-1--1]-%s.png' % time_str)
plt.show()

