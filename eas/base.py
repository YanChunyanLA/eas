import numpy as np
import eas
from eas.factor import MatrixFactor
from .solution import SolutionFactory
from eas import helper
from eas.boundary import Boundary


class BaseEA(object):
    def __init__(self, _np, n, upperxs, lowerxs, factors, **kwargs):
        # 对每一个的个体进行初始化
        self.np = _np
        self.n = n
        # 初始化上下限
        self.upperxs = upperxs
        self.lowerxs = lowerxs
        # 对过程中需要用到的因子进行初始化
        self.factors = factors
        # 目标函数最优求解是否为最小值，True 最小，False 最大
        self.optimal_minimal = kwargs.get('optimal_minimal', True)
        self.boundary_strategy = kwargs.get('boundary_strategy', Boundary.BOUNDARY)
        # fitness_func就是最终需要求取的函数，或者说是优化的问题
        self.fitness_func = kwargs.get('fitness_func', lambda xs: None)

        # 第一次对所有的解的可行位置进行初始化，初始化一个解的工厂
        self.solution_factory = SolutionFactory(self.n, self.upperxs, self.lowerxs)  # TODO
        self.solution_class = kwargs.get('solution_class', 'Solution')

        helper.must_callable(self.fitness_func)

        # 对种群中的每一个的个体进行初始化
        self.solutions = [self.create_solution() for _ in range(self.np)]

        self.strategies = {}
        # 对每一的迭代的过程中的最优值和最优值的下标进行记录
        self.best_fitness_store = []
        self.current_fitness_store = []
        self.current_best_index = 0
        self.log_file = None

        helper.must_valid_dimension(self.n, self.upperxs, self.lowerxs)

    def create_solution(self, all_zero=False):
        return self.solution_factory.create(self.solution_class, all_zero=all_zero)

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
        """定义该方法的含义在于，告诉调用者必须传入包含相应 key 的因子
        :return:
        """
        raise NotImplementedError

    def fit(self, gen):
        raise NotImplementedError

    def append_best_fitness(self):
        """ 每一次迭代中，需要将最优适应值保存
        存入 self.best_fitness_store 列表中
        """
        # 计算每个可行解的fitness
        self.current_fitness_store = [s.apply_fitness_func(self.fitness_func) for s in self.solutions]
        # 根据输入的是最大值还是最小值，取最优值
        fitness = min(self.current_fitness_store) if self.optimal_minimal else max(self.current_fitness_store)
        # 获得最优值的下标
        self.current_best_index = self.current_fitness_store.index(fitness)

        if eas.log_flag:
            self.log_best_vector(self.solutions[self.current_best_index].vector, fitness)
        # 对每一代的最优的fitness进行记录
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
