import numpy as np
import matplotlib.pyplot as plt
from methods import (
    lagrange_interpolation,
    newton_divided_diff_interpolation
)


def plot_interpolation(x, y):
    """Построение графиков интерполяции"""
    if len(x) < 2:
        print("Недостаточно точек для построения графика")
        return

    x_vals = np.linspace(min(x), max(x), 100)
    y_lagrange = [lagrange_interpolation(x, y, xi) for xi in x_vals]
    y_newton = [newton_divided_diff_interpolation(x, y, xi) for xi in x_vals]

    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, color='red', label='Узлы интерполяции')
    plt.plot(x_vals, y_lagrange, label='Многочлен Лагранжа')
    plt.plot(x_vals, y_newton, '--', label='Многочлен Ньютона')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Интерполяция функции')
    plt.legend()
    plt.grid()
    plt.show()