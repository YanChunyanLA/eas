# Usage
# python graph.py {function} {log value}
# example: python graph.py f1 6
#       log value: default 10

import sys
import matplotlib.pyplot as plt
import numpy as np
import math
import time
import os

algorithms = [
    # 'ABC',
    # 'DE',
    # 'GA',
    # 'HRO',
    'HRA'
    # 'PSO',
    # 'PRO'
]
line_styles = {
    'ABC': 'dashed',
    'DE': 'dotted',
    'GA': 'dashdot',
    'HRO': 'dotted',
    'PSO': 'dashed',
    'PRO': 'solid',
    'HRA': 'solid'
}
algo_styles = list(zip(algorithms, line_styles))

functions = ['f' + str(i) for i in range(1, 12)]
functions = ['f' + str(i) for i in range(2, 3)]

log_dir = './storages/logs'
graph_dir = './storages/graphs'

filenames = [filename for filename in os.listdir(log_dir) if not filename.startswith('.')]

log_files = {}
for function in functions:
    log_files[function] = {}
    for algorithm in algorithms:
        print(algorithm + '-' + function)
        log_files[function][algorithm] = list(filter(
            lambda filename: filename.startswith(algorithm + '-' + function),
            filenames))[0]

if len(sys.argv) < 2 or sys.argv[1] not in log_files.keys():
    exit()

func_key = sys.argv[1]


def _log_func(base):
    if base is None:
        return lambda x: x
    return lambda x: math.log(x, base)


if str(sys.argv[2]).upper() == 'NONE':
    base = None
else:
    base = int(sys.argv[2])

log_func = _log_func(base)

for (algo, file) in log_files[func_key].items():
    print(algo, file)

    data = np.loadtxt(log_dir + '/' + file, dtype=float, delimiter=',')
    plt.plot(
        np.linspace(1, 10000, 10000),
        [log_func(v) for v in data],
        linestyle=line_styles[algo],
        label=algo)

plt.title(func_key)
plt.legend()
plt.xlabel('gen')

plt.ylabel('log%d(%s)' % (int(sys.argv[2]), func_key) if base is not None else 'f(x)')
plt.savefig('%s/summary-%s-%s.png' %
            (graph_dir, func_key, time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))))
plt.show()