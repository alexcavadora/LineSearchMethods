import random as rn
import itertools

class SimAnn:
    def __init__(self, dataset, optmode = 1):
        self.dataset = dataset
        self.node_size = dataset["n_cities"]
        self.optmode = optmode

    def opt_swap(self, dataset):
        """
        Realiza un swap simple entre dos nodos i y j.
        """
        i, j = dataset["xy"][:0], dataset["xy"][:1]
        route = list(range(self.node_size))
        new_route = route[:]
        new_route[i], new_route[j] = new_route[j], new_route[i]
        return new_route

    def two_opt_swap(self, dataset):
        """
        Realiza un 2-opt swap, invirtiendo el segmento entre i y j.
        """
        i, j = dataset["xy"][:0], dataset["xy"][:1]
        route = list(range(self.node_size))
        new_route = route[:i] + route[i:j+1][::-1] + route[j+1:]
        return new_route

    def Neighbor(self, dataset, optmode):
        """
        Genera todos los vecinos de la ruta aplicando OPT y 2-OPT.
        """
        neighbors = []
        for _ in range(self.node_size):
            route = dataset["xy"][_]
        n = len(route)
        way = optmode
        
        if way == 1: 
            # Genera vecinos con 1-OPT (swap simple)
            for i, j in itertools.combinations(range(n), 2):
                neighbors.append(self.opt_swap(route, i, j))
        else:
            # Genera vecinos con 2-OPT (segment reversal)
            for i, j in itertools.combinations(range(n), 2):
                if j > i:  # Para evitar segmentos vacíos
                    neighbors.append(self.two_opt_swap(route, i, j))
        
        return neighbors



