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
raw_or_log10 = math.log10 if sys.argv[2] == '1' else lambda x: x

for (algo, file) in log_files[func_key].items():
    print(algo, file)

    data = np.loadtxt(log_dir + '/' + file, dtype=float, delimiter=',')
    plt.plot(np.linspace(1, 3000, 3000), [raw_or_log10(v) for v in data.mean(axis=0)], label=algo)

plt.title(func_key)
plt.legend()
plt.xlabel('gen')
plt.ylabel('log10(%s)' % func_key)
plt.savefig('%s/summary-%s-%s.png' %
            (graph_dir, func_key, time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))))
plt.show()