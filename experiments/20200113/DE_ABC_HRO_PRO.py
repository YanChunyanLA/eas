import eas
from eas import BaseEA, DE, ABC, HRO, PRO, selection, Solution, TrialSolution, target, LabelSolution
from eas.factor import RandomFactor, ConstantFactor, RandomMatrixFactor, ConstantMatrixFactor, ExpFactor
import numpy as np
import matplotlib.pyplot as plt
import math
import time

time_str = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))

# global setting
eas.log_flag = False
eas.boundary_strategy_flag = 'middle'
fitness_func = target.bent_cigar # change the target function here

fig, ax = plt.subplots()

# common parameters
NP = 60
N = 10
U = np.array([100] * N)
L = np.array([-100] * N)
GEN = 3000

################ DE
de = DE(NP, N, U, L, {
    'cr': ConstantFactor(0.3, GEN),
    'f': ExpFactor([0, 0.5], GEN),
})
de.set_fitness_func(fitness_func)
de.register_strategy('selection', selection.random)
de.register_strategy('selection_base', selection.best)

de.fit(GEN)

ax.plot(np.arange(1, GEN + 1), [math.log(v) for v in de.best_fitness_store], label='DE')
# ax.plot(np.arange(1, gen + 1), de.history_best_fitness, label='DE')

################ ABC
TRIAL = 8

BaseEA.__SOLUTION_CLASS__ = TrialSolution
TrialSolution.TRIAL_LIMIT = TRIAL

abc = ABC(NP, N, U, L, {
    'r1': RandomMatrixFactor([-1.0, 1.0], GEN, N, has_direct=False),
    'r2': RandomMatrixFactor([-1.0, 1.0], GEN, N, has_direct=False),
})
abc.set_fitness_func(fitness_func)
abc.register_strategy('selection', selection.random)

abc.fit(GEN)

ax.plot(np.arange(1, GEN + 1), [math.log(v) for v in abc.best_fitness_store], label='ABC')
# ax.plot(np.arange(1, gen + 1), abc.history_best_fitness, label='ABC')

################ HRO
TRIAL = 8

BaseEA.__SOLUTION_CLASS__ = TrialSolution
TrialSolution.TRIAL_LIMIT = TRIAL

hro = HRO(NP, N, U, L, {
    'r1': RandomFactor([-1.0, 1.0], GEN, N),
    'r2': RandomFactor([-1.0, 1.0], GEN, N),
    'r3': RandomFactor([0.0, 1.0], GEN, N),
})
hro.set_fitness_func(fitness_func)
hro.register_strategy('selection', selection.random)

hro.fit(GEN)

ax.plot(np.arange(1, GEN + 1), [math.log(v) for v in hro.best_fitness_store], label='HRO')
# ax.plot(np.arange(1, gen + 1), hro.history_best_fitness, label='HRO')

################ PRO
NC = 8

BaseEA.__SOLUTION_CLASS__ = LabelSolution
LabelSolution.LABEL_SIZE = NC
LabelSolution.GEN = GEN

pro = PRO(NP, N, U, L, NC, {
    'r1': RandomFactor([-1.0, 1.0], GEN, N),
    'r2': RandomFactor([-1.0, 1.0], GEN, N),
})
pro.set_fitness_func(fitness_func)
pro.register_strategy('selection', selection.random)

pro.fit(GEN)

# 画图操作
ax.plot(np.arange(1, GEN + 1), [math.log(v) for v in pro.best_fitness_store], label='PRO')
# ax.plot(np.arange(1, gen + 1), pro.history_best_fitness, label='PRO')

##### at last
ax.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1)
plt.xlabel('Gen')
plt.ylabel('log(f(x))')

plt.savefig('./storages/graphs/DE_ABC_HRO_PRO-target-function-01-r1[-1--1]-r2[-1--1]-%s.png' % time_str)
plt.show()