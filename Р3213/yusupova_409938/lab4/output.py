def print_results(results, best_result):
    print("\nРЕЗУЛЬТАТЫ АППРОКСИМАЦИИ")

    for result in results:
        if 'error' in result:
            print(f"\n{result['name']}: {result['error']}")
            continue

        print(f"\n{result['name']} функция:")
        print(f"Параметры: {['%.4f' % p for p in result['params']]}")
        print(f"Мера отклонения S: {result['S']:.4f}")
        print(f"Среднеквадратичное отклонение (σ): {result['deviation']:.4f}")
        print(f"Коэффициент детерминации R²: {result['r_squared']:.4f}")

        if result['pearson'] is not None:
            print(f"Коэффициент корреляции Пирсона: {result['pearson']:.4f}")

        # Интерпретация R²
        r2 = result['r_squared']
        if r2 >= 0.9:
            print("Качество: Отличное (R² ≥ 0.9)")
        elif r2 >= 0.7:
            print("Качество: Хорошее (0.7 ≤ R² < 0.9)")
        elif r2 >= 0.5:
            print("Качество: Умеренное (0.5 ≤ R² < 0.7)")
        else:
            print("Качество: Слабое (R² < 0.5)")

    if best_result:
        print("\n" + "=" * 50)
        print(f"НАИЛУЧШАЯ АППРОКСИМАЦИЯ: {best_result['name']}")
        print(f"Среднеквадратичное отклонение: {best_result['deviation']:.4f}")
        print(f"R²: {best_result['r_squared']:.4f}")


def save_to_file(results, best_result, filename="results.txt"):
    """Сохранение результатов в файл"""
    with open(filename, 'w') as f:
        f.write("РЕЗУЛЬТАТЫ АППРОКСИМАЦИИ\n")
        f.write("=" * 50 + "\n")

        for result in results:
            if 'error' in result:
                f.write(f"\n{result['name']}: ОШИБКА - {result['error']}\n")
                continue

            f.write(f"\n{result['name']} функция:\n")
            f.write(f"Параметры: {['%.4f' % p for p in result['params']]}\n")
            f.write(f"Мера отклонения S: {result['S']:.4f}\n")
            f.write(f"Среднеквадратичное отклонение (σ): {result['deviation']:.4f}\n")
            f.write(f"Коэффициент детерминации R²: {result['r_squared']:.4f}\n")

            if result['pearson'] is not None:
                f.write(f"Коэффициент корреляции Пирсона: {result['pearson']:.4f}\n")

        if best_result:
            f.write("\n" + "=" * 50 + "\n")
            f.write(f"НАИЛУЧШАЯ АППРОКСИМАЦИЯ: {best_result['name']}\n")
            f.write(f"Среднеквадратичное отклонение: {best_result['deviation']:.4f}\n")
            f.write(f"R²: {best_result['r_squared']:.4f}\n")

    print(f"\nРезультаты сохранены в файл {filename}")