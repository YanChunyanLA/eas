import time
import eas.target
import eas.factor
import eas.boundary
import eas.selection
import numpy as np
from eas import ABC

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

# 参数项
upperxs = np.array([100] * n)  # 向量各分量上限
lowerxs = np.array([-100] * n)  # 向量各分量下限
eas.TrialSolution.TRIAL_LIMIT = 8  # ABC 个体检验的最大次数

# 开始
time_str = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
log_file = open(
    './storages/logs/ABC-function-01-%s-summary.tsv' % time_str,
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




