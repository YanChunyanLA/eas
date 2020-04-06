import numpy as np
from eas import EA
from eas.helper import init_vector
from copy import deepcopy


# paper
# Karaboga, Dervis, and Bahriye Basturk. "A powerful and efficient algorithm
# for numerical function optimization: artificial bee colony (ABC) algorithm.
# " Journal of global optimization 39.3 (2007): 459-471.
class ABC(EA):
    def __init__(self,  *args, nc: int = 8,**kwargs):
        super(ABC, self).__init__(*args, **kwargs)
        # 试验的最大次数
        self.nc = nc
        # 一维向量，记录各个解向量已试验的次数
        self.ncs = np.zeros(self.np)

    def sort(self):
        flag = 1 if self.optimal_minimal else -1
        self.fc = self.equip_procedure_all()
        tmp = np.column_stack((self.sc, self.ncs, self.fc))
        self.sc, self.ncs, self.fc = np.split(tmp[np.argsort(flag * tmp[:, -1])], [-2,-1], axis=1)

    def run(self, g):
        self.employee_stage(g)
        self.onlooker_stage(g)
        self.scouter_stage(g)

    def employee_stage(self, g):
        for i in range(self.np):
            for j in range(self.n):
                s_copy = deepcopy(self.sc[i])
                # r1 random number between [−1, 1]
                r1 = 1 - 2 * np.random.random()
                # Although
                # si is determined randomly, it has to be different from i.
                si = np.random.choice([x for x in range(self.np) if x != i])
                s_copy[j] = s_copy[j] + r1 * (s_copy[j] - self.sc[si][j])
                # In this work, the value of the parameter
                # exceeding its limit is set to its limit value.
                s_copy = self.bs(s_copy, self.ub, self.lb)

                if self.better_than(i, s_copy):  # 原先的好
                    self.ncs[i] += 1
                else:  # 新生的好
                    self.sc[i] = s_copy
                    self.ncs[i] = 0

    def onlooker_stage(self, g):
        ps = self.get_probabilities()
        for i in range(self.np):
            for j in range(self.n):
                s_copy = deepcopy(self.sc[i])
                r2 = 1 - 2 * np.random.random()
                si = np.random.choice(list(range(self.np)), p=ps)
                s_copy[j] = s_copy[j] + r2 * (s_copy[j] - self.sc[si][j])
                s_copy = self.bs(s_copy, self.ub, self.lb)
                if self.better_than(i, s_copy):  # 原先的好
                    self.ncs[i] += 1
                else:  # 新生的好
                    self.sc[i] = s_copy
                    self.ncs[i] = 0

    def scouter_stage(self, g):
        for i, nc in enumerate(self.ncs.flatten().astype(int)):
            if nc >= self.nc:
                self.sc[i] = init_vector(self.n, self.ub, self.lb)
                self.ncs[i] = 0
