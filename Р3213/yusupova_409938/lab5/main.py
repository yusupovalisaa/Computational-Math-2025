# main.py
from input_output_handlers import InputOutputHandler
from methods import *
from finite_difference import calculate_finite_differences
from plot import plot_interpolation

class Interpolation:
    def __init__(self):
        self.io = InputOutputHandler()
        self.x = []
        self.y = []
        self.finite_diff_table = []

    def run(self):
        # Ввод данных
        input_choice = self.io.get_input_choice()
        if input_choice == 1:
            self.x, self.y = self.io.input_from_keyboard()
        elif input_choice == 2:
            self.x, self.y = self.io.input_from_file()
        else:
            self.x, self.y = self.io.generate_from_function()

        # Печать введённых данных
        print("\nВведённые данные:")
        for xi, yi in zip(self.x, self.y):
            print(f"x = {xi:.4f}, y = {yi:.4f}")

        # Таблица конечных разностей
        self.finite_diff_table = calculate_finite_differences(self.y)
        self.io.print_finite_diff_table(self.x, self.y, self.finite_diff_table)

        # Ввод точки интерполяции
        x_val = self.io.get_interpolation_point()

        # Вычисление
        results = {
            1: lagrange_interpolation(self.x, self.y, x_val),
            2: newton_divided_diff_interpolation(self.x, self.y, x_val),
            3: newton_finite_diff_interpolation(self.x, self.y, self.finite_diff_table, x_val)
        }

        try:
            if len(self.x) >= 3 and len(self.x) % 2 == 1:
                results[4] = stirling_interpolation(self.x, self.y, self.finite_diff_table, x_val)
            elif len(self.x) >= 4 and len(self.x) % 2 == 0:
                results[5] = bessel_interpolation(self.x, self.y, self.finite_diff_table, x_val)
            else:
                print("Для схем Стирлинга/Бесселя требуется не менее 3/4 точек соответственно")
        except Exception as e:
            self.io.print_error(f"Дополнительные методы: {e}")

        self.io.print_results(results)
        plot_interpolation(self.x, self.y)

if __name__ == "__main__":
    try:
        Interpolation().run()
    except Exception as e:
        print(f"Произошла ошибка: {e}")
