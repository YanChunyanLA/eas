import numpy as np
import matplotlib.pyplot as plt
import time
import math

log_dir = '../../storages/logs'
graph_dir = '../../storages/graphs'

log_files = {
    'ABC': 'ABC-function-01-2020-02-26-15-27-39-summary.tsv',
    'DE': 'DE-function-01-2020-02-26-15-59-25-summary.tsv',
    'GA': 'GA-function-01-2020-02-24-14-31-05-summary.tsv',
    'HRO': 'HRO-function-01-2020-02-26-16-27-49-summary.tsv',
    'PSO': 'PSO-function-01-2020-02-26-17-00-34-summary.tsv',
    'PRO': 'PRO-function-01-2020-02-26-16-39-05-summary.tsv',
}

plt.figure(1)

for algo, file in log_files.items():
    data = np.loadtxt(log_dir + '/' + file, dtype=float, delimiter=',')
    print(algo)
    print('Mean', data[:, -1].mean())
    print('Best', data[:, -1].min())
    print('Worst', data[:, -1].max())
    print('Std', np.std(data[:, -1]))
    plt.plot(np.linspace(1, 3000, 3000), [math.log10(v) for v in data.mean(axis=0)], label=algo)

plt.ylabel('gen')
plt.ylabel('log10(f1)')
plt.legend()
plt.savefig(
    graph_dir + '/' + 'f1-' + time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())) + '-curve.png',
    dpi=1280
)
plt.show()