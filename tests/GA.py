import eas
from eas import GA, selection, TrialSolution, target
from eas.factor import ConstantFactor, LinearFactor
from eas.boundary import Boundary
import numpy as np
import matplotlib.pyplot as plt
import math
import time

time_str = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))

eas.log_flag = True

log_file = open(
    './storages/logs/GA-target-function-01-r1[-1--1]-r2[-1--1]-%s.tsv' % time_str,
    mode='ab')

# 开始对算法中所需要的值进行传值
NP = 60  # 种群的数目
N = 4  # 维度
# 初始化的粒子的位置
U = np.array([30] * N)  # 生成一个初始的4维向量
L = np.array([-30] * N)
# 迭代的次数
gen = 3000

# 初始化的交叉率和变异率
factors = {
    'cr': ConstantFactor(0.8, gen),  # crossRate
    'al': ConstantFactor(0.05, gen),  # alterRate
}

# 对算法进行初始化，并且将写好的值进行传入
ga = GA(NP, N, U, L, factors,
        optimal_minimal=True,
        fitness_func=target.f7,
        solution_class='Solution')  # 对算法进行解的初始化

ga.set_log_file(log_file)

# 算法主要的循环过程： 选择 -> 交叉 -> 变异
ga.fit(gen)

# 画图操作
plt.plot(np.arange(1, gen + 1), [v for v in ga.best_fitness_store])
plt.xlabel('Gen')
plt.ylabel('log(f(x))')
plt.savefig('./storages/graphs/GA-target-function-01-r1[-1--1]-r2[-1--1]-%s.png' % time_str)
plt.show()
