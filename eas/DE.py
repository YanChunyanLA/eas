from eas import EA
import numpy as np


# Differential Evolution Algorithm With Strategy
# Adaptation for Global Numerical Optimization
class DE(EA):
    def __init__(self, *args, **kwargs):
        super(DE, self).__init__(*args, **kwargs)
        self.fg = lambda cg: 0.9 - 0.9 * cg / self.max_gen
        self.crg = lambda cg: 0.3

    def run(self, g):
        f = self.fg(g)
        cr = self.crg(g)
        for i in range(self.np):
            # mutation
            # DE/rand-to-best/1
            si = np.random.choice([x for x in range(self.np) if x != i])
            # V solution
            vs = self.sc[i] + f * (self.sc[0] - self.sc[i]) + f * (self.sc[si] - self.sc[i])

            for j in range(self.n):
                if np.random.random() > cr:
                    vs[j] = self.sc[i,j]

            vs = self.bs(vs, self.ub, self.lb)

            if not self.better_than(i, vs):
                self.sc[i] = vs
