import math


class Individu:
    def __init__(self, genome, data):
        self.genome = genome
        self.fit = 0
        self.fitness(data)

    def fitness(self, data):
        self.fit = 0
        for i in range(len(self.genome)):
            self.fit += math.dist(data[self.genome[i - 1]], data[self.genome[i]])

    def __str__(self) -> str:
        return("fit " + str(self.fit) + ", gene:" + str(self.genome))
