from LineSearchAlgorithm.optFunc import optFuncSphere
import matplotlib.pyplot as plt
import numpy as np

class linSearch:
    def __init__(self, func, stopCrit, stepCond, c1=1e-4, c2=0.9):
        self.func = func
        self.stopCrit = stopCrit 
        self.stepCond = stepCond
        self.wolfe = WolfeConditions(c1, c2)
        self.solutions = []

    def solve(self, x0, condition="armijo"):
        """Resuelve el problema de optimización usando la condición de Wolfe especificada."""
        x = np.array(x0, dtype=float)
        self.solutions.append(x.copy())
        iterations = 0

        while True:
            grad_norm = np.linalg.norm(self.func.grad(x))
            prev_value = self.solutions[-1] if len(self.solutions) > 1 else x
            curr_value = x

            if self.stopCrit(grad_norm, prev_value, curr_value, iterations):
                break

            d = -self.func.grad(x)
            alpha = self.stepCond(x, d, self.func, self.wolfe, condition)
            x = x + alpha * d
            self.solutions.append(x.copy())
            iterations += 1

        return x

    def plot2D(self):
        x = np.linspace(-5, 5, 100)
        y = np.linspace(-5, 5, 100)
        X, Y = np.meshgrid(x, y)
        Z = X**2 + Y**2

        contours = plt.contour(x, y, Z, 30, cmap=plt.cm.gnuplot)
        plt.clabel(contours, inline=1, fontsize=10)
        
        sol = np.array(self.solutions)
        plt.plot(sol[:-1, 0], sol[:-1, 1], 'ro-', label="Trayectoria")
        plt.scatter(sol[-1, 0], sol[-1, 1], c='blue', label="Óptimo")
        plt.legend()
        plt.show()

class WolfeConditions:
    def __init__(self, c1=1e-4, c2=0.9):
        self.c1 = c1
        self.c2 = c2

    def armijo_condition(self, func, x, alpha, d):
        return func.eval(x + alpha * d) <= func.eval(x) + self.c1 * alpha * np.dot(func.grad(x), d)

    def curvature_condition(self, func, x, alpha, d):
        return np.dot(func.grad(x + alpha * d), d) >= self.c2 * np.dot(func.grad(x), d)

    def strong_wolfe_condition(self, func, x, alpha, d):
        grad_x = func.grad(x)
        grad_x_alpha = func.grad(x + alpha * d)
        return abs(np.dot(grad_x_alpha, d)) <= self.c2 * abs(np.dot(grad_x, d))

# Definición de funciones externas
def stop_criterion(grad_norm, prev_value, curr_value, iterations):
    grad_tolerance = 1e-5
    value_tolerance = 1e-8
    max_iter = 1000

    grad_small = grad_norm < grad_tolerance
    diff = np.linalg.norm(curr_value - prev_value)
    value_converged = diff < value_tolerance if diff != 0 else False
    iter_exceeded = iterations > max_iter

    return grad_small or value_converged or iter_exceeded


def step_condition(x, d, func, wolfe, condition):
    alpha = 0.1
    if condition == "armijo":
        while not wolfe.armijo_condition(func, x, alpha, d):
            alpha *= 0.5
    elif condition == "curvature":
        while not (wolfe.armijo_condition(func, x, alpha, d) and
                   wolfe.curvature_condition(func, x, alpha, d)):
            alpha *= 0.5
    elif condition == "strong":
        while not (wolfe.armijo_condition(func, x, alpha, d) and
                   wolfe.strong_wolfe_condition(func, x, alpha, d)):
            alpha *= 0.5
    else:
        raise ValueError("Condición no soportada. Use 'armijo', 'curvature' o 'strong'.")
    return alpha

if __name__ == "__main__":
    func = optFuncSphere()
    optimizer = linSearch(func, stop_criterion, step_condition)
    x_opt = optimizer.solve([5, 5], condition="strong")
    print(f"Óptimo encontrado en: {x_opt}")
    print(f"Número de iteraciones: {len(optimizer.solutions)}")
    optimizer.plot2D()
