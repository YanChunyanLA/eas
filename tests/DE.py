import eas
from eas import DE, selection, target
from eas.factor import ConstantFactor
from eas.boundary import Boundary
import numpy as np
import matplotlib.pyplot as plt
import math
import time

time_str = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))

eas.log_flag = True

log_file = open(
    './storages/logs/DE-target-function-01-cr0.3-f0.5-%s.tsv' % time_str,
    mode='ab')

NP = 10
N = 4
U = np.array([50] * N)
L = np.array([-50] * N)
GEN = 3000
factors = {
    'cr': ConstantFactor(0.3, GEN),
    'f': ConstantFactor(0.5, GEN),
}

de = DE(NP, N, U, L, factors,
        optimal_minimal=True,
        fitness_func=target.exp_rastrigin,
        boundary_strategy=Boundary.BOUNDARY,
        solution_class='Solution')
de.selection_n = 2

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