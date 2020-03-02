import sys
import matplotlib.pyplot as plt
import numpy as np
import math
import time

log_dir = './storages/logs/m'
graph_dir = './storages/graphs/m'

log_files = {
    'f1': {
        'ABC': 'ABC-f1-2020-03-02-20-29-33.tsv',
        'DE': 'DE-f1-2020-03-02-20-40-54.tsv',
        'GA': 'GA-f1-2020-03-02-20-47-05.tsv',
        'HRO': 'HRO-f1-2020-03-02-20-48-19.tsv',
        'PSO': 'PSO-f1-2020-03-02-20-49-17.tsv',
        'PRO': 'PRO-f1-2020-03-02-20-51-30.tsv',
    },
    'f2': {
        'ABC': 'ABC-f2-2020-03-02-20-56-58.tsv',
        'DE': 'DE-f2-2020-03-02-20-58-09.tsv',
        'GA': 'GA-f2-2020-03-02-20-58-47.tsv',
        'HRO': 'HRO-f2-2020-03-02-20-59-16.tsv',
        'PSO': 'PSO-f2-2020-03-02-20-59-47.tsv',
        'PRO': 'PRO-f2-2020-03-02-21-01-46.tsv',
    },
    'f3': {
        'ABC': 'ABC-f3-2020-03-02-21-06-34.tsv',
        'DE': 'DE-f3-2020-03-02-21-09-46.tsv',
        'GA': 'GA-f3-2020-03-02-21-11-29.tsv',
        'HRO': 'HRO-f3-2020-03-02-21-12-10.tsv',
        'PSO': 'PSO-f3-2020-03-02-21-13-16.tsv',
        'PRO': 'PRO-f3-2020-03-02-21-14-17.tsv',
    },
    'f4': {
        'ABC': 'ABC-f4-2020-03-02-21-16-59.tsv',
        'DE': 'DE-f4-2020-03-02-21-17-52.tsv',
        'GA': 'GA-f4-2020-03-02-21-18-25.tsv',
        'HRO': 'HRO-f4-2020-03-02-21-18-44.tsv',
        'PSO': 'PSO-f4-2020-03-02-21-19-36.tsv',
        'PRO': 'HRO-f4-2020-03-02-21-18-44.tsv',
    },

    'f5': {
        'ABC': 'ABC-f5-2020-03-02-21-23-25.tsv',
        'DE': 'DE-f5-2020-03-02-21-25-04.tsv',
        'GA': 'GA-f5-2020-03-02-21-25-55.tsv',
        'HRO': 'HRO-f5-2020-03-02-21-26-33.tsv',
        'PSO': 'PSO-f5-2020-03-02-21-26-35.tsv',
        'PRO': 'PRO-f5-2020-03-02-21-28-12.tsv',
    },

    'f6': {
        'ABC': 'ABC-f6-2020-03-02-21-18-59.tsv',
        'DE': 'DE-f6-2020-03-02-21-55-49.tsv',
        'GA': 'GA-f6-2020-03-02-21-56-20.tsv',
        'HRO': 'HRO-f6-2020-03-02-21-56-46.tsv',
        'PSO': 'PSO-f6-2020-03-02-21-58-13.tsv',
        'PRO': 'PRO-f6-2020-03-02-21-57-21.tsv',
    },

    'f7': {
        'ABC': 'ABC-f7-2020-03-02-21-31-58.tsv',
        'DE': 'DE-f7-2020-03-02-21-32-13.tsv',
        'GA': 'GA-f7-2020-03-02-21-33-15.tsv',
        'HRO': 'HRO-f7-2020-03-02-21-33-25.tsv',
        'PSO': 'PSO-f7-2020-03-02-21-34-23.tsv',
        'PRO': 'PRO-f7-2020-03-02-21-34-32.tsv',
    },

    'f8': {
        'ABC': 'ABC-f8-2020-03-02-21-36-21.tsv',
        'DE': 'DE-f8-2020-03-02-21-36-31.tsv',
        'GA': 'GA-f8-2020-03-02-21-37-58.tsv',
        'HRO': 'HRO-f8-2020-03-02-21-38-30.tsv',
        'PSO': 'PSO-f8-2020-03-02-21-38-35.tsv',
        'PRO': 'PRO-f8-2020-03-02-21-39-48.tsv',
    },

    'f9': {
        'ABC': 'ABC-f9-2020-03-02-21-40-17.tsv',
        'DE': 'DE-f9-2020-03-02-21-40-50.tsv',
        'GA': 'GA-f9-2020-03-02-21-42-39.tsv',
        'HRO': 'HRO-f9-2020-03-02-21-42-48.tsv',
        'PSO': 'PSO-f9-2020-03-02-21-43-43.tsv',
        'PRO': 'PRO-f9-2020-03-02-21-43-50.tsv',
    },

    'f10': {
        'ABC': 'ABC-f10-2020-03-02-21-44-32.tsv',
        'DE': 'DE-f10-2020-03-02-21-45-14.tsv',
        'GA': 'GA-f10-2020-03-02-21-46-24.tsv',
        'HRO': 'HRO-f10-2020-03-02-21-46-31.tsv',
        'PSO': 'PSO-f10-2020-03-02-21-46-51.tsv',
        'PRO': 'PRO-f10-2020-03-02-21-47-04.tsv',
    },

    'f11': {
        'ABC': 'ABC-f11-2020-03-02-21-51-10.tsv',
        'DE': 'DE-f11-2020-03-02-21-51-54.tsv',
        'GA': 'GA-f11-2020-03-02-21-49-50.tsv',
        'HRO': 'HRO-f11-2020-03-02-21-49-44.tsv',
        'PSO': 'PSO-f11-2020-03-02-21-47-59.tsv',
        'PRO': 'PRO-f11-2020-03-02-21-48-03.tsv',
    },
}

if len(sys.argv) < 2 or sys.argv[1] not in log_files.keys():
    exit()

func_key = sys.argv[1]

for (algo, file) in log_files[func_key].items():
    print(algo, file)

    data = np.loadtxt(log_dir + '/' + file, dtype=float, delimiter=',')
    plt.plot(np.linspace(1, 3000, 3000), [math.log10(v) for v in data.mean(axis=0)], label=algo)

plt.title(func_key)
plt.legend()
plt.xlabel('gen')
plt.ylabel('log10(%s)' % func_key)
plt.savefig('%s/summary-%s-%s.png' %
            (graph_dir, func_key, time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))))
plt.show()