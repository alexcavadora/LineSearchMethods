import random as rn
import itertools

class state:
    #keep track of states- the current path and its cost/value
    def __init__(self, path, value):
        self.path = path
        self.value = value

class SimAnn:
    C_input = 7
    p_input = 0.37

    def __init__(self, dataset, optmode = 1):
        self.dataset = dataset
        self.node_size = dataset["n_cities"]
        self.optmode = optmode

        self.initial_state = initial # a path that visits all the nodes. This will just be the list of nodes how they are.
        self.current_state = initial # the current path we are checking
        self.best_state = best # the best state we have found so far
        self.objective_function = objective_function # minimize the total path cost, this will be the path_cost() function.
        self.schedule_function = schedule_function # schedule function and probability of acceptance function, the information we need to choose our action
        

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
    
    def schedule(time, C=C_input, p=p_input):
        # 
        # some sort of mapping from time to temperature, to represent "cooling off" - 
        # that is, accepting wacky solutions with lower and lower probability as time increases
        # 
        T = C/(time+1)**p
        return T
    
    def distance(self, route):

        distance = 0
        
        return distance

    
    def simulated_annealing(self, n_iter):
        current_state = self.initial_state
        best_state = self.best_state
        times = []
        values = []
        
        for t in range(int(n_iter)):
            temperature = self.schedule_function(t)
            nextMove, nextValue = self.random_move() #from randomly generated moves
            
            if nextValue < best_state.value:
                self.best_state.path = nextMove
                self.best_state.value = nextValue
                
            # Next value is better than current value
            if nextValue < current_state.value:
                self.current_state.path = nextMove
                self.current_state.value = nextValue 
            else: # next value is worse (or equal to) current value
                n_random = np.random.rand()
                E = -abs(nextValue-current_state.value) # E<0
                p_accept = np.exp(E/temperature) #should depend on quality of path
                if n_random < p_accept:
                    self.current_state.path, self.current_state.value = nextMove, nextValue
                # else: do nothing, keep iterating

            if t % 100 ==0:
                times.append(t)
                values.append(best_state.value)
                print(best_state.path, best_state.value)
            if t==n_iter:
                times.append(t)
                values.append(best_state.value)
        return self.best_state

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


