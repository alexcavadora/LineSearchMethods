import os
import numpy as np
import matplotlib.pyplot as plt
from time import time

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

def plotCurve2D(idx_perm, data, total_distance):
    coord_x = [data["xy"][i][0] for i in range(len(data["xy"]))]
    coord_y = [data["xy"][i][1] for i in range(len(data["xy"]))]

    # Crear el gráfico de puntos
    plt.figure(figsize=(10, 7))
    plt.style.use('ggplot')
    plt.scatter(coord_x, coord_y, c='gray')
    # Anotar los índices de los puntos en cada punto
    for i, (x, y) in enumerate(zip(coord_x, coord_y)):
        plt.text(x, y, str(i), fontsize=12, ha='right')

    # Conectar los puntos con una línea curva usando idx_perm
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

def plot2D(idx_perm, data, total_distance,index = False, curve=False, log=False):
    coord_x = [data["xy"][i][0] for i in range(len(data["xy"]))]
    coord_y = [data["xy"][i][1] for i in range(len(data["xy"]))]

    if log:
        coord_y = np.log(coord_y)

    # Crear el gráfico de puntos
    plt.figure(figsize=(10, 7))
    plt.style.use('ggplot')
    plt.scatter(coord_x, coord_y, c='gray')
    if index:
    # Anotar los índices de los puntos en cada punto
        for i, (x, y) in enumerate(zip(coord_x, coord_y)):
            plt.text(x, y, str(i), fontsize=12, ha='right')

    if curve:
    # Conectar los puntos con una línea curva usando idx_perm
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
    else:
    # Conectar los puntos con una línea recta gris usando idx_perm
        for i in range(len(idx_perm)):
            start_idx = idx_perm[i]
            end_idx = idx_perm[(i + 1) % len(idx_perm)]
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
            plt.plot([coord_x[start_idx], coord_x[end_idx]], [coord_y[start_idx], coord_y[end_idx]], 'c-', linewidth=2, alpha=alpha)

    # Añadir títulos y etiquetas
    plt.title(f"Distancias Ciudades \n Total Distance: {total_distance}")
    plt.xlabel('Coord X')
    plt.ylabel('Coord Y')

    # Mostrar el gráfico
    plt.show()


def main():
    # Load and parse the dataset
    with open(os.path.join(__file__, "../dataset/n200w140.002.txt")) as f:
        fileContent = f.read()

    data = parser(fileContent)

    # Initialize Simulated Annealing
    sm = SimAnn(data, optmode=2, C=100, p=0.75)  # C [50, 100, 200], p [0.9, ,1.0, 1.1]

    # Run the Simulated Annealing algorithm for 10,000 iterations
    start = time()

    best_solution = sm.simulated_annealing(30000)
    end = time()

    # Plot the best path found
    print("Best Path:", best_solution.path)
    print("Best Value (Distance):", best_solution.value)
    print("Execution Time:", (end - start) / 60, "minutes")

    # Plot the best solution
    plot2D(best_solution.path, data, best_solution.value, curve=False, log=False)
    
    # sol = [151, 24, 107, 91, 95, 140, 184, 195, 161, 67, 82, 85, 169, 173, 78, 182, 9, 142, 159, 79, 176, 17, 90, 153, 81, 117, 27, 150, 113, 165, 57, 45, 2, 84, 89, 137, 80, 134, 103, 189, 177, 30, 135, 155, 63, 72, 122, 98, 13, 139, 114, 191, 164, 106, 94, 136, 144, 183, 160, 121, 193, 29, 51, 47, 175, 141, 52, 181, 197, 37, 33, 133, 62, 180, 32, 125, 86, 69, 143, 19, 71, 187, 116, 36, 64, 163, 131, 104, 31, 14, 124, 50, 171, 93, 178, 111, 92, 10, 185, 186, 66, 76, 138, 109, 115, 194, 42, 166, 190, 60, 5, 26, 97, 23, 192, 75, 73, 55, 168, 46, 3, 58, 77, 174, 65, 56, 128, 83, 20, 110, 120, 119, 145, 126, 7, 130, 100, 118, 199, 129, 53, 54, 21, 12, 158, 147, 44, 167, 39, 28, 146, 123, 170, 70, 99, 48, 18, 127, 35, 0, 132, 74, 172, 152, 6, 156, 179, 88, 188, 59, 198, 40, 15, 49, 11, 87, 200, 16, 112, 154, 101, 43, 157, 96, 41, 8, 22, 162, 68, 148, 102, 1, 105, 108, 196, 149, 4, 61, 38, 25, 34]
    # plot2D(sol, data, 986.0,index=False, curve=False, log=False), 


if __name__ == "__main__":
    main()