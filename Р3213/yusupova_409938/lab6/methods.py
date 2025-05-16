class EulerMethod:
    def solve(self, equation_num, x0, y0, xn, h):
        f = self._get_equation(equation_num)
        x_values = []
        y_values = []

        x = x0
        y = y0
        x_values.append(x)
        y_values.append(y)

        while x < xn:
            y += h * f(x, y)
            x += h
            x_values.append(x)
            y_values.append(y)

        return x_values, y_values

    def _get_equation(self, num):
        equations = {
            '1': lambda x, y: x + y,
            '2': lambda x, y: x**2 + y**2,
            '3': lambda x, y: 2 * x - y
        }
        return equations.get(num, lambda x, y: x + y)


class RungeKutta4Method:
    def solve(self, equation_num, x0, y0, xn, h):
        f = self._get_equation(equation_num)
        x_values = []
        y_values = []

        x = x0
        y = y0
        x_values.append(x)
        y_values.append(y)

        while x < xn:
            k1 = h * f(x, y)
            k2 = h * f(x + h/2, y + k1/2)
            k3 = h * f(x + h/2, y + k2/2)
            k4 = h * f(x + h, y + k3)

            y += (k1 + 2*k2 + 2*k3 + k4) / 6
            x += h
            x_values.append(x)
            y_values.append(y)

        return x_values, y_values

    def _get_equation(self, num):
        equations = {
            '1': lambda x, y: x + y,
            '2': lambda x, y: x**2 + y**2,
            '3': lambda x, y: 2*x - y
        }
        return equations.get(num, lambda x, y: x + y)


class AdamsMethod:
    def solve(self, equation_num, x0, y0, xn, h):
        f = self._get_equation(equation_num)
        x_values = []
        y_values = []

        # Используем Рунге-Кутта для получения первых 4 точек
        rk4 = RungeKutta4Method()
        start_x, start_y = rk4.solve(equation_num, x0, y0, x0 + 3*h, h)

        x_values.extend(start_x)
        y_values.extend(start_y)

        x = x0 + 3*h
        while x < xn:
            # Предыдущие значения функции
            f0 = f(x_values[-4], y_values[-4])
            f1 = f(x_values[-3], y_values[-3])
            f2 = f(x_values[-2], y_values[-2])
            f3 = f(x_values[-1], y_values[-1])

            # Формула Адамса (предиктор)
            y_next = y_values[-1] + h*(55*f3 - 59*f2 + 37*f1 - 9*f0)/24
            x_next = x + h

            # Корректор (одна итерация)
            f_next = f(x_next, y_next)
            y_next = y_values[-1] + h*(9*f_next + 19*f3 - 5*f2 + f1)/24

            x_values.append(x_next)
            y_values.append(y_next)
            x = x_next

        return x_values, y_values

    def _get_equation(self, num):
        """Возвращает выбранное уравнение"""
        equations = {
            '1': lambda x, y: x + y,
            '2': lambda x, y: x**2 + y**2,
            '3': lambda x, y: 2*x - y
        }
        return equations.get(num, lambda x, y: x + y)


def Runge_rule(y_h, y_h2, p):
    return abs(y_h - y_h2) / (2 ** p - 1)