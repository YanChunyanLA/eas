# Usage
# python box.py {function}
# example: python box.py f1

import sys
import matplotlib.pyplot as plt
import numpy as np
import math
import time
import os

algorithms = [
    'ABC',
    'DE',
    'GA',
    'HRO',
    'PSO',
    'PRO'
]

functions = ['f' + str(i) for i in range(1, 12)]

log_dir = './storages/logs'
graph_dir = './storages/graphs'

filenames = [filename for filename in os.listdir(log_dir) if not filename.startswith('.')]

log_files = {}
for function in functions:
    log_files[function] = {}
    for algorithm in algorithms:
        log_files[function][algorithm] = list(filter(
            lambda filename: filename.startswith(algorithm + '-' + function),
            filenames))[0]

if len(sys.argv) < 2 or sys.argv[1] not in log_files.keys():
    exit()

func_key = sys.argv[1]
data = {}
for (algo, file) in log_files[func_key].items():
    print(algo, file)
    data[algo] = list(map(lambda d: d, np.loadtxt(log_dir + '/' + file, dtype=float, delimiter=',')[:,-1]))

colors = ['pink', 'lightblue', 'lightgreen', 'cyan', 'tan', 'blue']
box = plt.boxplot(data.values(), labels=data.keys(), patch_artist=True)

for patch, color in zip(box['boxes'], colors):
    patch.set_facecolor(color)

plt.title('%s Fitness Distribution' % func_key)
plt.xlabel('Algorithm')
plt.ylabel('f')
plt.savefig('%s/box-%s-%s.png' %
            (graph_dir, func_key, time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))))
# plt.show()