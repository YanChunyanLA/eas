import time
import eas.target
import eas.factor
import eas.boundary
import eas.selection
import numpy as np
from eas import ABC
import matplotlib.pyplot as plt
import math
import sys

targets = {
    'f1': eas.target.f1,
    'f2': eas.target.f2,
    'f3': eas.target.f3,
    'f4': eas.target.f4,
    'f5': eas.target.f5,
    'f6': eas.target.f6,
    'f7': eas.target.f7,
    'f8': eas.target.f8,
    'f9': eas.target.f9,
    'f10': eas.target.f10,
    'f11': eas.target.f11,
}

if len(sys.argv) < 2 or sys.argv[1] not in targets.keys():
    exit()

func_key = sys.argv[1]

# 常规参数项
eas.log_flag = False  # 用于记录日志开关，当前记录信息
times = 10 if len(sys.argv) <= 2 else int(sys.argv[2]) # 算法执行的总次数  TODO
gen = 3000  # 3000  # 一次算法的迭代次数
_np = 60  # 60  # 总群个体的数量
n = 10  # 10  # 解向量的维数
# 向量越界策略
boundary_strategy = eas.boundary.Boundary.BOUNDARY
# 目标函数，其最优解为 100
fitness_func = targets[func_key]

# 参数项
upperxs = np.array([100] * n)  # 向量各分量上限
lowerxs = np.array([-100] * n)  # 向量各分量下限
eas.TrialSolution.TRIAL_LIMIT = 8  # ABC 个体检验的最大次数

# 开始
time_str = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
log_file = open(
    './storages/logs/m/ABC-%s-%s.tsv' % (func_key, time_str),
    mode='ab')

for i in range(times):
    print('round %d start: ' % (i + 1))
    # 由于因子有生成次数限制，所以需要在 times 循环体内重新创建
    factors = {
        # 在 ABC 中使用到 r1 r2 两个因子
        # 内部操作属于矩阵相乘，故需要传入一个生成随机矩阵的因子对象
        'r1': eas.factor.RandomMatrixFactor([-1.0, 1.0], gen, n, has_direct=False),
        'r2': eas.factor.RandomMatrixFactor([-1.0, 1.0], gen, n, has_direct=False),
    }

    algo = ABC(_np, n, upperxs, lowerxs,
               factors=factors,
               optimal_minimal=True,
               fitness_func=fitness_func,
               boundary_strategy=boundary_strategy,
               solution_class='TrialSolution')

    algo.fit(gen)
    np.savetxt(log_file, np.array(algo.best_fitness_store).T[np.newaxis], delimiter=',')

    print('round %d end: ' % (i + 1))

log_file.close()

# data = np.loadtxt(
#     './storages/logs/m/ABC-%s-%s.tsv' % (func_key, time_str),
#     dtype=float,
#     delimiter=','
# )
#
# plt.plot(np.linspace(1, 3000, 3000), np.vectorize(math.log10)(data.mean(axis=0)),
#          label='ABC-%s' % func_key)
# plt.title(func_key)
# plt.xlabel('gen')
# plt.ylabel('log10(%s)' % func_key)
# plt.legend()
# plt.savefig('./storages/graphs/m/ABC-%s-%s.png' % (func_key, time_str), dpi=1280)
# plt.show()
