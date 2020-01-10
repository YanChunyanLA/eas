from eas.target import weierstrass, rosenbrock, griewank
import numpy as np

f1 = weierstrass(0.5, 3, 20)
f2 = rosenbrock
f3 = griewank

xss = np.random.uniform(-100, 100, size=(2, 10))

for xs in xss:
    print(f1(xs))

for xs in xss:
    print(f2(xs))

for xs in xss:
    print(f3(xs))