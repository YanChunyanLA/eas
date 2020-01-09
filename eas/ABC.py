from .base import BaseEA
from eas import Solution
import numpy as np
import random

class ABC(BaseEA):
    def __init__(self, NP, N, U, L, TRIAL, factors):
        BaseEA.__init__(self, NP, N, U, L, factors)
        BaseEA.check_factors(self)
        self.TRIAL_LIMIT = TRIAL
        self.trials = [0] * self.NP

    def get_factor_keys(self):
        return [
            'r1',
            'r2'
        ]

    def trial_increase(self, i):
        self.trials[i] += 1
    
    def get_exceeded_trials(self):
        '''返回试验次数等于阈值的个体下标
        '''
        return [k for k, v in enumerate(self.trials) if v == self.TRIAL_LIMIT]

    def fit(self, gen):
        for _ in range(gen):
            self.append_best_fitness()
            self.employee_stage()
            self.outlooker_stage()
            self.scouter_stage()

    def employee_stage(self):
        r_factor = self.factors['r1'].next()
        for i in range(self.NP):
            selected_index = self.strategies['selection'](0, self.NP, size=1, excludes=[i])
            selected_solution = self.solutions[selected_index]

            trial_solution = Solution(np.zeros(self.N))

            trial_solution.vector = self.solutions[i].vector + np.matmul(r_factor, selected_solution.vector)
            trial_solution.amend_vector(self.U, self.L)
            target_fitness = self.solutions[i].apply_fitness_func(self.fitness_func)
            trial_fitness = trial_solution.apply_fitness_func(self.fitness_func)
            
            if (self.is_minimal and trial_fitness < target_fitness) or (not self.is_minimal and trial_fitness > target_fitness):
                self.solutions[i] = trial_solution
                self.trials[i] = 0
            else:
                self.trial_increase(i)

    def outlooker_stage(self):
        fitness_list = np.array([s.apply_fitness_func(self.fitness_func) for s in self.solutions])
        fitness_sum = sum(fitness_list)
        probabilities = fitness_list / fitness_sum
        r_factor = self.factors['r2'].next()

        for i in range(self.NP):
            temp_probabilities = probabilities.copy()
            temp_probabilities[i] = 0
            selected_index = random.choices(list(range(self.NP)), temp_probabilities)[0]
            selected_solution = self.solutions[selected_index]

            trial_solution = Solution(np.zeros(self.N))

            trial_solution.vector = self.solutions[i].vector + np.matmul(r_factor, selected_solution.vector)
            trial_solution.amend_vector(self.U, self.L)
            target_fitness = self.solutions[i].apply_fitness_func(self.fitness_func)
            trial_fitness = trial_solution.apply_fitness_func(self.fitness_func)
            
            if (self.is_minimal and trial_fitness < target_fitness) or (not self.is_minimal and trial_fitness > target_fitness):
                self.solutions[i] = trial_solution
                self.trials[i] = 0
            else:
                self.trial_increase(i)

    def scouter_stage(self):
        indexes = self.get_exceeded_trials()
        if len(indexes) != 0:
            for i in indexes:
                self.solutions[i] = Solution.create(self.N, self.U, self.L)
                self.trials[i] = 0
