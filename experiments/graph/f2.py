import numpy as np
import matplotlib.pyplot as plt
import time
import math
import csv

log_dir = '../../storages/logs'
graph_dir = '../../storages/graphs'

log_files = {
    'ABC': 'ABC-function-02-2020-02-26-18-26-50-summary.tsv',
    'DE': 'DE-function-02-2020-02-26-20-16-02-summary.tsv',
    'GA': 'GA-function-02-2020-02-26-20-34-40-summary.tsv',
    'HRO': 'HRO-function-02-2020-02-26-20-39-35-summary.tsv',
    'PSO': 'PSO-function-02-2020-02-26-21-26-55-summary.tsv',
    'PRO': 'PRO-function-02-2020-02-26-21-00-53-summary.tsv',
}

fp = open('./tsv/f2.tsv', 'wt')
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
plt.ylabel('log10(f2)')
plt.legend()
plt.savefig(
    graph_dir + '/' + 'f2-' + time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())) + '-curve.png',
    dpi=1280
)
plt.show()