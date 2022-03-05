import math


class Individu:
    def __init__(self, genome, data):
        self.genome = genome
        self.loss = 0
        self.compute_loss(data)
        self.age = 0

    def compute_loss(self, data):
        self.loss = 0
        for i in range(len(self.genome)):
            self.loss += math.dist(data[self.genome[i - 1]], data[self.genome[i]])

    def __str__(self) -> str:
        return("fit " + str(self.loss) + ", gene:" + str(self.genome))
