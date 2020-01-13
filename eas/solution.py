import numpy as np
import eas
from eas import helper
import random, math

class Solution(object):
    def __init__(self, vector):
        self.vector = vector
        self.N = len(self.vector)
        self.mean_vector = self.vector

    @staticmethod
    def create(N, U, L):
        return Solution(helper.init_vector(N, U, L))

    @staticmethod
    def zeros(N):
        return Solution(np.zeros(N))
    
    def apply_fitness_func(self, fitness_func):
        return fitness_func(self.vector)

    def change_vector(self, vector, mean=False, gen=2):
        self.vector = vector

        if mean == True:
            self.mean_vector = (self.mean_vector * gen + self.vector) / (gen + 1)

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
        return TrialSolution(helper.init_vector(N, U, L))

    @staticmethod
    def zeros(N):
        return TrialSolution(np.zeros(N))

class LabelSolution(Solution):
    LABEL_SIZE = 8
    GEN = 3000

    def __init__(self, vector):
        Solution.__init__(self, vector)
        self.labels = []
        self.learn_rate = random.random()
        self.seed = random.choice(list(range(1, LabelSolution.LABEL_SIZE)))

    def get_current_label(self):
        '''at each iteration, instances of Label should invoke this method to 
        get the current label it got
        '''
        return self.labels[LabelSolution.LABEL_SIZE - 1]
    
    def add_label(self, label):
        '''give a label to a solution
        '''
        self.labels.append(label)
        if len(self.labels) >= LabelSolution.LABEL_SIZE:
            self.labels = self.labels[1:]

    def should_be_fired(self):
        '''check whether the solution should be fired
        '''
        return len([label for label in self.labels if label == LabelSolution.LABEL_SIZE - 1]) == LabelSolution.LABEL_SIZE

    def get_learn_rate(self, gen):
        return self.learn_rate * (self.seed - math.exp(gen / LabelSolution.GEN * math.log(self.seed)))

    @staticmethod
    def create(N, U, L):
        return LabelSolution(helper.init_vector(N, U, L))

    @staticmethod
    def zeros(N):
        return LabelSolution(np.zeros(N))

    