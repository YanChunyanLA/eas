import numpy as np
import matplotlib.pyplot as plt
import time
import math
import csv

log_dir = '../../storages/logs'
graph_dir = '../../storages/graphs'

log_files = {
    'ABC': 'ABC-function-05-2020-02-27-16-00-00-summary.tsv',
    'DE': 'DE-function-05-2020-02-27-16-34-12-summary.tsv',
    'GA': 'GA-function-05-2020-02-27-16-57-32-summary.tsv',
    'HRO': 'HRO-function-05-2020-02-27-17-03-46-summary.tsv',
    'PSO': 'PSO-function-05-2020-02-27-17-47-14-summary.tsv',
    'PRO': 'PRO-function-05-2020-02-27-17-18-42-summary.tsv',
}

fp = open('./tsv/f5.tsv', 'wt')
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
plt.ylabel('log10(f5)')
plt.legend()
plt.savefig(
    graph_dir + '/' + 'f5-' + time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())) + '-curve.png',
    dpi=1280
)
plt.show()