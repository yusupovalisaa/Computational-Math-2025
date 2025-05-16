import math
from solve import solve_slae
import numpy as np


def linear(xs, ys):
    n =len(xs)
    sx = sum(xs)
    sxx = sum(x ** 2 for x in xs)
    sy = sum(ys)
    sxy = sum(x * y for x, y in zip(xs, ys))
    a, b = solve_slae([[n, sx], [sx, sxx]], [sy, sxy], 2)
    print(sxy)
    return lambda x: a + b * x, [a, b]


def quadratic(xs, ys):
    n = len(xs)
    sx = sum(xs)
    sxx = sum(x ** 2 for x in xs)
    sxxx = sum(x ** 3 for x in xs)
    sxxxx = sum(x ** 4 for x in xs)
    sy = sum(ys)
    sxy = sum(x * y for x, y in zip(xs, ys))
    sxxy = sum(x ** 2 * y for x, y in zip(xs, ys))
    a, b, c = solve_slae(
        [[n, sx, sxx],
         [sx, sxx, sxxx],
         [sxx, sxxx, sxxxx]],
        [sy, sxy, sxxy],
        3
    )

    return lambda x: a + b * x + c * x ** 2, [a, b, c]


def cubic(xs, ys):
    n = len(xs)
    sx = sum(xs)
    sxx = sum(x ** 2 for x in xs)
    sxxx = sum(x ** 3 for x in xs)
    sxxxx = sum(x ** 4 for x in xs)
    sxxxxx = sum(x ** 5 for x in xs)
    sxxxxxx = sum(x ** 6 for x in xs)
    sy = sum(ys)
    sxy = sum(x * y for x, y in zip(xs, ys))
    sxxy = sum(x ** 2 * y for x, y in zip(xs, ys))
    sxxxy = sum(x ** 3 * y for x, y in zip(xs, ys))

    a, b, c, d = solve_slae(
        [
            [n, sx, sxx, sxxx],
            [sx, sxx, sxxx, sxxxx],
            [sxx, sxxx, sxxxx, sxxxxx],
            [sxxx, sxxxx, sxxxxx, sxxxxxx]
        ],
        [sy, sxy, sxxy, sxxxy],
        4
    )
    return lambda x: a + b * x + c * x ** 2 + d * x ** 3, [a, b, c, d]


def exponential(xs, ys):
    if any(y <= 0 for y in ys):
        raise ValueError("Экспоненциальная аппроксимация невозможна для y <= 0")
    log_ys = [math.log(y) for y in ys]
    fi, [a_log, b] = linear(xs, log_ys)
    a = math.exp(a_log)
    return lambda x: a * math.exp(b * x), [a, b]


def logarithmic(xs, ys):
    if any(x <= 0 for x in xs):
        raise ValueError("Логарифмическая аппроксимация невозможна для x <= 0")
    log_xs = [math.log(x) for x in xs]
    fi, [a, b] = linear(log_xs, ys)
    return lambda x: a * math.log(x) + b, [a, b]


def power(xs, ys):
    if any(x <= 0 for x in xs) or any(y <= 0 for y in ys):
        raise ValueError("Степенная аппроксимация невозможна для x <= 0 или y <= 0")
    log_xs = [math.log(x) for x in xs]
    log_ys = [math.log(y) for y in ys]
    fi, [a_log, b] = linear(log_xs, log_ys)
    a = math.exp(a_log)
    return lambda x: a * x ** b, [a, b]
def deviation(y_true, y_pred):
    return np.sqrt(np.mean((y_true - y_pred) ** 2))

def calculate_r_squared(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return 1 - ss_res / ss_tot if ss_tot != 0 else float('-inf')

def perform_approximation(x, y):
    """Запускает все методы аппроксимации и возвращает результаты"""
    methods = [
        ('Линейная', linear),
        ('Квадратичная', quadratic),
        ('Кубическая', cubic),
        ('Экспоненциальная', exponential),
        ('Логарифмическая', logarithmic),
        ('Степенная', power)
    ]

    results = []
    for name, func in methods:
        try:
            f, params = func(x, y)  # получить функцию и параметры
            y_pred = np.array([f(val) for val in x])  # рассчитать предсказанные значения
            dev = deviation(y, y_pred)  # стандартное отклонение ошибки
            r2 = calculate_r_squared(y, y_pred)  # коэффициент детерминации
            results.append({
                'name': name,
                'func': f,  # обёртка для plot_results
                'params': params,
                'deviation': dev,
                'r_squared': r2,
                'S': np.sum((y_pred - y) ** 2),
                'pearson': np.corrcoef(x, y_pred)[0, 1] if len(x) > 1 else None
            })
        except Exception as e:
            results.append({
                'name': name,
                'error': str(e)
            })

    # Отбор лучшего результата
    valid_results = [r for r in results if 'error' not in r]
    best_result = min(valid_results, key=lambda r: r['deviation']) if valid_results else None

    return results, best_result