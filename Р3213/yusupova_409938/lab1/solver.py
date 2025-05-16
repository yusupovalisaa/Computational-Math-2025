import numpy as np
import random

DEFAULT_EPSILON = 1e-6
MAX_ITERATIONS = 1000
MAX_MATRIX_SIZE = 20

# Абстракция для решения СЛАУ
class SLAUSolverMethod:
    def solve(self, A, b, eps=DEFAULT_EPSILON, max_iter=MAX_ITERATIONS):
        pass

# Реализация метода простых итераций
class SimpleIterationSolver(SLAUSolverMethod):
    def solve(self, A, b, eps=DEFAULT_EPSILON, max_iter=MAX_ITERATIONS):
        A_new, b_new, warning = rearrange_for_diagonal_dominance(A, b)
        result_message = warning or ""

        n = len(A_new)
        x = np.zeros(n)
        B = np.zeros((n, n))
        c = np.zeros(n)

        # Приведение к форме x = Bx + C
        for i in range(n):
            c[i] = b_new[i] / A_new[i, i]
            for j in range(n):
                if i != j:
                    B[i, j] = -A_new[i, j] / A_new[i, i]

        norm_B = np.max(np.sum(np.abs(B), axis=1))  # Норма по строкам
        if norm_B >= 1:
            return None, f"{result_message}Решений нет. Метод не сходится, так как норма матрицы B ≥ 1.\n", norm_B

        iter_count = 0
        while iter_count < max_iter:
            x_new = np.dot(B, x) + c
            if np.linalg.norm(x_new - x, ord=np.inf) < eps:
                residual = np.dot(A_new, x_new) - b_new
                return x_new, iter_count, residual, result_message, norm_B
            x = x_new
            iter_count += 1

        return None, f"{result_message}Превышено максимальное количество итераций.", norm_B


def rearrange_for_diagonal_dominance(A, b):
    n = len(A)
    A = A.copy()
    b = b.copy()

    for i in range(n):
        max_col = np.argmax(np.abs(A[i, :]))  # Находим индекс максимального по модулю элемента в строке
        if max_col != i:
            A[:, [i, max_col]] = A[:, [max_col, i]]  # Переставляем столбцы
    # Проверка на диагональное преобладание
    for i in range(n):
        row_sum = np.sum(np.abs(A[i, :])) - np.abs(A[i, i])
        if np.abs(A[i, i]) < row_sum:
            return A, b, "Не удалось достичь диагонального преобладания. Пробуем решить без него.\n"
    return A, b, None

def generate_random_matrix(n, min_val=-10, max_val=10):
    A = np.random.randint(min_val, max_val + 1, size=(n, n)).astype(float)
    b = np.random.randint(min_val, max_val + 1, size=n).astype(float)

    for i in range(n):
        A[i, i] = sum(abs(A[i])) + random.uniform(1, 5)
    return A, b