from .base import BaseEA


class PRO(BaseEA):
    def __init__(self, _np, n, upperxs, lowerxs, LABEL_SIZE, factors, **kwargs):
        BaseEA.__init__(self, _np, n, upperxs, lowerxs, factors, **kwargs)
        self.LABLE_SIZE = LABEL_SIZE
        self.GROUP_SIZE = int(self.np / self.LABLE_SIZE)

    def get_factor_keys(self):
        return [
            'r1',
            'r2',
        ]

    def fit(self, gen):
        for i in range(gen):
            self.append_best_fitness()
            self.rate_stage(i)
            self.learn_stage(i)
            self.promote_stage(i)
    
    def rate_stage(self, gen):
        self.solutions.sort(key=lambda s: s.apply_fitness_func(self.fitness_func))

        if not self.optimal_minimal:
            self.solutions.reverse()

        factors = self.get_factors()

        for i in range(self.LABLE_SIZE):
            for j in range(self.GROUP_SIZE):
                index = i * self.GROUP_SIZE + j

                self.solutions[index].add_label(i)

                if self.solutions[index].should_be_fired():
                    s_index = self.strategies['selection'](0, self.GROUP_SIZE, size=1, excludes=[index])
                    a_index = self.strategies['selection'](self.GROUP_SIZE, self.GROUP_SIZE * 2, size=1, excludes=[index])

                    new_solution = self.solution_factory.create(self.solution_class, all_zero=True)
                    new_solution.vector = (factors['r1'] * self.solutions[s_index].vector + factors['r2'] * self.solutions[a_index].vector) / (factors['r1'] + factors['r2'])
                    new_solution.amend_vector(self.upperxs, self.lowerxs, boundary_strategy=self.boundary_strategy)
                    new_solution.change_vector(new_solution.vector, mean=True, gen=gen)

                    self.solutions[index] = new_solution

    def learn_stage(self, gen):
        for i in range(self.LABLE_SIZE):
            for j in range(self.GROUP_SIZE):
                index = i * self.GROUP_SIZE + j
                s1 = None
                s2 = None

                if i == 0:
                    s1, s2 = self.strategies['selection'](0, self.GROUP_SIZE, size=2, excludes=[index])
                else:
                    s1, s2 = self.strategies['selection'](self.GROUP_SIZE * i, self.GROUP_SIZE * (i + 1), size=2, excludes=[index])
                
                trial_solution = self.solution_factory.create(self.solution_class, all_zero=True)
                trial_solution.vector = self.solutions[index].vector + self.solutions[index].get_learn_rate(gen) * (self.solutions[s1].vector - self.solutions[s2].vector)
                trial_solution.amend_vector(self.upperxs, self.lowerxs, boundary_strategy=self.boundary_strategy)
                trial_solution.change_vector(trial_solution.vector, mean=True, gen=gen)

                self.solutions[index], _ = self.compare(self.solutions[index], trial_solution)

    def promote_stage(self, gen):
        for i in range(self.np):
            learn_rate = self.solutions[i].get_learn_rate(gen)
            self.solutions[i].vector = self.solutions[i].vector + learn_rate * (self.solutions[i].mean_vector - self.solutions[i].vector)
            self.solutions[i].amend_vector(self.upperxs, self.lowerxs, boundary_strategy=self.boundary_strategy)
            self.solutions[i].change_vector(self.solutions[i].vector)