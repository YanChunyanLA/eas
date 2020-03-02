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
        # 对可行解进行初始化
        vector = np.zeros(self.n) if all_zero else helper.init_vector(self.n, self.upperxs, self.lowerxs)
        _class = Solution
        if class_str == 'TrialSolution':
            _class = TrialSolution
        if class_str == 'LabelSolution':
            _class = LabelSolution
        if class_str == 'VelocitySolution':
            _class = VelocitySolution
        return _class(vector)


class Solution(object):
    def __init__(self, vector):
        self.vector = vector
        self.n = len(self.vector)
        self.mean_vector = self.vector
        self.fitness = None

    @staticmethod
    def create(n, upperxs, lowerxs):
        return Solution(helper.init_vector(n, upperxs, lowerxs))

    @staticmethod
    def zeros(n):
        return Solution(np.zeros(n))
    
    def apply_fitness_func(self, fitness_func):
        self.fitness = fitness_func(self.vector)
        return self.fitness

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


class LabelSolution(Solution):
    LABEL_SIZE = 8
    GEN = 3000

    def __init__(self, vector):
        Solution.__init__(self, vector)
        self.labels = []
        self.learn_rate = random.random()
        self.seed = random.choice(np.linspace(0.0001, 0.01, LabelSolution.LABEL_SIZE))

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


class VelocitySolution(Solution):
    def __init__(self, vector):
        super(VelocitySolution, self).__init__(vector)
        self.velocity = None
        self.p_vector = vector  # the previous best vector is the initial vector at first

    def set_velocity(self, **kwargs):
        if 'velocity' in kwargs:
            self.velocity = kwargs.get('velocity')

        if 'uppervs' in kwargs and 'lowervs' in kwargs:
            self.velocity = helper.init_vector(self.n, kwargs['uppervs'], kwargs['lowervs'])

    def amend_velocity(self, uppervs, lowervs, boundary_strategy=Boundary.BOUNDARY):
        self.velocity = Boundary.make_strategy(boundary_strategy)(self.velocity, uppervs, lowervs)

    def update_velocity(self, best_vector, w, r1, r2):
        ir1 = random.random()
        ir2 = random.random()
        self.velocity = w * self.velocity + r1 * ir1 * (self.p_vector - self.vector) + \
            r2 * ir2 * (best_vector - self.vector)

    def update_vector(self):
        self.vector += self.velocity

