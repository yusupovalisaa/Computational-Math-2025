# input_output_handler.py
import math


class InputOutputHandler:
    def __init__(self):
        self.equations = {
            '1': {
                'text': "y' = x + y",
                'solution': lambda x0, y0, x: -x - 1 + (y0 + x0 + 1) * math.exp(x - x0)
            },
            '2': {
                'text': "y' = x^2 + y^2",
                'solution': None
            },
            '3': {
                'text': "y' = 2x - y",
                'solution': lambda x0, y0, x: 2 * x - 2 + (y0 - 2 * x0 + 2) * math.exp(-(x - x0))
            }
        }

    def get_input(self):
        """Получает входные данные от пользователя"""
        print("Доступные дифференциальные уравнения:")
        for num, eq in self.equations.items():
            print(f"{num}. {eq['text']}")

        while True:
            choice = input("Выберите уравнение (1-3): ")
            if choice in self.equations:
                break
            print("Неверный ввод. Попробуйте снова.")

        while True:
            try:
                x0 = float(input("Введите начальное значение x0: "))
                y0 = float(input(f"Введите начальное значение y0 = y({x0}): "))
                xn = float(input("Введите конечное значение xn: "))
                h = float(input("Введите шаг h: "))
                epsilon = float(input("Введите точность ε: "))

                if xn <= x0:
                    print("xn должно быть больше x0. Попробуйте снова.")
                    continue
                if h <= 0:
                    print("Шаг h должен быть положительным. Попробуйте снова.")
                    continue
                if epsilon <= 0:
                    print("Точность ε должна быть положительной. Попробуйте снова.")
                    continue

                break
            except ValueError:
                print("Неверный формат числа. Попробуйте снова.")

        # Формируем точное решение, если оно доступно
        exact_solution = None
        if self.equations[choice]['solution'] is not None:
            exact_solution = lambda x: self.equations[choice]['solution'](x0, y0, x)

        return choice, x0, y0, xn, h, epsilon, exact_solution

    def print_results_table(self, euler_results, rk4_results, adams_results, exact_results=None):
        """Выводит таблицу результатов"""
        x_euler, y_euler = euler_results
        x_rk4, y_rk4 = rk4_results
        x_adams, y_adams = adams_results

        print("\nРезультаты численного решения:")
        header = "| {:^10} | {:^15} | {:^15} | {:^15} |".format(
            "x", "Метод Эйлера", "Рунге-Кутта 4", "Метод Адамса")
        if exact_results:
            header = header[:-1] + "| {:^15} |".format("Точное решение")
        print(header)
        print("-" * len(header))

        max_len = max(len(x_euler), len(x_rk4), len(x_adams))
        for i in range(max_len):
            x = x_euler[i] if i < len(x_euler) else "-"
            euler_val = y_euler[i] if i < len(y_euler) else "-"
            rk4_val = y_rk4[i] if i < len(y_rk4) else "-"
            adams_val = y_adams[i] if i < len(y_adams) else "-"
            exact_val = exact_results[i] if exact_results and i < len(exact_results) else "-"

            row = "| {:^10.4f} | {:^15.6f} | {:^15.6f} | {:^15.6f} |".format(
                x if x != "-" else "-",
                euler_val if euler_val != "-" else "-",
                rk4_val if rk4_val != "-" else "-",
                adams_val if adams_val != "-" else "-")

            if exact_results:
                row = row[:-1] + " {:^15.6f} |".format(
                    exact_val if exact_val != "-" else "-")

            print(row)