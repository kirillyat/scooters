import numpy as np
import matplotlib.pyplot as plt

# Чтение матрицы расстояний из файла
def read_distance_matrix(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        distance_matrix = []
        for line in lines:
            row = list(map(int, line.strip().split()))
            distance_matrix.append(row)
    return distance_matrix

# Чтение вектора приоритетов из файла
def read_priority_vector(file_path):
    with open(file_path, 'r') as file:
        line = file.readline()
        priority_vector = list(map(float, line.strip().split()))
    return priority_vector

# Рисование графа
def draw_graph(distance_matrix, priority_vector):
    n = len(distance_matrix)  # Количество вершин в графе

    # Расчет координат вершин графа
    angles = np.linspace(0, 2*np.pi, n, endpoint=False)
    x = np.cos(angles)
    y = np.sin(angles)

    # Рисование ребер графа
    for i in range(n):
        for j in range(i+1, n):
            plt.plot([x[i], x[j]], [y[i], y[j]], color='gray')

    # Рисование вершин графа с учетом вектора приоритетов
    for i in range(n):
        plt.scatter(x[i], y[i], s=500*priority_vector[i], color='red')

    # Добавление номеров вершин
    for i in range(n):
        plt.text(x[i], y[i], str(i+1), ha='center', va='center', color='black')

    # Настройки графика
    plt.axis('off')
    plt.title('Граф с учетом приоритетов')

    # Отображение графика
    plt.show()

# Главная функция
def main():
    file_path = input("Введите путь к файлу: ")
    distance_matrix = read_distance_matrix(file_path)
    priority_vector_file_path = input("Введите путь к файлу с вектором приоритетов: ")
    priority_vector = read_priority_vector(priority_vector_file_path)
    draw_graph(distance_matrix, priority_vector)

# Запуск программы
if __name__ == "__main__":
    main()

