from eas import EA
from copy import deepcopy
import numpy as np
import math


class PRO(EA):
    def __init__(self, *args, gnum: int = 3, nc: int = 8, **kwargs):
        """
        :param gnum: Group Number 分组个数
        :param nc: 评分最后允许的次数
        """
        super(PRO, self).__init__(*args, **kwargs)
        # group_num: Group Number 分组个数
        # 若分组个数为 3, 则评分从高到低依次为 1,2,3
        self.group_num = gnum
        # group_size: Group Size 组内个数
        self.group_size = self.np // self.group_num
        # max_limit_num: 连续考核垫底次数 >= max_limit_num 时
        # 该解向量需要重新生成
        self.max_limit_num = nc
        # assess_record: 用于保存考核信息
        # 垫底则对应分量加 1
        self.assess_record = np.zeros(self.np)
        # mean_solutions: 各解向量历史的平均值
        self.mean_solutions = deepcopy(self.sc)
        self._learn_rate_max = 2
        self._learn_rate_min = 0
        # learn_rate_seeds: 各解向量对应的生成学习率的随机种子
        # 重新生成解向量时，对应位置的随机种子需要重新生成
        self.learn_rate_seeds = self._learn_rate_max - \
                                (self._learn_rate_max - self._learn_rate_min) * \
                                np.random.random(self.np)

        # 2 -> 0
        self.a1g = lambda current_gen: 2 * (1 - current_gen / self.max_gen)
        # -1 -> -2
        self.a2g = lambda current_gen: -1 * (1 + current_gen / self.max_gen)

    def _reset_learn_rate_seed(self, i):
        self.learn_rate_seeds[i] = self._learn_rate_max - \
                                (self._learn_rate_max - self._learn_rate_min) * \
                                np.random.random()

    def _get_learn_rate(self, i, gen):
        """传入解向量下标和当前迭代次数，返回对应解向量的学习率
        在自我提升阶段使用
        """
        seed = self.learn_rate_seeds[i]
        return np.random.random() * (seed - math.exp(gen / self.max_gen * math.log(seed)))
        # return np.random.random() * (seed - seed * gen / self.max_gen)

    def rate_stage(self, g):
        """为每一个个体评分"""
        # self.sc 已排序
        start = self.group_size * (self.group_num - 1)
        for i in range(start, self.np):
            self.assess_record[i] += 1
            if self.assess_record[i] >= self.max_limit_num:  # 表示该位置解向量需要重新生成
                # 针对每一个分量
                for j in range(self.n):
                    r1, r2 = 2 * np.random.random(2) - 1
                    si = np.random.randint(0, self.group_size)
                    ai = np.random.randint(self.group_size, self.group_size * 2)
                    self.sc[i, j] = (r1 * self.sc[si][j] + r2 * self.sc[ai][j]) / (r1 + r2)
                # 越界处理
                self.sc[i] = self.bs(self.sc[i], self.ub, self.lb)
                self.assess_record[i] = 0
                self._reset_learn_rate_seed(i)

    def learn_stage(self, g):
        """组间学习"""
        for gi in range(self.group_num):
            """第 gi 组"""
            for gj in range(self.group_size):
                """第 gi 组的第 gj 个个体"""
                i = gi * self.group_size + gj  # 种群中的第 i 个
                s_copy = deepcopy(self.sc[i])
                r = self._get_learn_rate(i, g)

                for j in range(self.n):
                    # 随机选择一个组
                    rand_g = np.random.choice([gx for gx in range(self.group_num) if gx != gi])
                    # 随机选择该组中的两个解向量
                    i1, i2 = np.random.choice(np.arange(rand_g * self.group_size, (rand_g + 1) * self.group_size), 2)
                    rr = 2 * np.random.random() - 1
                    s_copy[j] = self.sc[0,j] + r * rr * (self.sc[i1,j] - self.sc[i2,j])

                s_copy = self.bs(s_copy, self.ub, self.lb)
                if not self.better_than(i, s_copy):
                    self.sc[i] = s_copy

                # 重新计算历史平均
                self.mean_solutions[i] = (self.mean_solutions[i] * g + self.sc[i]) / (g + 1)

    def promote_stage(self, g):
        """提升阶段"""
        for i in range(self.np):
            r = self._get_learn_rate(i, g)
            s_new = deepcopy(self.sc[i])
            for j in range(self.n):
                rr = 2 * np.random.random() - 1
                s_new[j] += rr * r * (self.mean_solutions[i, j] - self.sc[i, j])

            s_new = self.bs(s_new, self.ub, self.lb)

            if not self.better_than(i, s_new):
                self.sc[i] = s_new

            # 重新计算历史平均
            self.mean_solutions[i] = (self.mean_solutions[i] * g + self.sc[i]) / (g + 1)

        A = 2 * self.a1g(g) * np.random.random() - self.a1g(g)
        if abs(A) > 1:
            self.hidden(g)

    def hidden(self, g):
        for i in range(self.np - 1, 0, -1):
            if np.random.random() > 0.8:
                s_copy = np.sum(self.sc, axis=0) / self.np * (2 * np.random.random() - 1)
                if not self.better_than(i, s_copy):
                    self.sc[i] = s_copy
                    self.mean_solutions[i] = (self.mean_solutions[i] * g + self.sc[i]) / (g + 1)

    def run(self, g):
        self.rate_stage(g)
        self.learn_stage(g)
        self.promote_stage(g)

    def sort(self):
        flag = 1 if self.optimal_minimal else -1
        self.fc = self.equip_procedure_all()
        sorted_indexes = np.argsort(flag * self.fc)
        self.sc = self.sc[sorted_indexes]
        self.mean_solutions = self.mean_solutions[sorted_indexes]
        self.assess_record = self.assess_record[sorted_indexes]
        self.fc = self.fc[sorted_indexes]
