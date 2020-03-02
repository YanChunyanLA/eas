import numpy as np
import matplotlib.pyplot as plt
import time
import math
import csv

log_dir = '../../storages/logs'
graph_dir = '../../storages/graphs'

log_files = {
    'ABC': 'ABC-function-06-2020-02-27-18-06-35-summary.tsv',
    'DE': 'DE-function-06-2020-02-27-18-43-43-summary.tsv',
    'GA': 'GA-function-06-2020-02-27-19-12-46-summary.tsv',
    'HRO': 'HRO-function-06-2020-02-27-19-19-02-summary.tsv',
    'PSO': 'PSO-function-06-2020-02-27-19-48-01-summary.tsv',
    'PRO': 'PRO-function-06-2020-02-27-19-32-53-summary.tsv',
}

fp = open('./tsv/f6.tsv', 'wt')
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
    plt.plot(np.linspace(1, 3000, 3000), [v for v in data.mean(axis=0)], label=algo)

fp.close()

plt.ylabel('gen')
plt.ylabel('log10(f6)')
plt.legend()
plt.savefig(
    graph_dir + '/' + 'f6-' + time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())) + '-curve.png',
    dpi=1280
)
plt.show()