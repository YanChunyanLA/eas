import os
import numpy as np
import json

log_dir = './storages/logs'

filenames = [filename for filename in os.listdir(log_dir) if not filename.startswith('.')]

algorithms = [
    'ABC',
    'DE',
    'GA',
    'HRO',
    'PRO',
    'PSO'
]


def filter_log_file(filenames, algorithm, function):
    return list(filter(lambda f: f.startswith(algorithm + '-' + function),filenames))[0]


functions = ['f' + str(i) for i in range(1, 12)]

result = {}

for function in functions:
    result[function] = {}
    for algorithm in algorithms:
        result[function][algorithm] = {}
        data = np.loadtxt(log_dir + '/' + filter_log_file(filenames, algorithm, function), dtype=float, delimiter=',')
        result[function][algorithm]['mean'] = np.mean(data[:, -1])
        result[function][algorithm]['best'] = np.min(data[:, -1])
        result[function][algorithm]['worst'] = np.max(data[:, -1])
        result[function][algorithm]['std'] = np.std(data[:, -1])

with open('stat.json', 'w') as f:
    json.dump(result, f, indent=2)