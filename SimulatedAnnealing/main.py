import random as rn
import itertools

class SimAnn:
    def __init__(self, dataset, optmode = 1):
        self.dataset = dataset
        self.node_size = dataset["n_cities"]
        self.optmode = optmode

    def opt_swap(self, i, j):
        """
        Realiza un swap simple entre dos nodos i y j.
        """
        i, j = self.dataset["xy"][:0], self.dataset["xy"][:1]
        route = list(range(self.node_size))
        new_route = route[:]
        new_route[i], new_route[j] = new_route[j], new_route[i]
        return new_route

    def two_opt_swap(self, i, j):
        """
        Realiza un 2-opt swap, invirtiendo el segmento entre i y j.
        """
        i, j = self.dataset["xy"][:0], self.dataset["xy"][:1]
        route = list(range(self.node_size))
        new_route = route[:i] + route[i:j+1][::-1] + route[j+1:]
        return new_route

    def Neighbor(self, dataset, optmode):
        """
        Genera todos los vecinos de la ruta aplicando OPT y 2-OPT.
        """
        neighbors = []
        route = dataset["xy"]

        n = len(route)
        
        way = optmode
        
        if way == 1: 
            # Genera vecinos con 1-OPT (swap simple)
            for i, j in itertools.combinations(dataset, 2):
                neighbors.append(self.opt_swap(route, i, j))
        else:
            # Genera vecinos con 2-OPT (segment reversal)
            for i, j in itertools.combinations(dataset, 2):
                if j > i: 
                    neighbors.append(self.two_opt_swap(route, i, j))
        return neighbors



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


