# -*- coding:utf-8 -*-
# @Time : 2020/3/31 11:23
# @Author: a2htray
# @File : BHRO.py
# @Desc: HRO 算法的二进制版本

import numpy as np
import copy


def _one_or_zero(alpha):
    return 1 if np.random.random() >= alpha else 0


class BHRO:
    def __init__(self, _np: int, n: int, procedure: callable, alpha: float = 0.5, nc: int = 8, random_state: int = None):
        self.np = _np
        self.n = n
        self.procedure = procedure
        # one/zero generation factor
        # 随机数 >= alpha 返回 1
        # 随机数 < alpha 返回 0
        self.alpha = alpha
        # 试验次数
        # >= max_limit_num 则需要重新生成解
        self.nc = nc
        self.ncs = np.zeros(self.np)
        self.random_state = random_state
        if self.random_state:
            np.random.seed(self.random_state)
        # bsc: Binary Solution Collection
        # 解集合
        self.bsc = np.array([self.init_solution() for _ in range(self.np)])
        self.accuracies = None
        # group_size: group size
        self.gs = self.np // 3

    def init_solution(self):
        return np.array(self.must_one([_one_or_zero(self.alpha) for _ in range(self.n)]))

    def must_one(self, s):
        """向量分量到至少有一个 1"""
        if sum([x == 1 for x in s]) == 0:
            s[np.random.randint(0, self.n, 1)[0]] = 1
        return s

    def equip_procedure(self):
        self.accuracies = np.array([self.procedure(s) for s in self.bsc])

    def sort(self):
        self.equip_procedure()
        tmp = np.column_stack((self.bsc, self.accuracies, self.ncs))
        self.bsc, self.accuracies, self.ncs = np.split(tmp[np.argsort(-tmp[:, -2])], [-2, -1], axis=1)
        self.bsc = self.bsc.astype(dtype=int)
        self.accuracies = self.accuracies.flatten()
        self.ncs = self.ncs.flatten()

    def fit(self, gen):
        for i in range(gen):
            self.sort()
            # print(self.accuracies)
            self.hybridization_stage()
            self.selfing_stage()
            self.renewal_stage()

        self.sort()

    def hybridization_stage(self):
        """sterile line 操作
        基本操作单位：分量
        """
        for i in range(self.gs * 2, self.np):
            # s_copy: solution copy
            s_copy = copy.deepcopy(self.bsc[i])
            for j in range(self.n):
                r1, r2 = np.random.random(2)
                rr1 = r1 / (r1 + r2)
                rr2 = r2 / (r1 + r2)
                # mi: maintainer line index
                mi = np.random.randint(0, self.gs, size=1)[0]
                # si：sterile line index
                si = np.random.randint(self.gs, self.np // 3 * 2, size=1)[0]
                # maintainer line component
                mc = self.bsc[mi][j] if rr1 >= self.alpha else (1 - self.bsc[mi][j])
                # sc: sterile line component
                sc = self.bsc[si][j] if rr2 >= self.alpha else (1 - self.bsc[si][j])
                # print(mc, sc)
                # 异或
                s_copy[j] = mc^sc

            s_copy = self.must_one(s_copy)
            # 新测试解的准确率
            sca = self.procedure(s_copy)
            if sca > self.accuracies[i]:  # 新解优于旧解
                self.bsc[i] = s_copy
                self.accuracies[i] = sca
                self.ncs[i] = 0
            else:
                self.ncs[i] = self.ncs[i] + 1

    def selfing_stage(self):
        """restorer line 操作
        基本操作单位：分量
        """
        for i in range(self.gs, self.gs * 2):
            s_copy = copy.deepcopy(self.bsc[i])
            for j in range(self.n):
                r3 = np.random.random(1)[0]
                si = np.random.choice([ii for ii in range(self.gs, self.gs * 2) if ii != j], 1)[0]
                t = abs(self.bsc[0][j] - self.bsc[si][j])
                t = t if r3 >= self.alpha else (1 - t)
                s_copy[j] = t ^ s_copy[j]

            s_copy = self.must_one(s_copy)
            sca = self.procedure(s_copy)
            if sca > self.accuracies[i]:  # 新解优于旧解
                self.bsc[i] = s_copy
                self.accuracies[i] = sca
                self.ncs[i] = 0
            else:
                self.ncs[i] = self.ncs[i] + 1

    def renewal_stage(self):
        """restorer line 操作
        基本操作单位：分量
        """
        for i in range(self.gs, self.gs * 2):
            if self.ncs[i] >= self.nc:
                s = self.init_solution()

                sca = self.procedure(s)
                if sca > self.accuracies[i]:
                    self.bsc[i] = s
                    self.accuracies[i] = sca
                    self.ncs[i] = 0

