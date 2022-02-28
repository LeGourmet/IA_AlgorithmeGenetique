import random as rd

class individu:
    def __init__(self, size):
        self.gene = None
        self.generate_population(size)

    def fitness(self,data):
        return

    def generate_population(self, size):
        self.gene = rd.sample(range(size), size)
