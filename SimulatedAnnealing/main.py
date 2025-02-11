import numpy as np
import matplotlib.pyplot as plt
from parser import parser



def plot2D(idx_perm, data):
    coord_x = [data["xy"][i][0] for i in range(len(data["xy"]))]
    coord_y = [data["xy"][i][1] for i in range(len(data["xy"]))]

    def log_base_change(value, base):
        return np.log(value) / np.log(base)
    # coord_y = log_base_change(coord_y, 500)
    # coord_y = [y**2 for y in coord_y]

    # Crear el gráfico de puntos
    plt.scatter(coord_x, coord_y, c='green')

    # Conectar los puntos con una línea gris usando idx_perm
    for i in range(len(idx_perm)):
        start_idx = idx_perm[i]
        end_idx = idx_perm[(i + 1) % len(idx_perm)]
        plt.plot([coord_x[start_idx], coord_x[end_idx]], [coord_y[start_idx], coord_y[end_idx]], 'gray', alpha=0.3)

    # Añadir títulos y etiquetas
    plt.title('Ciudades')
    plt.xlabel('Coord X')
    plt.ylabel('Coord Y')

    # Mostrar el gráfico
    plt.show()

with open("./dataset/rc_201.1.txt") as f:
    fileContent = f.read()

data = parser(fileContent)
idx_perm = np.random.permutation(len(data["xy"]))
plot2D(idx_perm, data)


