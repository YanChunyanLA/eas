import numpy as np
import random as rd

def random(start, end, size=2, excludes=None):
    l = list(range(start, end))
    if excludes is not None:
        l = [i for i in l if i not in excludes]
    
    res = rd.choices(l, k=size)
    if size == 1:
        return res[0]
    return res