import numpy as np
import eas

class Solution(object):
    def __init__(self, vector):
        self.vector = vector
        self.N = len(self.vector)

    @staticmethod
    def create(N, U, L):
        random_diag = np.diag(np.random.uniform(0, 1, N))
        vector = L + np.matmul(random_diag, U - L)
        return Solution(vector)

    @staticmethod
    def zeros(N):
        return Solution(np.zeros(N))
    
    def apply_fitness_func(self, fitness_func):
        return fitness_func(self.vector)

    def change_vector(self, vector):
        self.vector = vector

    def amend_vector(self, U, L):
        func = getattr(self, '_use_' + eas.boundary_strategy_flag)
        func(U, L)

    def _use_boundary(self, U, L):
        for i in range(self.N):
            if self.vector[i] > U[i]:
                self.vector[i] = U[i]
            if self.vector[i] < L[i]:
                self.vector[i] = L[i]

    def _use_middle(self, U, L):
        for i in range(self.N):
            if self.vector[i] > U[i] or self.vector[i] < L[i]:
                self.vector[i] = (U[i] + L[i]) / 2.0
    
    def _use_random(self, U, L):
        for i in range(self.N):
            if self.vector[i] > U[i] or self.vector[i] < L[i]:
                self.vector[i] = L[i] + random.random() * (U[i] - L[i])

class TrialSolution(Solution):
    TRIAL_LIMIT = 8

    def __init__(self, vector):
        Solution.__init__(self, vector)
        self.trial = 0

    def trial_increase(self):
        self.trial += 1
    
    def trial_zero(self):
        self.trial = 0

    def is_exceed_trial(self):
        return self.trial >= TrialSolution.TRIAL_LIMIT

    @staticmethod
    def create(N, U, L):
        random_diag = np.diag(np.random.uniform(0, 1, N))
        vector = L + np.matmul(random_diag, U - L)
        return TrialSolution(vector)

    @staticmethod
    def zeros(N):
        return TrialSolution(np.zeros(N))