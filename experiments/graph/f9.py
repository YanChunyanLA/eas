import numpy as np
import matplotlib.pyplot as plt
import time
import math
import csv

log_dir = '../../storages/logs'
graph_dir = '../../storages/graphs'

log_files = {
    'ABC': 'ABC-function-09-2020-02-28-12-49-34-summary.tsv',
    'DE': 'DE-function-09-2020-02-28-13-16-42-summary.tsv',
    'GA': 'GA-function-09-2020-02-28-13-36-14-summary.tsv',
    'HRO': 'HRO-function-09-2020-02-28-13-45-26-summary.tsv',
    'PSO': 'PSO-function-09-2020-02-28-14-29-48-summary.tsv',
    'PRO': 'PRO-function-09-2020-02-28-14-09-58-summary.tsv',
}

fp = open('./tsv/f9.tsv', 'wt')
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
plt.ylabel('log10(f9)')
plt.legend()
plt.savefig(
    graph_dir + '/' + 'f9-' + time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())) + '-curve.png',
    dpi=1280
)
plt.show()