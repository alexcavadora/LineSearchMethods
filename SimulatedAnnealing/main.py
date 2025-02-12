import random as rn
import itertools
from SimulatedAnnealing import SimAnn

import numpy as np
import matplotlib.pyplot as plt
from parser import parser


def plotArch(point1, point2, dist=1):
    # Define the center of the circle that forms the arch
    center = (point1 + point2) / 2 + np.array([0, 1])  # Shift up for an arch
    # Compute the radius
    radius = np.linalg.norm(point1 - center)

    # Compute angles for the arc
    theta1 = np.arctan2(point1[1] - center[1], point1[0] - center[0])
    theta2 = np.arctan2(point2[1] - center[1], point2[0] - center[0])
    theta = np.linspace(theta1, theta2, 100)

    # Parametric equation for the arc
    x = center[0] + radius * np.cos(theta)
    y = center[1] + radius * np.sin(theta)
    return x, y

    # plt.scatter([point1[0], point2[0]], [point1[1], point2[1]], color='red', zorder=3)  # Mark endpoints





def plot2D(idx_perm, data):
    coord_x = [data["xy"][i][0] for i in range(len(data["xy"]))]
    coord_y = [data["xy"][i][1] for i in range(len(data["xy"]))]

    max_d =  max(max(data["distances"]))
    min_d =  min(min(data["distances"]))

    # Crear el gráfico de puntos
    plt.scatter(coord_x, coord_y, c='b')

    # Conectar los puntos con una línea gris usando idx_perm
    for i in range(len(idx_perm)):
        start_idx = idx_perm[i]
        end_idx = idx_perm[(i + 1) % len(idx_perm)]
        x, y = plotArch(np.array([coord_x[start_idx], coord_y[start_idx]]), np.array([coord_x[end_idx], coord_y[end_idx]]))
        grad = (data["distances"][start_idx][end_idx] - min_d) / (max_d - min_d)
        plt.plot(x, y, 'b-', linewidth=2 , alpha=grad)

    # Añadir títulos y etiquetas
    plt.title('Ciudades')
    plt.xlabel('Coord X')
    plt.ylabel('Coord Y')

    # Mostrar el gráfico
    plt.show()

def main():
    # Load and parse the dataset
    with open("./dataset/rc_201.1.txt") as f:
        fileContent = f.read()

    data = parser(fileContent)

    # Initialize Simulated Annealing
    sm = SimAnn(data)

    # Run the Simulated Annealing algorithm for 1000 iterations
    best_solution = sm.simulated_annealing(1000)

    # Plot the best path found
    print("Best Path:", best_solution.path)
    print("Best Value (Distance):", best_solution.value)

    # Plot the best solution
    plot2D(best_solution.path, data)


if __name__ == "__main__":
    main()