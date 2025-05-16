from typing import List


def lagrange_interpolation(x, y, x_val):
    result = 0.0
    n = len(x)
    for i in range(n):
        term = y[i]
        for j in range(n):
            if i != j:
                term *= (x_val - x[j]) / (x[i] - x[j])
        result += term
    return result


def newton_divided_diff_interpolation(x, y, x_val):
    n = len(x)
    coef = y.copy()

    # Вычисление коэффициентов разделенных разностей
    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            coef[i] = (coef[i] - coef[i - 1]) / (x[i] - x[i - j])

    result = coef[-1]
    # Обратное вычисление полинома Ньютона
    for i in range(n - 2, -1, -1):
        result = result * (x_val - x[i]) + coef[i]
    return result


def newton_finite_diff_interpolation(x, y, finite_diff_table, x_val):
    n = len(x)
    h = x[1] - x[0]
    t = (x_val - x[0]) / h
    result = y[0]
    term = 1.0

    for i in range(1, n):
        term *= (t - (i - 1)) / i
        result += term * finite_diff_table[i][0]
    return result


def stirling_interpolation(x, y, finite_diff_table, x_val):
    n = len(x)
    h = x[1] - x[0]
    # Центр таблицы
    center = n // 2
    t = (x_val - x[center]) / h

    result = y[center]
    term = 1.0
    factorial_term = 1

    for i in range(1, n):
        factorial_term *= i
        if i % 2 == 1:
            # Для нечётного порядка используем среднее значение конечных разностей
            term *= (t ** 2 - ((i - 1) / 2) ** 2)
            idx = (i + 1) // 2
            diff = (finite_diff_table[i][center - idx] + finite_diff_table[i][center - idx + 1]) / 2
        else:
            term *= t
            idx = i // 2
            diff = finite_diff_table[i][center - idx]
        result += (term / factorial_term) * diff
    return result


def bessel_interpolation(x, y, finite_diff_table, x_val):
    n = len(x)
    if n < 4 or n % 2 != 0:
        raise ValueError("Для схемы Бесселя требуется четное количество точек (минимум 4)")

    h = x[1] - x[0]
    mid = n // 2 - 1
    t = (x_val - x[mid]) / h - 0.5

    # Начальное значение как среднее двух центральных узлов
    result = (y[mid] + y[mid + 1]) / 2

    # Первая конечная разность
    term = t - 0.5
    result += term * finite_diff_table[1][mid]

    # Вторая конечная разность
    if n >= 4:
        term2 = term * (t + 0.5) / 2
        result += term2 * finite_diff_table[2][mid]

    # Третья конечная разность (при наличии достаточного количества точек)
    if n >= 6:
        term3 = term2 * (t - 0.5) / 3
        result += term3 * (finite_diff_table[3][mid] + finite_diff_table[3][mid - 1]) / 2

    return result
