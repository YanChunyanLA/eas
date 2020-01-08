import eas.factor as factor

c = factor.ConstantFactor(0.4, 5)

for i in range(5):
    print(c.next())

r = factor.RandomFactor([0, 1], 5, has_direct=True)

for i in range(5):
    print(r.next())

l = factor.LinearFactor([0, 0.2], 10)

for i in range(10):
    print(l.next())

e = factor.ExpFactor([0, 2], 100)

for i in range(100):
    print(e.next())