import networkx as nx
import numpy as np

# Чтение матрицы расстояний из файла
def read_distance_matrix(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        distance_matrix = []
        for line in lines:
            row = list(map(int, line.strip().split()))
            distance_matrix.append(row)
    return np.array(distance_matrix)

G =nx.DiGraph(read_distance_matrix('matrix.txt'))
nx.draw(G)

