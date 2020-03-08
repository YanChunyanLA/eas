import os
import threading
from functools import reduce


class CmdThread(threading.Thread):
    def __init__(self, cmd):
        threading.Thread.__init__(self)
        self.cmd = cmd

    def run(self):
        os.system(self.cmd)


algorithms = [
    # 'ABC',
    # 'DE',
    'GA',
    'HRO',
    'PRO',
    'PSO'
]

functions = ['f' + str(i) for i in range(1, 12)]
cmds = reduce(lambda a, b: a + b, [list(map(lambda s: s + ' ' + f, map(lambda a: 'python experiments\\f\\' + a + '.py', algorithms))) for f in functions])

cmds.sort()

threads = [CmdThread(cmd) for cmd in cmds]

for thread in threads:
    thread.start()
    thread.join()

print('end')