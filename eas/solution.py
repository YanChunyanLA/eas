import numpy as np
from eas import helper
from eas.boundary import Boundary
import random, math


class SolutionFactory(object):
    def __init__(self, n, upperxs, lowerxs, **kwargs):
        self.n = n
        self.upperxs = upperxs
        self.lowerxs = lowerxs
        self.kwargs = kwargs

    def create(self, class_str, all_zero=False):
        if class_str == 'TrialSolution':
            vector = np.zeros(self.n) if all_zero else helper.init_vector(self.n, self.upperxs, self.lowerxs)
            return TrialSolution(vector)


class Solution(object):
    def __init__(self, vector):
        self.vector = vector
        self.N = len(self.vector)
        self.mean_vector = self.vector

    @staticmethod
    def create(n, upperxs, lowerxs):
        return Solution(helper.init_vector(n, upperxs, lowerxs))

    @staticmethod
    def zeros(n):
        return Solution(np.zeros(n))
    
    def apply_fitness_func(self, fitness_func):
        return fitness_func(self.vector)

    def change_vector(self, vector, mean=False, gen=2):
        self.vector = vector

        if mean:
            self.mean_vector = (self.mean_vector * gen + self.vector) / (gen + 1)

    def amend_vector(self, upperxs, lowerxs, boundary_strategy=Boundary.BOUNDARY):
        self.vector = Boundary.make_strategy(boundary_strategy)(self.vector, upperxs, lowerxs)


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
    def create(n, upperxs, lowerxs):
        return TrialSolution(helper.init_vector(n, upperxs, lowerxs))

    @staticmethod
    def zeros(n):
        return TrialSolution(np.zeros(n))


class LabelSolution(Solution):
    LABEL_SIZE = 8
    GEN = 3000

    def __init__(self, vector):
        Solution.__init__(self, vector)
        self.labels = []
        self.learn_rate = random.random()
        self.seed = random.choice(list(range(1, LabelSolution.LABEL_SIZE)))

    def get_current_label(self):
        """at each iteration, instances of Label should invoke this method to 
        get the current label it got
        """
        return self.labels[LabelSolution.LABEL_SIZE - 1]
    
    def add_label(self, label):
        """give a label to a solution
        """
        self.labels.append(label)
        if len(self.labels) >= LabelSolution.LABEL_SIZE:
            self.labels = self.labels[1:]

    def should_be_fired(self):
        """check whether the solution should be fired
        """
        return len([label for label in self.labels if label == LabelSolution.LABEL_SIZE - 1]) == LabelSolution.LABEL_SIZE

    def get_learn_rate(self, gen):
        return self.learn_rate * (self.seed - math.exp(gen / LabelSolution.GEN * math.log(self.seed)))

    @staticmethod
    def create(n, upperxs, lowerxs):
        return LabelSolution(helper.init_vector(n, upperxs, lowerxs))

    @staticmethod
    def zeros(n):
        return LabelSolution(np.zeros(n))

    