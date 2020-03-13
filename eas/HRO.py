from eas import BaseEA, selection
import random


# paper
# Ye, Zhiwei, Lie Ma, and Hongwei Chen. "A hybrid rice optimization algorithm.
# " 2016 11th International Conference on Computer Science & Education (ICCSE). 
# IEEE, 2016.
class HRO(BaseEA):
    def __init__(self, _np, n, upperxs, lowerxs, factors, **kwargs):
        BaseEA.__init__(self, _np, n, upperxs, lowerxs, factors, **kwargs)
        BaseEA.check_factors(self)

        if self.np % 3 != 0:
            raise ValueError('in HRO, NP must be divisible by 3')

        self.group_size = int(self.np / 3)

    def get_factor_keys(self):
        return [
            'r1',
            'r2',
            'r3',
        ]

    def fit(self, gen):
        for _ in range(gen):
            self.append_best_fitness()

            # sort
            # maintainer restorer sterile
            self.solutions.sort(key=lambda s: s.apply_fitness_func(self.fitness_func))

            if not self.optimal_minimal:
                self.solutions.reverse()

            self.hybridization_stage()
            self.selfing_stage()
            self.renewal_stage()

    def hybridization_stage(self):
        for i in range(2 * self.group_size, self.np):
            trial_solution = self.create_solution(all_zero=True)
            for j in range(self.n):
                r1 = random.random()
                r2 = random.random()
                sterile_index = selection.random(2 * self.group_size, self.np, size=1, excludes=[i])
                maintainer_index = selection.random(0, self.group_size, size=1)

                trial_solution.vector[j] = (r1 * self.solutions[sterile_index].vector[j] + r2 * self.solutions[maintainer_index].vector[j]) / \
                                           (r1 + r2)
                trial_solution.amend_component(j, self.upperxs[j], self.lowerxs[j], boundary_strategy=self.boundary_strategy)

            self.solutions[i], lost = self.compare(self.solutions[i], trial_solution)
            if lost == -1:
                self.solutions[i].trial_increase()

    def selfing_stage(self):
        for i in range(self.group_size, 2 * self.group_size):
            trial_solution = self.solution_factory.create(self.solution_class, all_zero=True)
            for j in range(self.n):
                restorer_index = selection.random(self.group_size, 2 * self.group_size, size=1, excludes=[i])
                r3 = random.random()
                trial_solution.vector[j] = r3 * (self.solutions[0].vector[j] - self.solutions[restorer_index].vector[j]) + self.solutions[i].vector[j]
                trial_solution.amend_component(j, self.upperxs[j], self.lowerxs[j], boundary_strategy=self.boundary_strategy)

            self.solutions[i], _ = self.compare(self.solutions[i], trial_solution)

    def renewal_stage(self):
        for i in range(self.group_size, 2 * self.group_size):
            if self.solutions[i].is_exceed_trial():
                self.solutions[i] = self.solution_factory.create(self.solution_class)
