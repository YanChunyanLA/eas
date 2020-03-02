import numpy as np
import matplotlib.pyplot as plt
import time
import math
import csv

log_dir = '../../storages/logs'
graph_dir = '../../storages/graphs'

log_files = {
    'ABC': 'ABC-function-08-2020-02-27-22-16-05-summary.tsv',
    'DE': 'DE-function-08-2020-02-27-23-12-33-summary.tsv',
    'GA': 'GA-function-08-2020-02-27-23-48-37-summary.tsv',
    'HRO': 'HRO-function-08-2020-02-28-11-09-51-summary.tsv',
    'PSO': 'PSO-function-08-2020-02-28-12-12-32-summary.tsv',
    'PRO': 'PRO-function-08-2020-02-28-11-42-25-summary.tsv',
}

fp = open('./tsv/f8.tsv', 'wt')
writer = csv.writer(fp, delimiter='\t')
writer.writerow(['algo', 'mean', 'best', 'worst', 'std'])

for algo, file in log_files.items():
    data = np.loadtxt(log_dir + '/' + file, dtype=float, delimiter=',')
    writer.writerow([
        algo,
        data[:, -1].mean(),
        data[:, -1].min(),
        data[:, -1].max(),
        np.std(data[:, -1]),
    ])
    plt.plot(np.linspace(1, 3000, 3000), [math.log10(v) for v in data.mean(axis=0)], label=algo)

fp.close()

plt.ylabel('gen')
plt.ylabel('log10(f8)')
plt.legend()
plt.savefig(
    graph_dir + '/' + 'f8-' + time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())) + '-curve.png',
    dpi=1280
)
plt.show()