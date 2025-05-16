import sys
from PyQt6.QtWidgets import QApplication
from ui import SLAUSolverUI
from solver import SimpleIterationSolver

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Создаем объект метода решения
    solver_method = SimpleIterationSolver()

    # Передаем метод решения в интерфейс
    solver = SLAUSolverUI(solver_method)
    solver.show()

    sys.exit(app.exec())
