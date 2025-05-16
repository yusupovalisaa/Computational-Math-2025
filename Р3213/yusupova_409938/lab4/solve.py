import numpy as np
def solve_slae(A, B, n):
    if n == 2:
        return solve2(A, B)
    if n == 3:
        return solve3(A, B)
    if n == 4:
        return solve4(A, B)
    raise ValueError(f"Только системы 2x2, 3x3 и 4x4 поддерживаются, получено n={n}")


def calc_det2(A):
    return (A[0][0] * A[1][0]) - (A[0][1] * A[1][1])

def solve2(A, B):
    det = calc_det2(A)

    if abs(det) < 1e-12:
        raise ValueError("Система вырождена (определитель матрицы равен нулю)")

    det1 = (B[0]* A[1][1]) - (B[1] * A[0][1])
    print((B[0], A[1][1], B[1], A[0][1]))
    det2 = (A[0][0] * B[1]) - (A[1][0] * B[0])
    print(det, det1, det2)
    # Находим решения
    x1 = det1 / det
    x2 = det2 / det

    return x1, x2

def calc_det3(A):
    pos = A[0][0] * A[1][1] * A[2][2] + A[0][1] * A[1][2] * A[2][0] + A[0][2] * A[1][0] * A[2][1]
    neg = A[0][2] * A[1][1] * A[2][0] + A[0][1] * A[1][0] * A[2][2] + A[0][0] * A[1][2] * A[2][1]
    return pos - neg


def solve3(A, B):
    det = calc_det3(A)
    if abs(det) < 1e-12:
        raise ValueError("Система несовместна или имеет бесконечно много решений.")
    det1 = calc_det3([[B[r], A[r][1], A[r][2]] for r in range(3)])
    det2 = calc_det3([[A[r][0], B[r], A[r][2]] for r in range(3)])
    det3 = calc_det3([[A[r][0], A[r][1], B[r]] for r in range(3)])
    return det1 / det, det2 / det, det3 / det


def calc_det4(A):
    result = 0
    for c in range(4):
        minor = [[A[r][cc] for cc in range(4) if cc != c] for r in range(1, 4)]
        result += ((-1) ** c) * A[0][c] * calc_det3(minor)
    return result

def solve4(A, B):
    det = calc_det4(A)
    if abs(det) < 1e-12:
        raise ValueError("Система несовместна или имеет бесконечно много решений.")
    det1 = calc_det4([[B[r], A[r][1], A[r][2], A[r][3]] for r in range(4)])
    det2 = calc_det4([[A[r][0], B[r], A[r][2], A[r][3]] for r in range(4)])
    det3 = calc_det4([[A[r][0], A[r][1], B[r], A[r][3]] for r in range(4)])
    det4 = calc_det4([[A[r][0], A[r][1], A[r][2], B[r]] for r in range(4)])
    return det1 / det, det2 / det, det3 / det, det4 / det