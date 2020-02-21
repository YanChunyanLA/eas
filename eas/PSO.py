from .base import BaseEA


# paper
# Shi, Y., & Eberhart, R. C. (1999, July). Empirical study of particle swarm optimization.
# In Proceedings of the 1999 Congress on Evolutionary Computation-CEC99 (Cat. No. 99TH8406) (Vol. 3, pp. 1945-1950).
# IEEE.
class PSO(BaseEA):
    def __init__(self, _np, n, upperxs, lowerxs, uppervs, lowervs, factors, **kwargs):
        BaseEA.__init__(self, _np, n, upperxs, lowerxs, factors, **kwargs)
        self.uppervs = uppervs
        self.lowervs = lowervs

        # 初始化速度
        for i in range(self.np):
            self.solutions[i].set_velocity(uppervs=self.uppervs, lowervs=self.lowervs)

    def get_factor_keys(self):
        return [
            'w',
            'r1',
            'r2',
        ]

    def fit(self, gen):
        for i in range(gen):
            self.append_best_fitness()
            best_solution = self.solutions[self.current_best_index]

            w = self.factors['w'].generate(i)
            r1 = self.factors['r1'].generate(i)
            r2 = self.factors['r2'].generate(i)

            for j in range(self.np):
                self.solutions[j].update_velocity(best_solution.vector, w, r1, r2)
                self.solutions[j].amend_velocity(self.uppervs, self.lowervs, boundary_strategy=self.boundary_strategy)
                self.solutions[j].update_vector()
                self.solutions[j].amend_vector(self.upperxs, self.lowerxs, boundary_strategy=self.boundary_strategy)
                self.solutions[j].p_vector = self.compare(self.solutions[j].p_vector, self.solutions[j].vector)

    def compare(self, v1, v2):
        f1 = self.fitness_func(v1)
        f2 = self.fitness_func(v2)

        if (self.optimal_minimal and f1 < f2) or (not self.optimal_minimal and f1 > f2):
            return v1

        return v2
