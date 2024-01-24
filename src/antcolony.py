"""
В этом файле написана реализация алгоритма "Муравьиной колонии"
"""

import numpy as np
from src.models import Request


class AntAlgorithm:
    def __init__(
        self,
        request: Request,
        n_ants=200,
        n_iterations=20,
        alpha=2,
        beta=1,
        evaporation_rate=0.5,
    ):
        self.request = request
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.pheromone_trails = np.ones((request.points_number, request.points_number))
        self.best_cost = float("-inf")
        self.best_itenerary = []

    def _update_pheromones(self, ants):
        self.pheromone_trails *= 1 - self.evaporation_rate
        for ant in ants:
            contribution = self.request.cost(ant) if self.request.check(ant) else 0
            for i, j in zip(ant, ant[1:] + [ant[0]]):
                self.pheromone_trails[i][j] += contribution

    def _select_next_city(self, current_city, tabu_list):
        probabilities = []
        for i in range(self.request.points_number):
            if i not in tabu_list:
                trail = self.pheromone_trails[current_city][i] ** self.alpha
                visibility = (
                    1 / (self.request.time_matrix[current_city][i] + 1)
                ) ** self.beta
                probabilities.append(trail * visibility)
            else:
                probabilities.append(0)
        probabilities = probabilities / np.sum(probabilities)
        return np.random.choice(range(self.request.points_number), p=probabilities)

    def _construct_solution(self):
        tabu_list = [0]
        while len(tabu_list) <= self.request.capacity:
            current_city = tabu_list[-1]
            next_city = self._select_next_city(current_city, tabu_list)
            if (self.request.time - self.request.cost(tabu_list + [next_city])) >= 0:
                tabu_list.append(next_city)
            else:
                break
        return tabu_list

    def run(self):
        for iteration in range(self.n_iterations):
            ants = [self._construct_solution() for _ in range(self.n_ants)]
            self._update_pheromones(ants)
            for ant in ants:
                if self.request.check(ant):
                    cost = self.request.cost(ant)
                    if cost > self.best_cost:
                        self.best_cost = cost
                        self.best_itenerary = ant
        return self.best_itenerary
