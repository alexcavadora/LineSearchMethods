import numpy as np
import itertools
class State:
    #keep track of states- the current path and its cost/value
    def __init__(self, path, value):
        self.path = path
        self.value = value

class SimAnn:
    C_input = 7  # Initial temperature constant
    p_input = 0.37  # Cooling rate

    def __init__(self, dataset, optmode=1):
        self.dataset = dataset
        self.node_size = dataset["n_cities"]
        self.optmode = optmode

        self.initial_state = State(list(range(self.node_size)), self.calculate_distance(list(range(self.node_size))))  # Default initial path
        self.current_state = self.initial_state
        self.best_state = self.initial_state

    def calculate_distance(self, path):
        """ Calculate the total distance of the current path """
        distance = 0
        for i in range(1, len(path)):
            x1, y1 = self.dataset["xy"][path[i-1]]
            x2, y2 = self.dataset["xy"][path[i]]
            distance += np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        # Assuming the path is circular, return to the starting city
        x1, y1 = self.dataset["xy"][path[-1]]
        x2, y2 = self.dataset["xy"][path[0]]
        distance += np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return distance

    def opt_swap(self, route, i, j):
        """Perform a simple swap between two nodes i and j in the route."""
        new_route = route[:]
        new_route[i], new_route[j] = new_route[j], new_route[i]
        return new_route

    def two_opt_swap(self, route, i, j):
        """Perform a 2-opt swap, reversing the segment between i and j."""
        new_route = route[:i] + route[i:j+1][::-1] + route[j+1:]
        return new_route

    def Neighbor(self, route):
        """Generates all neighbors of the current path by applying OPT or 2-OPT."""
        neighbors = []
        n = len(route)
        
        if self.optmode == 1:
            # Generate neighbors with 1-OPT (simple swap)
            for i, j in itertools.combinations(range(n), 2):
                neighbors.append(self.opt_swap(route, i, j))
        else:
            # Generate neighbors with 2-OPT (segment reversal)
            for i, j in itertools.combinations(range(n), 2):
                if j > i:
                    neighbors.append(self.two_opt_swap(route, i, j))
        return neighbors

    def schedule(self, time, C=C_input, p=p_input):
        """Temperature schedule for simulated annealing."""
        return C / (time + 1) ** p

    def simulated_annealing(self, n_iter):
        """Simulated Annealing algorithm for optimization."""
        current_state = self.initial_state
        best_state = self.best_state
        
        times = []
        values = []
        
        for t in range(n_iter):
            temperature = self.schedule(t)
            
            # Randomly choose a neighbor path
            neighbors = self.Neighbor(current_state.path)
            nextMove = neighbors[np.random.randint(len(neighbors))]
            nextValue = self.calculate_distance(nextMove)

            # Accept the new state if it improves the solution
            if nextValue < best_state.value:
                best_state.path = nextMove
                best_state.value = nextValue

            # If the new state is better than the current state, accept it
            if nextValue < current_state.value:
                current_state.path = nextMove
                current_state.value = nextValue
            else:  # New state is worse
                E = -abs(nextValue - current_state.value)  # Energy difference
                p_accept = np.exp(E / temperature)  # Acceptance probability
                if np.random.rand() < p_accept:
                    current_state.path = nextMove
                    current_state.value = nextValue
            
            # Logging progress
            if t % 100 == 0:
                times.append(t)
                values.append(best_state.value)
                print(f"Iteration {t}: Best path {best_state.path} with value {best_state.value}")
        
        return best_state