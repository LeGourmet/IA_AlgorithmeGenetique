import math


class Individu:
    def __init__(self, genome, data):
        self.genome = genome
        self.fit = 0
        self.fitness(data)

    def fitness(self, data):
        for i in range(len(self.genome)):
            self.fit += math.dist(data[self.genome[i-1]], data[self.genome[i]])
