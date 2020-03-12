import time
import eas.target
import eas.factor
import eas.boundary
import eas.selection
import numpy as np
from eas import PRO
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
times = 50  # 算法执行的总次数
gen = 3000  # 3000  # 一次算法的迭代次数
_np = 60  # 60  # 总群个体的数量
n = 10  # 10  # 解向量的维数
# 向量越界策略
boundary_strategy = eas.boundary.Boundary.BOUNDARY
# 目标函数，其最优解为 100
fitness_func = eas.target.f1

# PRO 参数项
upperxs = np.array([100] * n) # 向量各分量上限
lowerxs = np.array([-100] * n) # 向量各分量下限
ls = 3 # 分组要求，群体每次分成 3 组
eas.LabelSolution.LABEL_SIZE = 3  # PRO 中解向量类需要共享组数信息
eas.LabelSolution.GEN = gen  # PRO 中解向量需要共享迭代数信息

# 开始
time_str = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
log_file = open(
    './storages/logs/PRO-%s-%s.tsv' % (func_key, time_str),
    mode='ab')

for i in range(times):
    print('round %d start: ' % (i + 1))
    # 由于因子有生成次数限制，所以需要在 times 循环体内重新创建
    factors = {
        # r1 r2 分别为在 rating_phase 使用到的两个因子
        # 每一次迭代中返回 [-1.0, 1.0] 区间的随机数
        'r1': eas.factor.RandomMatrixFactor([-1, 1.0], gen, n),
        'r2': eas.factor.RandomMatrixFactor([-1, 1.0], gen, n),
        # 'r1': eas.factor.RandomFactor([0, 1.0], gen),
        # 'r2': eas.factor.RandomFactor([0, 1.0], gen),
    }

    algo = PRO(_np, n, upperxs, lowerxs,
               label_size=ls,
               factors=factors,
               optimal_minimal=True,
               fitness_func=fitness_func,
               boundary_strategy=boundary_strategy,
               solution_class='LabelSolution')

    algo.fit(gen)
    np.savetxt(log_file, np.array(algo.best_fitness_store).T[np.newaxis], delimiter=',')

    print('round %d end: ' % (i + 1))

log_file.close()

# data = np.loadtxt(
#     './storages/logs/PRO-%s-%s.tsv' % (func_key, time_str),
#     dtype=float,
#     delimiter=','
# )
#
# plt.plot(np.linspace(1, 3000, 3000), np.vectorize(math.log10)(data.mean(axis=0)),
#          label='PRO-%s' % func_key)
# plt.title(func_key)
# plt.xlabel('gen')
# plt.ylabel('log10(%s)' % func_key)
# plt.legend()
# plt.savefig('./storages/graphs/m/PRO-%s-%s.png' % (func_key, time_str), dpi=1280)
# plt.show()
