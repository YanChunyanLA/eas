from eas import EA
import numpy as np
from math import floor
from copy import deepcopy


class GA(EA):
    def __init__(self, *args, **kwargs):
        super(GA, self).__init__(*args, **kwargs)
        self.fappend = False
        self.fsort = False

        self.mrg = lambda cg: 0.9 - 0.9 * cg / self.max_gen
        self.crg = lambda cg: 0.3
        self.per = 0.4
        self.best_i = 0
        self.best_s = 0
        self.best_f = 0

    def run(self, g):
        self.best_i, self.best_s, self.best_f = self.get_current()
        self.hbsc.append(self.best_f)

        self.roulette(g)
        self.mutation(g)
        self.crossover(g)

    def roulette(self, g):
        for i in range(1, self.np):
            if i == self.best_i:
                continue
            ri = np.random.choice(np.arange(self.np), p=self.get_probabilities())
            self.sc[i] = self.sc[ri][:]

    def mutation(self, g):
        self.fc = self.equip_procedure_all()
        mr = self.mrg(g)
        for i in range(1, self.np):
            if i == self.best_i:
                continue
            s_new = deepcopy(self.sc[i])
            if np.random.random() < mr:
                sj = floor(np.random.random() * self.n)
                s_new[sj] = np.random.uniform(self.lb[sj], self.ub[sj])

            if not self.better_than(i, s_new):
                self.sc[i] = s_new

    def crossover(self, g):
        cr = self.crg(g)
        for i in range(self.np):
            s_new = deepcopy(self.sc[i])
            if np.random.random() < cr:
                si = floor(np.random.random() * self.np)
                sj = floor(np.random.random() * self.n)
                s_new[sj] = self.sc[si,sj]

            if not self.better_than(i, s_new):
                self.sc[i] = s_new
