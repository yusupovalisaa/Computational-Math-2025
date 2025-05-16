import matplotlib.pyplot as plt


class Plotter:
    def plot_results(self, euler_results, rk4_results, adams_results, exact_solution=None):
        plt.figure(figsize=(12, 8))

        x_euler, y_euler = euler_results
        x_rk4, y_rk4 = rk4_results
        x_adams, y_adams = adams_results

        plt.plot(x_euler, y_euler, 'b-', label='Метод Эйлера', linewidth=2)
        plt.plot(x_rk4, y_rk4, 'g-', label='Рунге-Кутта 4 порядка', linewidth=2)
        plt.plot(x_adams, y_adams, 'r-', label='Метод Адамса', linewidth=2)

        # Если есть точное решение, строим его
        if exact_solution is not None:
            x_exact = x_rk4  # Используем точки метода Рунге-Кутта как наиболее точные
            y_exact = [exact_solution(x) for x in x_exact]
            plt.plot(x_exact, y_exact, 'k--', label='Точное решение', linewidth=2)

        plt.title('Сравнение численных методов решения ОДУ')
        plt.xlabel('x')
        plt.ylabel('y(x)')
        plt.legend()
        plt.grid(True)

        plt.show()