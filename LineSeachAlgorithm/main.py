from optFunc import optFuncSphere
import matplotlib.pyplot as plt
import numpy as np

class linSearch:
    def __init__(self, func, stopCrit=1e-5, stepCond=0.1, c1=1e-4, c2=0.9):
        self.func = func
        self.stopCrit = stopCrit
        self.stepCond = stepCond
        self.wolfe = WolfeConditions(c1, c2)  # Initialize Wolfe conditions
        self.solutions = []

    def wolfe_step(self, x, d, condition="armijo"):
        """Calculate step size using the specified Wolfe condition."""
        alpha = self.stepCond
        if condition == "armijo":
            while not self.wolfe.armijo_condition(self.func, x, alpha, d):
                alpha *= 0.5
        elif condition == "curvature":
            while not (self.wolfe.armijo_condition(self.func, x, alpha, d) and
                       self.wolfe.curvature_condition(self.func, x, alpha, d)):
                alpha *= 0.5
        elif condition == "strong":
            while not (self.wolfe.armijo_condition(self.func, x, alpha, d) and
                       self.wolfe.strong_wolfe_condition(self.func, x, alpha, d)):
                alpha *= 0.5
        else:
            raise ValueError("Condition not supported. Use 'armijo', 'curvature', or 'strong'.")
        return alpha

    def solve(self, x0, condition="armijo"):
      """Solve the optimization problem using the specified Wolfe condition."""
      x = np.array(x0, dtype=float)
      self.solutions.append(x.copy())  # Add initial point to solutions

      iterations = 0
      while True:
          grad_norm = np.linalg.norm(self.func.grad(x))
          prev_value = self.solutions[-1] if len(self.solutions) > 1 else x
          curr_value = x

          # Check stopping conditions
          if self.stop_criterion(grad_norm, prev_value, curr_value, iterations):
              break

          d = -self.func.grad(x)  # Steepest descent direction
          alpha = self.wolfe_step(x, d, condition)
          x = x + alpha * d
          self.solutions.append(x.copy())
          iterations += 1

      return x
    
    def stop_criterion(self, grad_norm, prev_value, curr_value, iterations):
        grad_tolerance = 1e-5
        value_tolerance = 1e-8
        max_iter = 1000
        
        # Multiple stopping conditions
        grad_small = grad_norm < grad_tolerance
        diff = np.linalg.norm(curr_value - prev_value)
        if diff != 0:
          value_converged = diff < value_tolerance
        else:
          value_converged = False
        
        iter_exceeded = iterations > max_iter
        
        return grad_small or value_converged or iter_exceeded

    def plot2D(self):
        # Creación del mallado
        x = np.linspace(-5, 5, 100) # [-5, -4.9, -4.8, ..., 4.9, 5] 100 puntos
        y = np.linspace(-5, 5, 100) # [-5, -4.9, -4.8, ..., 4.9, 5] 100 puntos
        X, Y = np.meshgrid(x, y) # Crear la malla [-5, -4.9, ..., 5] x [-5, -4.9, ..., 5]
        Z = X**2 + Y**2  # La función esfera 

        # Dibuja las curvas de nivel
        contours=plt.contour(x, y, Z, 30, cmap=plt.cm.gnuplot)
        plt.clabel(contours, inline=1, fontsize=10)

        # Graficar la trayectoria del descenso
        sol = np.array(self.solutions) 
        plt.plot(sol[:-1:, 0], sol[:-1:, 1], 'ro-', label="Trayectoria")  # Recorrido en rojo
        plt.scatter(sol[-1, 0], sol[-1, 1], c='blue', label="Óptimo")  # Punto óptimo
        plt.legend()
        plt.show()

class WolfeConditions:
    def __init__(self, c1=1e-4, c2=0.9):
        self.c1 = c1  # Armijo condition constant
        self.c2 = c2  # Curvature condition constant

    def armijo_condition(self, func, x, alpha, d):
        """Armijo condition (sufficient decrease)."""
        return func.eval(x + alpha * d) <= func.eval(x) + self.c1 * alpha * np.dot(func.grad(x), d)

    def curvature_condition(self, func, x, alpha, d):
        """Curvature condition."""
        return np.dot(func.grad(x + alpha * d), d) >= self.c2 * np.dot(func.grad(x), d)

    def strong_wolfe_condition(self, func, x, alpha, d):
        """Strong Wolfe condition."""
        grad_x = func.grad(x)
        grad_x_alpha = func.grad(x + alpha * d)
        return abs(np.dot(grad_x_alpha, d)) <= self.c2 * abs(np.dot(grad_x, d))

if __name__ == "__main__":
    func = optFuncSphere()
    optimizer = linSearch(func)
    x_opt = optimizer.solve([5, 5], condition="strong")
    print(f"Óptimo encontrado en: {x_opt}")
    print(f"Numero de iteraciones: {len(optimizer.solutions)}")
    optimizer.plot2D()
