from eas import helper, TrialSolution, BaseEA, selection
import numpy as np
import random


# paper
# Karaboga, Dervis, and Bahriye Basturk. "A powerful and efficient algorithm 
# for numerical function optimization: artificial bee colony (ABC) algorithm.
# " Journal of global optimization 39.3 (2007): 459-471.
class ABC(BaseEA):
    def __init__(self, _np, n, upperxs, lowerxs, factors, **kwargs):
        BaseEA.__init__(self, _np, n, upperxs, lowerxs, factors, **kwargs)
        BaseEA.check_factors(self)

    def get_factor_keys(self):
        return [
            'r1',
            'r2',
        ]

    def get_exceeded_trials(self):
        """返回试验次数等于阈值的个体下标
        """
        return [k for k, s in enumerate(self.solutions)
                if s.trial == TrialSolution.TRIAL_LIMIT]

    def fit(self, gen):
        for g in range(gen):
            self.append_best_fitness()

            self.employee_stage(g)
            self.onlooker_stage(g)
            self.scouter_stage(g)

    def employee_stage(self, gen):
        r_factor = self.factors['r1'].next()
        is_matrix_factor = BaseEA.is_matrix_factor(self.factors['r1'])

        for i in range(self.np):
            # 选择的个体下标
            selected_index = selection.random(0, self.np, size=1, excludes=[i])
            selected_solution = self.solutions[selected_index]

            trial_solution = self.create_solution(all_zero=True)
            trial_solution.vector = self.solutions[i].vector + helper.factor_multiply(is_matrix_factor, r_factor, selected_solution.vector)
            trial_solution.amend_vector(self.upperxs, self.lowerxs, boundary_strategy=self.boundary_strategy)

            self.solutions[i], lost = self.compare(self.solutions[i], trial_solution)

            if lost == 1:
                self.solutions[i].trial_zero()
            else:
                self.solutions[i].trial_increase()

    def onlooker_stage(self, gen):
        fitness_list = np.array([s.apply_fitness_func(self.fitness_func) for s in self.solutions])
        fitness_sum = sum(fitness_list)
        probabilities = fitness_list / fitness_sum
        r_factor = self.factors['r2'].next()

        is_matrix_factor = BaseEA.is_matrix_factor(self.factors['r2'])

        for i in range(self.np):
            # protect the original probabilities
            temp_probabilities = probabilities.copy()
            temp_probabilities[i] = 0

            selected_index = random.choices(list(range(self.np)), temp_probabilities)[0]
            selected_solution = self.solutions[selected_index]

            trial_solution = self.create_solution(all_zero=True)
            trial_solution.vector = self.solutions[i].vector + helper.factor_multiply(is_matrix_factor, r_factor, selected_solution.vector)
            trial_solution.amend_vector(self.upperxs, self.lowerxs, boundary_strategy=self.boundary_strategy)

            self.solutions[i], lost = self.compare(self.solutions[i], trial_solution)

            if lost == 1:
                self.solutions[i].trial_zero()
            else:
                self.solutions[i].trial_increase()

    def scouter_stage(self, gen):
        indexes = self.get_exceeded_trials()
        if len(indexes) != 0:
            for i in indexes:
                self.solutions[i] = self.solution_factory.create(self.solution_class)
