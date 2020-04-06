# -*- coding:utf-8 -*-
# @Time : 2020/3/31 13:14
# @Author: a2htray
# @File : BHRO.py
# @Desc：测试脚本

from eas import BHRO
from sklearn.datasets import \
    load_breast_cancer, load_wine, load_iris
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import MinMaxScaler
import numpy as np

german_data = np.loadtxt('./dataset/german.data-numeric')
australian_data = np.loadtxt('./dataset/australian.dat')


dataset = {
    'australian': (australian_data[:,0:-1], australian_data[:,-1]),
    'breast_cancer': load_breast_cancer(return_X_y=True),
    'german_numeric': (german_data[:,0:-1], german_data[:,-1]),
    'wine': load_wine(return_X_y=True),
    'iris': load_iris(return_X_y=True),
}

dimensions = dict(zip(dataset.keys(), [len(dataset[key][0][0]) for key in dataset.keys()]))

for key in dataset.keys():
    dataset[key] = {
        'XY': dataset[key],
        'dimensionNum': dimensions[key],
    }

# 数据的预处理
keys = list(dataset.keys())
for key in keys:
    scaler = MinMaxScaler()
    scaler.fit(dataset[key]['XY'][0])
    dataset['after_preprocess_' + key] = {
        'XY': (scaler.transform(dataset[key]['XY'][0]), dataset[key]['XY'][1]),
        'dimensionNum': dataset[key]['dimensionNum'],
    }

random_state = 42
_np = 60  # 种群个数
gen = 10
X, Y = load_breast_cancer(return_X_y=True)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.7, random_state=random_state)

for key in dataset.keys():
    n = dataset[key]['dimensionNum']
    X, Y = dataset[key]['XY']
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.7, random_state=random_state)

    def procedure(solution):
        clf = SVC(random_state=random_state)
        clf.fit(X_train.T[solution == 1].T, Y_train)
        return clf.score(X_test.T[solution == 1].T, Y_test)

    ea = BHRO(_np, n, procedure, 0.5, random_state=random_state)
    ea.fit(gen)

    print('-- %s' % key)
    print(ea.accuracies, ea.bsc[0])
