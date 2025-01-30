from optFunc import optFuncSphere
import matplotlib.pyplot as plt
import numpy as np

class linSearch:
    def __init__(self, func, stopCrit=1e-5, stepCond=0.1):
        self.func = func
        self.stopCrit = stopCrit
        self.stepCond = stepCond
        self.solutions = []

    def solve(self, x0):
        x = np.array(x0, dtype=float)  # Asegurar que x es un array de numpy
        while np.linalg.norm(self.func.grad(x)) > self.stopCrit:
            x = x - self.stepCond * np.array(self.func.grad(x))  # Vectorizado
            self.solutions.append(x.copy())  # Guardar copia del vector
        return x

    def plot2D(self):
        # Creación del mallado
        x = np.linspace(-5, 5, 100)
        y = np.linspace(-5, 5, 100)
        X, Y = np.meshgrid(x, y)
        Z = X**2 + Y**2  # La función esfera

        # Dibuja las curvas de nivel
        plt.contour(X, Y, Z, levels=30)

        # Graficar la trayectoria del descenso
        sol = np.array(self.solutions)
        plt.plot(sol[:, 0], sol[:, 1], 'ro-', label="Trayectoria")  # Recorrido en rojo
        plt.scatter(sol[-1, 0], sol[-1, 1], c='blue', label="Óptimo")  # Punto óptimo
        plt.legend()
        plt.show()

if __name__ == "__main__":
    func = optFuncSphere()
    optimizer = linSearch(func)
    x_opt = optimizer.solve([5, 5])  # Pasar un vector inicial
    print(f"Óptimo encontrado en: {x_opt}")
    optimizer.plot2D()

import matplotlib.pyplot as plt
import numpy as np

class linSearch:
  def __init__(self, func, stopCrit=1e-5, stepCond=0.1):
    self.func = func
    self.stopCrit = stopCrit
    self.stepCond = stepCond
    self.solutions = []

  def solve(self, x0):
    x = x0
    while abs(self.func.grad(x) > self.stopCrit):
      x = x - self.stepCond * self.func.grad(x)
      self.solutions.append(x)
    return x

  def plot2D(self):
    # Creación del mallado
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2))

    # Dibuja las curvas de nivel
    plt.contour(X, Y, Z)

    ye = [self.func.eval(xi) for xi in self.solutions]
    plt.plot(self.solutions, ye)
    plt.show()

if __name__ == "__main__":
  func = optFuncSphere()
  optimizer = linSearch(func)
  x_opt = optimizer.solve(5)
  print(f"Optimo encontrado en: {x_opt}")
  optimizer.plot2D()