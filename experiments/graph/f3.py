import numpy as np
import matplotlib.pyplot as plt
import time
import math
import csv

log_dir = '../../storages/logs'
graph_dir = '../../storages/graphs'

log_files = {
    'ABC': 'ABC-function-03-2020-02-26-22-49-45-summary.tsv',
    'DE': 'DE-function-03-2020-02-27-12-45-59-summary.tsv',
    'GA': 'GA-function-03-2020-02-27-13-07-01-summary.tsv',
    'HRO': 'HRO-function-03-2020-02-27-13-12-32-summary.tsv',
    'PSO': 'PSO-function-03-2020-02-27-14-34-46-summary.tsv',
    'PRO': 'PRO-function-03-2020-02-27-13-59-16-summary.tsv',
}

fp = open('./tsv/f3.tsv', 'wt')
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
    graph_dir + '/' + 'f3-' + time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())) + '-curve.png',
    dpi=1280
)
plt.show()