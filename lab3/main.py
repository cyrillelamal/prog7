import math
import timeit
from concurrent.futures import as_completed, ThreadPoolExecutor
from functools import partial
from typing import Union

import funcs


def integrate_async(f: callable, a: Union[int, float], b: Union[int, float], *, n_jobs=2, n_iter=1000):
    with ThreadPoolExecutor(n_jobs) as executor:
        spawn = partial(executor.submit, funcs.integrate, f, n_iter=n_iter // n_jobs)
        step = (b - a) / n_jobs
        fs = [spawn(a + i * step, a + (i + 1) * step) for i in range(n_jobs)]
        return sum(f.result() for f in as_completed(fs))


if __name__ == '__main__':
    t = timeit.timeit(
        lambda: funcs.integrate(math.atan, 0, math.pi / 2, n_iter=10 ** 5),
        number=100
    )
    print(f'Sync: {round(t, 5)}, s')

    t = timeit.timeit(
        lambda: integrate_async(math.atan, 0, math.pi / 2, n_iter=10 ** 5),
        number=100
    )
    print(f'Async: {round(t, 5)}, s')
