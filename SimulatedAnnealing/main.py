import os
import numpy as np
import matplotlib.pyplot as plt

from Parser import parser
from SimulatedAnnealing import SimAnn

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

def plot2D(idx_perm, data, total_distance):
    coord_x = [data["xy"][i][0] for i in range(len(data["xy"]))]
    coord_y = [data["xy"][i][1] for i in range(len(data["xy"]))]

    # Crear el gráfico de puntos
    plt.figure(figsize=(10, 7))
    plt.style.use('ggplot')
    plt.scatter(coord_x, coord_y, c='gray')
    # Anotar los índices de los puntos en cada punto
    for i, (x, y) in enumerate(zip(coord_x, coord_y)):
        plt.text(x, y, str(i), fontsize=12, ha='right')

    # Conectar los puntos con una línea gris usando idx_perm
    for i in range(len(idx_perm)):
        start_idx = idx_perm[i]
        end_idx = idx_perm[(i + 1) % len(idx_perm)]
        x, y = plotArch(np.array([coord_x[start_idx], coord_y[start_idx]]), np.array([coord_x[end_idx], coord_y[end_idx]]))
        distances = [data["distances"][start_idx][end_idx] for start_idx, end_idx in zip(idx_perm, idx_perm[1:] + idx_perm[:1])]
        q1, q2, q3 = np.percentile(distances, [25, 50, 75])
        
        if data["distances"][start_idx][end_idx] <= q1:
            alpha = 0.2
        elif data["distances"][start_idx][end_idx] <= q2:
            alpha = 0.4
        elif data["distances"][start_idx][end_idx] <= q3:
            alpha = 0.6
        else:
            alpha = 0.8        
        plt.plot(x, y, 'c-', linewidth=2, alpha=alpha)


    # Añadir títulos y etiquetas
    plt.title(f"Distancias Ciudades \n Total Distance: {total_distance}")
    plt.xlabel('Coord X')
    plt.ylabel('Coord Y')

    # Mostrar el gráfico
    plt.show()

def main():
    # Load and parse the dataset
    with open(os.path.join(__file__, "../dataset/rc_201.1.txt")) as f:
        fileContent = f.read()

    data = parser(fileContent)

    # Initialize Simulated Annealing
    sm = SimAnn(data, optmode=2)

    # Run the Simulated Annealing algorithm for 1000 iterations
    best_solution = sm.simulated_annealing(1000)

    # Plot the best path found
    print("Best Path:", best_solution.path)
    print("Best Value (Distance):", best_solution.value)

    # Plot the best solution
    plot2D(best_solution.path, data, best_solution.value)


if __name__ == "__main__":
    main()