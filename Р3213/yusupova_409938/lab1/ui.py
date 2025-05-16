from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QTextEdit, QFileDialog, QLabel, QLineEdit, QGridLayout,
    QMessageBox
)
import numpy as np
from solver import generate_random_matrix


class SLAUSolverUI(QWidget):
    def __init__(self, solver_method):
        super().__init__()
        self.solver_method = solver_method
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.label = QLabel("Введите размерность матрицы (n ≤ 20):")
        self.layout.addWidget(self.label)

        self.size_input = QLineEdit()
        self.layout.addWidget(self.size_input)

        self.label_eps = QLabel("Введите точность (epsilon):")
        self.layout.addWidget(self.label_eps)

        self.eps_input = QLineEdit()
        self.layout.addWidget(self.eps_input)

        self.generate_matrix_button = QPushButton("Создать матрицу")
        self.generate_matrix_button.clicked.connect(self.create_matrix_input)
        self.layout.addWidget(self.generate_matrix_button)

        self.random_matrix_button = QPushButton("Случайная матрица")
        self.random_matrix_button.clicked.connect(self.fill_random_matrix)
        self.layout.addWidget(self.random_matrix_button)

        self.matrix_layout = QGridLayout()
        self.layout.addLayout(self.matrix_layout)

        self.solveButton = QPushButton("Решить")
        self.solveButton.clicked.connect(self.solve_slae)
        self.layout.addWidget(self.solveButton)

        self.loadButton = QPushButton("Загрузить из файла")
        self.loadButton.clicked.connect(self.load_from_file)
        self.layout.addWidget(self.loadButton)

        # Текстовое поле для результатов
        self.resultText = QTextEdit()
        self.resultText.setReadOnly(True)
        self.layout.addWidget(self.resultText)

        self.setLayout(self.layout)
        self.setWindowTitle("Решение СЛАУ методом простых итераций")
        self.resize(600, 400)

        self.matrix_inputs = []

    def create_matrix_input(self):
        # Очистка текущих полей
        for i in reversed(range(self.matrix_layout.count())):
            self.matrix_layout.itemAt(i).widget().setParent(None)

        try:
            n = int(self.size_input.text())
            if not (1 <= n <= 20):
                self.show_error_message("Ошибка: размерность должна быть от 1 до 20.")
                return

            eps_text = self.eps_input.text().strip()
            if not eps_text:
                self.show_error_message("Ошибка: введите точность (epsilon).")
                return

            try:
                eps = float(eps_text)
                if eps <= 0:
                    raise ValueError
            except ValueError:
                self.show_error_message("Ошибка: epsilon должен быть положительным числом.")
                return

            self.matrix_inputs = [[QLineEdit() for _ in range(n + 1)] for _ in range(n)]
            for i in range(n):
                for j in range(n + 1):
                    self.matrix_layout.addWidget(self.matrix_inputs[i][j], i, j)

        except ValueError:
            self.show_error_message("Ошибка: введите корректное число.")

    def fill_random_matrix(self):
            try:
                n = int(self.size_input.text())
                if not (1 <= n <= 20):
                    self.show_error_message("Ошибка: размерность должна быть от 1 до 20.")
                    return

                eps_text = self.eps_input.text().strip()
                if not eps_text:
                    self.show_error_message("Ошибка: введите точность (epsilon).")
                    return

                try:
                    eps = float(eps_text)
                    if eps <= 0:
                        raise ValueError
                except ValueError:
                    self.show_error_message("Ошибка: epsilon должен быть положительным числом.")
                    return

                A, b = generate_random_matrix(n)
                self.create_matrix_input()

                for i in range(n):
                    for j in range(n):
                        self.matrix_inputs[i][j].setText(str(A[i, j]))
                    self.matrix_inputs[i][-1].setText(str(b[i]))

            except ValueError:
                self.show_error_message("Введите корректное число.")

    def solve_slae(self):
        try:
            n = len(self.matrix_inputs)

            # Проверка epsilon
            eps_text = self.eps_input.text().strip()
            if not eps_text:
                self.show_error_message("Ошибка: введите точность (epsilon).")
                return

            try:
                eps = float(eps_text)
                if eps <= 0:
                    raise ValueError
            except ValueError:
                self.show_error_message("Ошибка: epsilon должен быть положительным числом.")
                return

            A = np.array([[float(self.matrix_inputs[i][j].text()) for j in range(n)] for i in range(n)])
            B = np.array([float(self.matrix_inputs[i][-1].text()) for i in range(n)])

            result = self.solver_method.solve(A, B, eps)
            if result[0] is None:
                self.resultText.setText(result[1])
            else:
                x, iter_count, residual, warning, norm_B = result

                x_str = ', '.join([f"{int(val) if val.is_integer() else val:.6f}" for val in x])
                residual_str = ', '.join([f"{int(val) if val.is_integer() else val:.6f}" for val in residual])

                self.resultText.setText(
                    f"Норма матрицы: {norm_B}\n"
                    f"Решение: [{x_str}]\n"
                    f"Количество итераций: {iter_count}\n"
                    f"Вектор погрешностей: [{residual_str}]\n"
                )
        except Exception as e:
            self.show_error_message(f"Ошибка ввода данных: {e}")

    def load_from_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "Text Files (*.txt);;All Files (*)")
        if filename:
            try:
                with open(filename, 'r') as file:
                    lines = file.readlines()

                n = int(lines[0].strip())  # размерность
                eps = float(lines[1].strip())  # точность

                A = []
                b = []

                for line in lines[2:n + 2]:
                    values = list(map(float, line.split()))
                    A.append(values[:-1])
                    b.append(values[-1])

                A = np.array(A)
                b = np.array(b)

                # Автоматически подставляем в поля ввода
                self.size_input.setText(str(n))
                self.eps_input.setText(str(eps))
                self.create_matrix_input()

                # Заполняем GUI полями из файла
                for i in range(n):
                    for j in range(n):
                        self.matrix_inputs[i][j].setText(str(A[i, j]))
                    self.matrix_inputs[i][-1].setText(str(b[i]))

                self.resultText.setText("Файл загружен успешно.")
            except Exception as e:
                self.show_error_message(f"Ошибка загрузки файла")

    def show_error_message(self, message):
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setWindowTitle("Ошибка")
        error_dialog.setText(message)
        error_dialog.exec()


