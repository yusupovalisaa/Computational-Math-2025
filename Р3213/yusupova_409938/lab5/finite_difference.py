from typing import List

def calculate_finite_differences(y_values: List[float]) -> List[List[float]]:
    n = len(y_values)
    table = [y_values.copy()]  # только y
    for level in range(1, n):
        prev_level = table[level - 1]
        current_level = [
            round(prev_level[i + 1] - prev_level[i], 4)
            for i in range(len(prev_level) - 1)
        ]
        table.append(current_level)
    return table


