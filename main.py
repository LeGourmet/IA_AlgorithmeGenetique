from tqdm import tqdm
from data_manager import *
from view_manager import *
from individu import *
from utils import *
import numpy as np


epoch = 100
nbParents = 50
keep = 0.3
# add nb of mutations
# add nb of block for mutations

def run():
    dm = DataManager()
    population = []
    loss = []

    # init population (gene + fitness) and theOne
    for i in range(nbParents):
        population.append(Individu(generateGenome(dm.size), dm.data))
    population = sorted(population, key=lambda individu: individu.fit)
    loss.append(population[0].fit)
    theOne = population[0]

    for _ in tqdm(range(epoch)):
        population = newGen(population[:int(nbParents * keep)], nbParents, dm.data)
        population = sorted(population, key=lambda individu: individu.fit)
        loss.append(population[0].fit)
        if theOne.fit > population[0].fit:
            theOne = population[0]

    vm = ViewManager(loss, np.array(dm.data)[np.array(theOne.genome)])
    vm.draw()


if __name__ == '__main__':
    run()
