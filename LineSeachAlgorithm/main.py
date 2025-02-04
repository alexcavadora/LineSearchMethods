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
        self.solutions.append(x.copy())  # Guardar copia del vector
        # self.solutions.append(x.copy() + 1) 
        while not self.stop_criterion(np.linalg.norm(self.func.grad(x)), self.solutions[-1], x, len(self.solutions)):
            x = x - self.stepCond * np.array(self.func.grad(x))  # Vectorizado
            self.solutions.append(x.copy())  # Guardar copia del vector
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


if __name__ == "__main__":
    func = optFuncSphere()
    optimizer = linSearch(func)
    x_opt = optimizer.solve([5, 5])  # Pasar un vector inicial
    print(f"Óptimo encontrado en: {x_opt}")
    print(f"Numero de iteraciones: {len(optimizer.solutions)}")
    optimizer.plot2D()
