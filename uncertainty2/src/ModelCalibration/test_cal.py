import numpy as np
from compiler.ast import flatten
x = np.mat(np.random.rand(1, 4))
print x
print type(x)

xx = x.tolist()
print xx
print type(xx)

xxx = flatten(xx)
print xxx
print type(xxx)
print xxx[0]

xxxx = np.array(x)
print xxxx
print type(xxxx)

l = flatten(mat.tolist())

