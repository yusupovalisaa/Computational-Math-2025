def plot_results(x, y, results, best_result):
    """Построение графиков"""
    import matplotlib.pyplot as plt
    import numpy as np

    plt.figure(figsize=(12, 8))
    plt.scatter(x, y, color='black', label='Исходные данные', zorder=5)

    # Диапазон для построения кривых
    x_plot = np.linspace(min(x), max(x), 100)

    for result in results:
        if 'error' in result:
            continue

        try:
            # ВАЖНО: тут уже без *result['params']
            y_plot = result['func'](x_plot)
            line_style = '-' if result == best_result else '--'
            line_width = 2 if result == best_result else 1
            plt.plot(x_plot, y_plot,
                     label=f"{result['name']} (σ={result['deviation']:.3f})",
                     linestyle=line_style,
                     linewidth=line_width)
        except Exception as e:
            print(f"Ошибка при построении графика для {result['name']}: {e}")
            continue

    plt.title("Аппроксимация функции различными методами")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)

    if best_result:
        plt.annotate(f"Лучшая: {best_result['name']}\nσ = {best_result['deviation']:.3f}",
                     xy=(0.05, 0.9), xycoords='axes fraction',
                     bbox=dict(boxstyle='round', alpha=0.8))

    plt.tight_layout()
    plt.show()
