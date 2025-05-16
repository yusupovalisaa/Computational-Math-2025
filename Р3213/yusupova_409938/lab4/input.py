import numpy as np


def input_data():
    """Функция для ввода данных с проверкой корректности"""
    while True:
        print("\nВыберите способ ввода данных:")
        print("1 - Вручную")
        print("2 - Из файла")
        choice = input("Ваш выбор (1/2): ")

        if choice not in ['1', '2']:
            print("Ошибка: выберите 1 или 2")
            continue

        try:
            if choice == '1':
                return manual_input()
            else:
                return file_input()
        except Exception as e:
            print(f"Ошибка: {str(e)}")
            print("Попробуйте ещё раз")


def manual_input():
    """Ручной ввод данных"""
    while True:
        try:
            n = int(input("Введите количество точек (8-12): "))
            if n < 8 or n > 12:
                raise ValueError("Количество точек должно быть от 8 до 12")

            x, y = [], []
            for i in range(n):
                point = input(f"Точка {i + 1} (x y через пробел): ").split()
                if len(point) != 2:
                    raise ValueError("Нужно ввести 2 числа")
                x.append(float(point[0]))
                y.append(float(point[1]))
            return np.array(x), np.array(y)
        except ValueError as e:
            print(f"Ошибка ввода: {str(e)}")


def file_input():
    """Чтение данных из файла"""
    while True:
        try:
            filename = input("Введите имя файла: ")
            data = np.loadtxt(filename)
            if data.shape[1] != 2:
                raise ValueError("Файл должен содержать 2 столбца")
            if data.shape[0] < 8 or data.shape[0] > 12:
                raise ValueError("Должно быть 8-12 точек")
            return data[:, 0], data[:, 1]
        except Exception as e:
            print(f"Ошибка чтения файла: {str(e)}")