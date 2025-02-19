import numpy as np

class State:
    def __init__(self, path, value):
        self.path = path
        self.value = value

class SimAnn:
    C_input = 100
    p_input = 0.75  

    def __init__(self, dataset, optmode=1, C=C_input, p=p_input):
        self.dataset = dataset
        self.node_size = dataset["n_cities"]
        self.optmode = optmode
        self.C = C
        self.p = p
        self.initial_state = State(list(range(self.node_size)), self.calculate_distance(list(range(self.node_size))))
        self.current_state = self.initial_state
        self.best_state = self.initial_state

    def calculate_distance(self, path):
        distance = sum(self.dataset["distances"][path[i-1]][path[i]] for i in range(1, len(path)))
        return distance + self.dataset["distances"][path[-1]][path[0]]

    def delta_distance(self, route, i, j):
        a, b = route[i-1], route[i]
        c, d = route[j], route[(j+1) % len(route)]
        return (self.dataset["distances"][a][c] + self.dataset["distances"][b][d]) - \
               (self.dataset["distances"][a][b] + self.dataset["distances"][c][d])

    def opt_swap(self, route, i, j):
        new_route = route[:]
        new_route[i], new_route[j] = new_route[j], new_route[i]
        return new_route

    def two_opt_swap(self, route, i, j):
        return route[:i] + route[i:j+1][::-1] + route[j+1:]

    def Neighbor(self, route):
        new_route = route[:]
        for _ in range(3):  # Apply 3 swaps for more diversification
            i, j = np.random.choice(len(route), size=2, replace=False)
            new_route[i], new_route[j] = new_route[j], new_route[i]
        return new_route

    def schedule(self, time):
         return self.C * 0.999**time


    def simulated_annealing(self, n_iter):
        current_state = self.initial_state
        best_state = self.best_state
        
        for t in range(n_iter):
            temperature = self.schedule(t)
            nextMove = self.Neighbor(current_state.path)
            nextValue = self.calculate_distance(nextMove)

            if nextValue < current_state.value or np.random.rand() < np.exp(-(nextValue - current_state.value) / temperature):
                current_state = State(nextMove, nextValue)

            if current_state.value < best_state.value:
                best_state = State(current_state.path[:], current_state.value)

            if t % 5000 == 0:  # Reheat temperature every 5000 iterations
                self.C *= 1.1
            if t % 1000 == 0:
                print(f"Iteration {t}: Best value {best_state.value}")
        
        return best_state
