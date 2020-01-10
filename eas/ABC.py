from .base import BaseEA
from eas import Solution, helper, TrialSolution
import numpy as np
import random

# paper
# Karaboga, Dervis, and Bahriye Basturk. "A powerful and efficient algorithm 
# for numerical function optimization: artificial bee colony (ABC) algorithm.
# " Journal of global optimization 39.3 (2007): 459-471.
class ABC(BaseEA):
    def __init__(self, NP, N, U, L, factors):
        BaseEA.__init__(self, NP, N, U, L, factors)
        BaseEA.check_factors(self)

    def get_factor_keys(self):
        return [
            'r1',
            'r2',
        ]

    def get_exceeded_trials(self):
        '''返回试验次数等于阈值的个体下标
        '''
        return [k for k, s in enumerate(self.solutions) if s.trial == TrialSolution.TRIAL_LIMIT]

    def fit(self, gen):
        for _ in range(gen):
            self.append_best_fitness()
            self.employee_stage()
            self.outlooker_stage()
            self.scouter_stage()

    def employee_stage(self):
        r_factor = self.factors['r1'].next()
        is_martirx_factor = BaseEA.is_matrix_factor(self.factors['r1'])

        for i in range(self.NP):
            selected_index = self.strategies['selection'](0, self.NP, size=1, excludes=[i])
            selected_solution = self.solutions[selected_index]
            trial_solution = BaseEA.__SOLUTION_CLASS__.zeros(self.N)
            trial_solution.vector = self.solutions[i].vector + helper.factor_multiply(is_martirx_factor, r_factor, selected_solution.vector)
            trial_solution.amend_vector(self.U, self.L)
            target_fitness = self.solutions[i].apply_fitness_func(self.fitness_func)
            trial_fitness = trial_solution.apply_fitness_func(self.fitness_func)
            
            if (self.is_minimal and trial_fitness < target_fitness) or (not self.is_minimal and trial_fitness > target_fitness):
                self.solutions[i] = trial_solution
                self.solutions[i].trial_zero()
            else:
                self.solutions[i].trial_increase()

    def outlooker_stage(self):
        fitness_list = np.array([s.apply_fitness_func(self.fitness_func) for s in self.solutions])
        fitness_sum = sum(fitness_list)
        probabilities = fitness_list / fitness_sum
        r_factor = self.factors['r2'].next()

        is_martirx_factor = BaseEA.is_matrix_factor(self.factors['r2'])

        for i in range(self.NP):
            # protect the original probabilities
            temp_probabilities = probabilities.copy()
            temp_probabilities[i] = 0

            selected_index = random.choices(list(range(self.NP)), temp_probabilities)[0]
            selected_solution = self.solutions[selected_index]

            trial_solution = BaseEA.__SOLUTION_CLASS__(np.zeros(self.N))
            trial_solution.vector = self.solutions[i].vector + helper.factor_multiply(is_martirx_factor, r_factor, selected_solution.vector)
            trial_solution.amend_vector(self.U, self.L)

            target_fitness = self.solutions[i].apply_fitness_func(self.fitness_func)
            trial_fitness = trial_solution.apply_fitness_func(self.fitness_func)
            
            if (self.is_minimal and trial_fitness < target_fitness) or (not self.is_minimal and trial_fitness > target_fitness):
                self.solutions[i] = trial_solution
                self.solutions[i].trial_zero()
            else:
                self.solutions[i].trial_increase()

    def scouter_stage(self):
        indexes = self.get_exceeded_trials()
        if len(indexes) != 0:
            for i in indexes:
                self.solutions[i] = BaseEA.__SOLUTION_CLASS__.create(self.N, self.U, self.L)
