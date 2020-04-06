from eas import GA
from eas.target import fs
import sys
import matplotlib.pyplot as plt
from math import log10

random_state = 42
_np = 60  # 种群个数
n = 10
max_gen = 500

ea = GA(_np, n, [10] * n, [-10] * n,
        max_gen=max_gen,
        procedure=fs[sys.argv[1]],
        random_state=random_state)

ea.fit()
fig, ax = plt.subplots(1, 1)
ax.plot(list(range(max_gen)), [log10(x) for x in ea.hbsc], 'r')
plt.show()
