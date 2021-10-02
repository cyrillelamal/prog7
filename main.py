import math
import timeit

import funcs

t = timeit.timeit(
    lambda: funcs.integrate(math.atan, 0, math.pi / 2, n_iter=10 ** 5),
    number=100
)
print(f'{round(t, 5)}, s')
