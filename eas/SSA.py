# -*- coding:utf-8 -*-
# @Time : 2020/4/3 10:18
# @Author : a2htray
# @File : SSA.py
# @Desc : http://www.alimirjalili.com/SSA.html

from eas import EA
from math import exp
import numpy as np
from copy import deepcopy


class SSA(EA):
    def fit(self):
        self.sort()
        # 最好个体的下标
        bs = deepcopy(self.sc[0])
        # 最好个体的适应值
        fc = self.fc.flatten()[0]
        for g in range(2, self.max_gen + 1):
            self.hbsc.append(fc)
            c1 = 20 * exp(-(4 * g / self.max_gen)**2)

            for i in range(self.np):
                if i <= self.np / 2:
                    c2, c3 = np.random.random(2)
                    for j in range(self.n):
                        if c3 < 0.5:
                            self.sc[i,j] = bs[j] + c1 * ((self.ub[j] - self.lb[j]) * c2 + self.lb[j])
                        else:
                            self.sc[i, j] = bs[j] - c1 * ((self.ub[j] - self.lb[j]) * c2 + self.lb[j])
                else:
                    self.sc[i] = 1 / 2 * (self.sc[i] + self.sc[i - 1])

            for i in range(self.np):
                self.sc[i] = self.bs(self.sc[i], self.ub, self.lb)

                cfc = self.equip_procedure(self.sc[i])

                if (self.optimal_minimal and cfc < fc) or (not self.optimal_minimal and cfc > fc):
                    bs = deepcopy(self.sc[i])
                    fc = cfc

        self.hbsc.append(fc)
