# input_output_handler.py
import numpy as np
import math
from typing import Tuple, List, Dict

class InputOutputHandler:
    def __init__(self):
        self.functions = {
            1: ("sin(x)", math.sin),
            2: ("cos(x)", math.cos),
            3: ("exp(x)", math.exp),
            4: ("x^2", lambda x: x ** 2)
        }
        self.methods = {
            1: "Многочлен Лагранжа",
            2: "Многочлен Ньютона с разделенными разностями",
            3: "Многочлен Ньютона с конечными разностями",
            4: "Схема Стирлинга",
            5: "Схема Бесселя"
        }

    def get_input_choice(self) -> int:
        print("Выберите способ ввода данных:")
        print("1. Ввод с клавиатуры\n2. Чтение из файла\n3. Генерация по функции")
        while True:
            try:
                choice = int(input("Ваш выбор (1-3): "))
                if 1 <= choice <= 3:
                    return choice
                self.print_error("введите число от 1 до 3")
            except ValueError:
                self.print_error("введите целое число")

    def input_from_keyboard(self) -> Tuple[List[float], List[float]]:
        x, y = [], []
        while True:
            try:
                n = int(input("Введите количество точек (не менее 2): "))
                if n >= 2:
                    break
                self.print_error("должно быть не менее 2 точек")
            except ValueError:
                self.print_error("введите целое число")

        for i in range(n):
            while True:
                try:
                    x_val, y_val = map(float, input(f"Точка {i + 1}: ").strip().split())
                    x.append(x_val)
                    y.append(y_val)
                    break
                except ValueError:
                    self.print_error("введите два числа через пробел")
        return x, y

    def input_from_file(self) -> Tuple[List[float], List[float]]:
        while True:
            filename = input("Введите имя файла: ").strip()

            try:
                with open(filename, 'r') as f:
                    lines = [line.strip() for line in f.readlines() if line.strip()]

                # Пропускаем пустые строки
                lines = [line for line in lines if line]

                if not lines:
                    self.print_error("Файл пуст")
                    continue

                try:
                    num_points = int(lines[0])  # Первая строка - количество точек
                except ValueError:
                    self.print_error("Первая строка должна содержать целое число - количество точек")
                    continue

                if len(lines) - 1 != num_points:
                    self.print_error(f"Ожидается {num_points} точек, но найдено {len(lines) - 1}")
                    continue

                x, y = [], []

                for line in lines[1:]:  # Обрабатываем строки с данными
                    try:
                        parts = line.split()
                        if len(parts) != 2:
                            raise ValueError("Каждая строка должна содержать ровно 2 значения")

                        x_val = float(parts[0])
                        y_val = float(parts[1])
                        x.append(x_val)
                        y.append(y_val)
                    except ValueError as ve:
                        self.print_error(f"Ошибка в строке '{line}': {str(ve)}")
                        break

                if len(x) == num_points:
                    return x, y
                else:
                    self.print_error("Не удалось загрузить все точки")

            except FileNotFoundError:
                self.print_error(f"Файл '{filename}' не найден")
            except Exception as e:
                self.print_error(f"Ошибка при чтении файла: {str(e)}")

    def generate_from_function(self) -> Tuple[List[float], List[float]]:
        print("Доступные функции:")
        for num, (name, _) in self.functions.items():
            print(f"{num}. {name}")
        while True:
            try:
                func_num = int(input("Выберите номер функции: "))
                if func_num in self.functions:
                    break
                self.print_error("нет функции с таким номером")
            except ValueError:
                self.print_error("введите целое число")
        while True:
            try:
                a = float(input("Введите начало интервала: "))
                b = float(input("Введите конец интервала: "))
                if b > a:
                    break
                self.print_error("конец интервала должен быть больше начала")
            except ValueError:
                self.print_error("введите число")
        while True:
            try:
                n = int(input("Введите количество точек (не менее 2): "))
                if n >= 2:
                    break
                self.print_error("должно быть не менее 2 точек")
            except ValueError:
                self.print_error("введите целое число")

        x = np.linspace(a, b, n).tolist()
        y = [self.functions[func_num][1](xi) for xi in x]
        return x, y

    def get_interpolation_point(self) -> float:
        while True:
            try:
                return float(input("Введите значение x для интерполяции: "))
            except ValueError:
                self.print_error("введите число")

    def print_results(self, results: Dict[int, float]):
        print("\nРезультаты интерполяции:")
        for method_num, value in results.items():
            print(f"{method_num}. {self.methods[method_num]}: {value:.6f}")

    def print_error(self, message: str):
        print(f"Ошибка: {message}")

    def print_finite_diff_table(self, x: List[float], y: List[float], table: List[List[float]]):
        print("\nТаблица конечных разностей:")
        # Заголовки столбцов
        headers = ["x", "y"] + [f"Δ^{i}y" for i in range(1, len(table))]
        print("\t".join(f"{h:>10}" for h in headers))  # Выравнивание по правому краю

        for i in range(len(x)):
            # Вывод x и y
            row = [f"{x[i]:>10.4f}", f"{y[i]:>10.4f}"]
            # Вывод разностей (начиная с Δ^1y)
            for j in range(min(len(table) - 1, len(x) - i - 1)):
                row.append(f"{table[j][i]:>10.4f}")
            print("\t".join(row))