import math


class Individual:
    """An individual holds a genome and loss is computed at creation"""
    def __init__(self, genome, data):
        """Creates an individual

        Args:
            genome (int[n]): the genome of the individual
            data (int[n][2]): data to compute loss"""
        self.genome = genome
        self.loss = 0
        self.compute_loss(data)

    def compute_loss(self, data):
        """compute the loss for a given genome

        Args:
            data (int[n][2]): the data to browse to compute loss"""
        self.loss = 0
        for i in range(len(self.genome)):
            self.loss += math.dist(data[self.genome[i - 1]], data[self.genome[i]])

    def __str__(self) -> str:
        return("fit " + str(self.loss) + ", gene:" + str(self.genome))
