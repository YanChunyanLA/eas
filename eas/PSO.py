from .base import BaseEA
from eas import EA
import numpy as np
from eas.helper import init_vector
from copy import deepcopy


# paper
# Shi, Y., & Eberhart, R. C. (1999, July). Empirical study of particle swarm optimization.
# In Proceedings of the 1999 Congress on Evolutionary Computation-CEC99 (Cat. No. 99TH8406) (Vol. 3, pp. 1945-1950).
# IEEE.
class PSO(EA):
    def __init__(self, *args, vlb=None, vub=None, **kwargs):
        super(PSO, self).__init__(*args, **kwargs)
        self.vlb = vlb if vlb else ([-5] * self.n)
        self.vub = vub if vub else ([5] * self.n)

        self.vc = np.array([init_vector(self.n, self.vub, self.vlb) for _ in range(self.np)])
        # self.vcg = lambda cg: self.vc - self.vc * cg / self.max_gen
        # 记录每一个体的历史最优
        self.psc = deepcopy(self.sc)
        # 参数生成
        self.wg = lambda cg: 0.9 - cg * 0.4 / self.max_gen
        self.r1g = lambda: 0.05
        self.r2g = lambda: 0.05

    def run(self, g):
        w = self.wg(g)
        r1 = self.r1g()
        r2 = self.r2g()

        for i in range(self.np):
            # 更新速度
            # print(self.vc[i])
            for j in range(self.n):
                ir1, ir2 = np.random.random(2)
                # self.sc[0,j] 总是当前全局最优
                self.vc[i,j] = w * self.vc[i,j] + \
                             r1 * ir1 * (self.psc[i,j] - self.sc[i,j]) + \
                             r2 * ir2 * (self.sc[0,j] - self.sc[i,j])

            self.vc[i] = self.bs(self.vc[i], self.vub, self.vlb)

            s_new = self.sc[i] + self.vc[i]
            s_new = self.bs(s_new, self.ub, self.lb)

            if not self.better_than(i, s_new):
                self.sc[i] = s_new
            # 记录个体历史最优
            if not self.better_than(i, self.psc[i]):
                self.psc[i] = deepcopy(self.sc[i])

    def sort(self):
        flag = 1 if self.optimal_minimal else -1
        self.fc = self.equip_procedure_all()
        sorted_indexes = np.argsort(flag * self.fc)
        self.sc = self.sc[sorted_indexes]
        self.psc = self.psc[sorted_indexes]
        self.vc = self.vc[sorted_indexes]
        self.fc = self.fc[sorted_indexes]