from eas import BaseEA


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
        factors = {
            'r1': self.factors['r1'].next(),
            'r2': self.factors['r2'].next(),
        }
        for i in range(2 * self.group_size, self.np):
            sterile_index = self.strategies['selection'](2 * self.group_size, self.np, size=1, excludes=[i])
            maintainer_index = self.strategies['selection'](0, self.group_size, size=1)

            trial_solution = self.solution_factory.create(self.solution_class, all_zero=True)
            trial_solution.vector = (factors['r1'] * self.solutions[sterile_index].vector + factors['r2'] * self.solutions[maintainer_index].vector) / (factors['r1'] + factors['r2'])

            trial_solution.amend_vector(self.upperxs, self.lowerxs, boundary_strategy=self.boundary_strategy)

            self.solutions[i], lost = self.compare(self.solutions[i], trial_solution)
            if lost == -1:
                self.solutions[i].trial_increase()

    def selfing_stage(self):
        factor = self.factors['r3'].next()
        for i in range(self.group_size, 2 * self.group_size):
            restorer_index = self.strategies['selection'](self.group_size, 2 * self.group_size, size=1, excludes=[i])
            
            trial_solution = self.solution_factory.create(self.solution_class, all_zero=True)
            trial_solution.vector = factor * (self.solutions[0].vector - self.solutions[restorer_index].vector) + self.solutions[i].vector

            trial_solution.amend_vector(self.upperxs, self.lowerxs, boundary_strategy=self.boundary_strategy)
            self.solutions[i], _ = self.compare(self.solutions[i], trial_solution)

    def renewal_stage(self):
        for i in range(self.group_size, 2 * self.group_size):
            if self.solutions[i].is_exceed_trial():
                self.solutions[i] = self.solution_factory.create(self.solution_class)
