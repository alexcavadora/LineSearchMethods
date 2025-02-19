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

        initial_path = list(range(self.node_size))
        initial_value = self.calculate_distance(initial_path)
        self.initial_state = State(initial_path, initial_value)
        self.current_state = State(initial_path.copy(), initial_value)
        self.best_state = State(initial_path.copy(), initial_value)

    def calculate_distance(self, path):
        """ Calculate the total distance of the current path """
        distance = 0
        d = self.dataset["distances"]
        for i in range(1, len(path)):
            distance += d[path[i-1]][path[i]]
        
        # Loop distance
        distance += d[path[-1]][path[0]] 
        return distance

    def opt_swap(self, route, i, j):
        """Perform a simple swap between two nodes i and j in the route."""
        new_route = route.copy()
        new_route[i], new_route[j] = new_route[j], new_route[i]
        return new_route

    def two_opt_swap(self, route, i, j):
        """Perform a 2-opt swap, reversing the segment between i and j."""
        # 2 opt swap is a reversal of the segment between i and j in the route 
        return route[:i] + route[i:j+1][::-1] + route[j+1:]

    def random_neighbor(self, route):
        """Generate a random neighbor without needing to enumerate all neighbors."""
        n = len(route)
        i = int(np.random.randint(0, n))
        j = int(np.random.randint(0, n))
        while i == j:
            j = int(np.random.randint(0, n))
        if self.optmode == 1:
            return self.opt_swap(route, i, j)
        else:
            if i > j:
                i, j = j, i
            return self.two_opt_swap(route, i, j)

    def schedule(self, t):
        """Temperature schedule for simulated annealing."""
        return self.C / (t + 1) ** self.p

    def simulated_annealing(self, n_iter):
        """Simulated Annealing algorithm for optimization."""
        current_state = self.current_state
        best_state = self.best_state

        for t in range(n_iter):
            temperature = self.schedule(t)
            # Seleccionar un vecino aleatorio
            next_route = self.random_neighbor(current_state.path)
            next_value = self.calculate_distance(next_route)
            delta_E = next_value - current_state.value

            # Accept automatically if it improves the solution
            if delta_E < 0:
                current_state.path = next_route
                current_state.value = next_value
            else:
                # Calculate the probability of acceptance for a worse state
                p_accept = np.exp(-delta_E / temperature)
                if np.random.rand() < p_accept:
                    current_state.path = next_route
                    current_state.value = next_value

            # Update the best state found
            if current_state.value < best_state.value:
                best_state.path = current_state.path.copy()
                best_state.value = current_state.value

            if t % 20 == 0:
                print(f"Iteración {t}: valor {best_state.value}")

        return best_state

