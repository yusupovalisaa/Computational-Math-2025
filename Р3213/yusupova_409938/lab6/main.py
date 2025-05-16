from methods import EulerMethod, RungeKutta4Method, AdamsMethod, Runge_rule
from input_output_handler import InputOutputHandler
from plot import Plotter

def main():
    io_handler = InputOutputHandler()
    plotter = Plotter()

    # Получение входных данных от пользователя
    equation_choice, x0, y0, xn, h, epsilon, exact_solution = io_handler.get_input()

    # Инициализация методов
    euler = EulerMethod()
    rk4 = RungeKutta4Method()
    adams = AdamsMethod()

    # Решение уравнения выбранными методами
    methods = {
        '1': ('Метод Эйлера', euler.solve, 1),
        '2': ('Метод Рунге-Кутта 4 порядка', rk4.solve, 4),
        '3': ('Метод Адамса', adams.solve, None)
    }

    results = {}
    for method_num, (method_name, solver, order) in methods.items():
        x_values, y_values = solver(equation_choice, x0, y0, xn, h)
        results[method_name] = (x_values, y_values)

        # Оценка точности
        if order is not None:  # Для одношаговых методов используем правило Рунге
            _, y_values_half = solver(equation_choice, x0, y0, xn, h / 2)
            error = Runge_rule(y_values[-1], y_values_half[-1], order)
        else:  # Для многошаговых методов сравниваем с точным решением
            if exact_solution:
                exact_values = [exact_solution(x) for x in x_values]
                error = max(abs(y - exact) for y, exact in zip(y_values, exact_values))
            else:
                error = float('nan')

        print(f"\n{method_name}:")
        print(f"Погрешность: {error:.6f}")

    # Вывод результатов в таблицу
    exact_values = [exact_solution(x) for x in results['Метод Эйлера'][0]] if exact_solution else None
    io_handler.print_results_table(
        results['Метод Эйлера'],
        results['Метод Рунге-Кутта 4 порядка'],
        results['Метод Адамса'],
        exact_values
    )

    # Построение графиков
    plotter.plot_results(
        results['Метод Эйлера'],
        results['Метод Рунге-Кутта 4 порядка'],
        results['Метод Адамса'],
        exact_solution
    )


if __name__ == "__main__":
    main()