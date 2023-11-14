from typing import List
from models import SolverABC
from models import Request

class GeneticAlgorithmSolver(SolverABC):
    def init(self, populationsize: int, generations: int, mutationrate: float) -> None:
        self.populationsize = populationsize
        self.generations = generations
        self.mutationrate = mutationrate

    def solve(self, r: Request) -> List[int]:
        # Initialize population
        population = self.initialpopulation(r)

        for i in range(self.generations):
            # Evaluate fitness of each individual
            fitnessscores = self.calculatefitnessscores(population, r)

            # Select parents for mating
            parents = self.selectparents(population, fitnessscores)

            # Generate offspring
            offspring = self.generateoffspring(parents)

            # Mutate offspring
            mutatedoffspring = self.mutateoffspring(offspring)

            # Select new population for the next generation
            population = self.selectnewpopulation(population, mutatedoffspring)

        # Select the best individual as the solution
        bestindividual = self.selectbestindividual(population, r)

        return bestindividual

    def initialpopulation(self, r: Request) -> List[List[int]]:
        return [i for i in range(1, r.points_number) for i in range(self.populationsize)]

    def calculatefitnessscores(self, population: List[List[int]], r: Request) -> List[float]:
        fitnessscores = 
        for individual in population:
            fitnessscore = self.calculatefitnessscore(individual, r)
            fitnessscores.append(fitnessscore)
        return fitnessscores

    def calculatefitnessscore(self, individual: List[int], r: Request) -> float:
        # TODO: Implement fitness score calculation
        pass

    def selectparents(self, population: List[List[int]], fitnessscores: List[float]) -> List[List[int]]:
        parents = []
        # TODO: Implement parent selection using fitness scores
        return parents

    def generateoffspring(self, parents: List[List[int]]) -> List[List[int]]:
        offspring = []
        # TODO: Implement offspring generation using parents
        return offspring

    def mutateoffspring(self, offspring: List[List[int]]) -> List[List[int]]:
        mutatedoffspring = 
        # TODO: Implement offspring mutation
        return mutatedoffspring

    def selectnewpopulation(self, population: List[List[int]], offspring: List[List[int]]) -> List[List[int]]:
        newpopulation = []
        # TODO: Implement new population selection
        return newpopulation

    def selectbestindividual(self, population: List[List[int]], r: Request) -> List[int]:
        bestindividual = population[0]
        bestfitnessscore = self.calculatefitnessscore(bestindividual, r)
        for individual in population[1]:
            fitnessscore = self.calculatefitnessscore(individual, r)
            if fitnessscore > bestfitnessscore:
                bestindividual = individual
                bestfitnessscore = fitnessscore
        return bestindividual