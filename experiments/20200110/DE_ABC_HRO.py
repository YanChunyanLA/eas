import eas
from eas import BaseEA, DE, ABC, HRO, selection, Solution, TrialSolution, target
from eas.factor import RandomFactor, ConstantFactor, RandomMatrixFactor, ConstantMatrixFactor, ExpFactor
import numpy as np
import matplotlib.pyplot as plt
import math
import time

time_str = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))

# global setting
eas.log_flag = False
eas.boundary_strategy_flag = 'middle'
fitness_func = target.griewank # change the target function here

# common parameters
NP = 60
N = 10
U = np.array([100] * N)
L = np.array([-100] * N)
GEN = 3000

##### DE
de = DE(NP, N, U, L, {
    'cr': ConstantFactor(0.3, GEN),
    'f': ExpFactor([0, 0.5], GEN),
})
de.set_fitness_func(fitness_func)
de.register_strategy('selection', selection.random)
de.register_strategy('selection_base', selection.best)

de.fit(GEN)

# plt.plot(np.arange(1, GEN + 1), [math.log(v) for v in de.history_best_fitness])
plt.plot(np.arange(1, GEN + 1), de.history_best_fitness)

##### ABC
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

# plt.plot(np.arange(1, GEN + 1), [math.log(v) for v in abc.history_best_fitness])
plt.plot(np.arange(1, GEN + 1), abc.history_best_fitness)

### HRO
TRIAL = 8

BaseEA.__SOLUTION_CLASS__ = TrialSolution
TrialSolution.TRIAL_LIMIT = TRIAL

hro = HRO(NP, N, U, L, {
    'r1': RandomFactor([-1.0, 1.0], GEN, N),
    'r2': RandomFactor([-1.0, 1.0], GEN, N),
    'r3': RandomFactor([0.0, 1.0], GEN, N),
})
hro.register_strategy('selection', selection.random)
hro.set_fitness_func(fitness_func)

hro.fit(GEN)

# plt.plot(np.arange(1, GEN + 1), [math.log(v) for v in hro.history_best_fitness])
plt.plot(np.arange(1, GEN + 1), hro.history_best_fitness)

##### at last
plt.xlabel('Gen')
plt.ylabel('log(f(x))')
plt.show()