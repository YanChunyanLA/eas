from .base import BaseEA
import random
import copy


class GA(BaseEA):
    def __init__(self, _np, n, upperxs, lowerxs, factors, **kwargs):
        BaseEA.__init__(self, _np, n, upperxs, lowerxs, factors, **kwargs)
        BaseEA.check_factors(self)

    def get_factor_keys(self):
        return [
            'cr',
            'al'
        ]

    def fit(self, gen):
        # 算法的主体内容
        for i in range(gen):
            # 计算fitness，并且进行记录
            self.append_best_fitness()
            # 根据轮盘赌算子对种群中的个体进行选择
            self.roulette()
            # 变异
            self.mutation(i)
            # 交叉
            self.crossover(i)

    def roulette(self):
        """对种群中的个体进行选择
        :return:
        """
        roulette_list = copy.copy(self.current_fitness_store)

        # 对求最小值和最大值进行一个判断
        if self.optimal_minimal:
            # 如果是求最小值，就将数值倒过来
            for i, val in enumerate(roulette_list):
                if roulette_list[i] != 0:
                    roulette_list[i] = 1 / roulette_list[i]

        current_fitness_sum = sum(roulette_list)

        # 进行选择
        for i in range(self.np):
            if i != self.current_best_index:
                rand = random.uniform(0, current_fitness_sum)
                temp_roulette_rate = 0.0
                temp_j = 0

                for j, val in enumerate(roulette_list):
                    temp_roulette_rate += val

                    if rand < temp_roulette_rate:
                        temp_j = j
                        break

                # 将第i次循环选中的个体，赋值给第i个个体
                self.solutions[i].vector = copy.copy(self.solutions[temp_j].vector)

    def mutation(self, gen):
        """mutation 变异
        :return:
        """
        al = self.factors['al'].generate(gen)
        l = list(range(self.np))
        l.pop(self.current_best_index)

        for i in l:
            # 依条件需要变异的分量下标
            index = random.randint(0, self.n - 1)
            rand_probability = random.random()

            if rand_probability < al:
                self.solutions[i].vector[index] = random.uniform(self.lowerxs[index], self.upperxs[index])

    def crossover(self, gen):
        """crossover 交叉
        :return:
        """
        cr = self.factors['cr'].generate(gen)

        for i in range(0, self.np, 2):
            # 依条件需要交叉的分量下标
            index = random.randint(0, self.n - 1)
            rand_probability = random.random()

            if rand_probability < cr:
                self.solutions[i].vector[index], self.solutions[i+1].vector[index] = \
                                                       self.solutions[i+1].vector[index], self.solutions[i].vector[index]
