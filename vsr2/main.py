from multiprocessing import Pool
from timeit import timeit

import numpy as np


def mmul(matrix):
    for i in range(100):
        matrix = matrix * matrix
    return matrix


if __name__ == '__main__':
    matrices = []
    for i in range(4):
        matrices.append(np.random.random_integers(100, size=(1000, 1000)))

    print(timeit(lambda: map(mmul, matrices), number=20))

    pool = Pool(8)

    print(timeit(lambda: pool.map(mmul, matrices), number=20))
