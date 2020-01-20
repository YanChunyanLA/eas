import numpy as np
import eas
from eas.factor import MatrixFactor
from .solution import SolutionFactory, Solution
from eas import helper
from eas.boundary import Boundary


class BaseEA(object):
    __SOLUTION_CLASS__ = Solution  # default solution derived from Solution

    def __init__(self, _np, n, upperxs, lowerxs, factors, **kwargs):
        self.np = _np
        self.n = n
        self.upperxs = upperxs
        self.lowerxs = lowerxs
        self.factors = factors
        self.optimal_minimal = kwargs.get('optimal_minimal', True)
        self.boundary_strategy = kwargs.get('boundary_strategy', Boundary.BOUNDARY)
        self.fitness_func = kwargs.get('fitness_func', lambda xs: None)

        self.solution_factory = SolutionFactory(self.n, self.upperxs, self.lowerxs)  # TODO
        self.solution_class = kwargs.get('solution_class', 'Solution')

        helper.must_callable(self.fitness_func)

        self.solutions = [self.solution_factory.create(self.solution_class) for _ in range(self.np)]
        self.strategies = {}
        self.best_fitness_store = []
        self.log_file = None

        helper.must_valid_dimension(self.n, self.upperxs, self.lowerxs)

    def set_fitness_func(self, fitness_func):
        helper.must_callable(fitness_func)
        self.fitness_func = fitness_func

    def set_log_file(self, log_file):
        self.log_file = log_file

    def check_factors(self):
        for k in self.get_factor_keys():
            if k not in self.factors:
                raise ValueError('lost the factor')

    def get_factor_keys(self):
        raise NotImplementedError

    def fit(self, gen):
        raise NotImplementedError

    def append_best_fitness(self):
        """每一次迭代中，需要将最优适应值保存
        存入 self.best_fitness_store 列表中
        """
        fitness_list = [s.apply_fitness_func(self.fitness_func) for s in self.solutions]
        fitness = min(fitness_list) if self.optimal_minimal else max(fitness_list)

        if eas.log_flag:
            self.log_best_vector(self.solutions[fitness_list.index(fitness)].vector, fitness)

        self.best_fitness_store.append(fitness)

    def get_factors(self):
        factors = []
        for key in self.factors.keys():
            factors.append(self.factors[key].next())
        return dict(zip(self.factors.keys(), factors))

    def register_strategy(self, key, strategy):
        self.strategies[key] = strategy

    def log_best_vector(self, best_vector, fitness):
        if self.log_file is None:
            raise ValueError('need to set log file, if you want to use log activities')
        np.savetxt(self.log_file, np.append(best_vector, [fitness], axis=0)[np.newaxis], delimiter=',')

    def compare(self, s, trial):
        f = s.apply_fitness_func(self.fitness_func)
        tf = trial.apply_fitness_func(self.fitness_func)

        if (self.optimal_minimal and tf < f) or (
                not self.optimal_minimal and tf > f):
            return trial, 1

        return s, -1

    @staticmethod
    def is_matrix_factor(factor):
        return MatrixFactor.is_matrix_factor(factor)

    def __del__(self):
        try:
            self.log_file.close()
        except:
            pass
