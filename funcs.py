from typing import Union


def integrate(f: callable, a: Union[int, float], b: Union[int, float], *, n_iter=1000) -> float:
    dx = (b - a) / n_iter

    area = 0
    x = a

    for _ in range(n_iter):
        area += dx * f(x)
        x += dx

    return round(area, 8)
