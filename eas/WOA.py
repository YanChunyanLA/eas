# -*- coding:utf-8 -*-
# @Time : 2020/4/2 9:30
# @Author : a2htray
# @File : WOA.py
# @Desc : http://www.alimirjalili.com/WOA.html
import numpy as np
import math
from eas import EA


class WOA(EA):
    def __init__(self, *args, **kwargs):
        super(WOA, self).__init__(*args, **kwargs)
        # 2 -> 0
        self.a1g = lambda current_gen: 2 * (1 - current_gen / self.max_gen)
        # -1 -> -2
        self.a2g = lambda current_gen: -1 * (1 + current_gen / self.max_gen)

    def run(self, g):
        for i in range(self.np):
            r1, r2, r3, p = np.random.random(4)
            A = 2 * self.a1g(g) * r1 - self.a1g(g)
            C = 2 * r2
            b = 1
            l = (self.a2g(g) - 1) * r3 + 1

            for j in range(self.n):
                if p > 0.5:
                    if abs(A) >= 1:
                        rand_leader_index = math.floor(self.np * np.random.random())
                        X_rand = self.sc[rand_leader_index]
                        D_X_rand = abs(C * X_rand[j] - self.sc[i, j])
                        self.sc[i, j] = X_rand[j] - A * D_X_rand
                    else:
                        self.sc[i, j] = self.sc[0, j] - A * abs(C * self.sc[0, j] - self.sc[i, j])
                else:
                    self.sc[i, j] = abs(self.sc[0, j] - self.sc[i, j]) * math.exp(b * l) * math.cos(l * 2 * math.pi) + \
                                    self.sc[0, j]

            self.sc[i] = self.bs(self.sc[i], self.ub, self.lb)
