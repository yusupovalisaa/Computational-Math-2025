from input import input_data
from plot import plot_results
from output import print_results, save_to_file
from approximation import perform_approximation


def main():
    while True:
        # Ввод данных
        x, y = input_data()

        # Выполнение аппроксимации
        results, best_result = perform_approximation(x, y)

        # Вывод результатов
        print_results(results, best_result)

        # Построение графиков
        plot_results(x, y, results, best_result)

        break


if __name__ == "__main__":
    main()