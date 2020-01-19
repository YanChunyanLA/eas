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

        self.GROUP_SIZE = int(self.np / 3)

    def get_factor_keys(self):
        return [
            'r1',
            'r2',
            'r3',
        ]

    def fit(self, gen):
        for _ in range(gen):
            # sort
            # maintainer restorer sterile
            self.solutions.sort(key=lambda s: s.apply_fitness_func(self.fitness_func))

            if not self.optimal_minimal:
                self.solutions.reverse()

            self.append_best_fitness()

            self.hybridization_stage()
            self.selfing_stage()
            self.renewal_stage()

    def hybridization_stage(self):
        factors = {
            'r1': self.factors['r1'].next(),
            'r2': self.factors['r2'].next(),
        }
        for i in range(2 * self.GROUP_SIZE, self.np):
            sterile_index = self.strategies['selection'](2 * self.GROUP_SIZE, self.np, size=1, excludes=[i])
            maintainer_index = self.strategies['selection'](0, self.GROUP_SIZE, size=1)

            trial_solution = BaseEA.__SOLUTION_CLASS__.zeros(self.n)
            trial_solution.vector = (factors['r1'] * self.solutions[sterile_index].vector + factors['r2'] * self.solutions[maintainer_index].vector) / (factors['r1'] + factors['r2'])

            trial_solution.amend_vector(self.upperxs, self.lowerxs, boundary_strategy=self.boundary_strategy)
            target_fitness = self.solutions[i].apply_fitness_func(self.fitness_func)
            trial_fitness = trial_solution.apply_fitness_func(self.fitness_func)
            
            if (self.optimal_minimal and trial_fitness < target_fitness) or (not self.optimal_minimal and trial_fitness > target_fitness):
                self.solutions[i] = trial_solution
            else:
                self.solutions[i].trial_increase()

    def selfing_stage(self):
        factor = self.factors['r3'].next()
        for i in range(self.GROUP_SIZE, 2 * self.GROUP_SIZE):
            restorer_index = self.strategies['selection'](self.GROUP_SIZE, 2 * self.GROUP_SIZE, size=1, excludes=[i])
            
            trial_solution = BaseEA.__SOLUTION_CLASS__.zeros(self.n)
            trial_solution.vector = factor * (self.solutions[0].vector - self.solutions[restorer_index].vector) + self.solutions[i].vector

            trial_solution.amend_vector(self.upperxs, self.lowerxs, boundary_strategy=self.boundary_strategy)
            target_fitness = self.solutions[i].apply_fitness_func(self.fitness_func)
            trial_fitness = trial_solution.apply_fitness_func(self.fitness_func)
            
            if (self.optimal_minimal and trial_fitness < target_fitness) or (not self.optimal_minimal and trial_fitness > target_fitness):
                self.solutions[i] = trial_solution

    def renewal_stage(self):
        for i in range(self.GROUP_SIZE, 2 * self.GROUP_SIZE):
            if self.solutions[i].is_exceed_trial():
                self.solutions[i] = Solution.create(self.n, self.upperxs, self.lowerxs)
