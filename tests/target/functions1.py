import numpy as np
from eas import target

D = 10
o = np.array([1] * D)
xs = np.array([20] * D)


f = target.exp_sphere
print('exp_sphere', f(xs))
print('exp_sphere*', f(o))

f = target.exp_rastrigin
print('exp_rastrigin', f(xs))
print('exp_rastrigin*', f(o))

f = target.exp_ackley
print('exp_ackley', f(xs))
print('exp_ackley*', f(o))

f = target.exp_schwefel
print('exp_schwefel', f(xs))
print('exp_schwefel*', f(o))


f = target.exp_rosenbrock
print('exp_rosenbrock', f(xs))
print('exp_rosenbrock*', f(o))



