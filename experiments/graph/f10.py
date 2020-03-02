import numpy as np
import matplotlib.pyplot as plt
import time
import math
import csv

log_dir = '../../storages/logs'
graph_dir = '../../storages/graphs'

log_files = {
    'ABC': 'ABC-function-10-2020-02-28-14-43-55-summary.tsv',
    'DE': 'DE-function-10-2020-02-28-15-09-49-summary.tsv',
    'GA': 'GA-function-10-2020-02-28-15-25-48-summary.tsv',
    'HRO': 'HRO-function-10-2020-02-28-15-30-15-summary.tsv',
    'PSO': 'PSO-function-10-2020-02-28-16-10-08-summary.tsv',
    'PRO': 'PRO-function-10-2020-02-28-15-51-42-summary.tsv',
}

fp = open('./tsv/f10.tsv', 'wt')
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
plt.ylabel('log10(f10)')
plt.legend()
plt.savefig(
    graph_dir + '/' + 'f10-' + time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())) + '-curve.png',
    dpi=1280
)
plt.show()