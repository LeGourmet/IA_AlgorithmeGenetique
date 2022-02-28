import numpy as np
from tqdm import tqdm
from data_manager import *
from view_manager import *
from individu import *
from utils import *


epoch = 20
nbParents = 100
keep = 0.2


def run():
    dm = DataManager()
    nbBest = nbParents * keep
    parents = np.array(None)
    fit = np.array(None)
    children = None
    loss = []

    # init parents and compute fitness
    for i in range(nbParents):
        np.append(parents, individu(dm.size))
        np.append(fit, parents[i].fitness(dm.data))

    for _ in tqdm(range(epoch)):
        # sort parent and keep best
        best = parents[(fit.argsort())[:nbBest]]
        loss.append(best[0].fitness(dm.data))

        # croisement & mutation
        children = newGen(best, nbParents)

    # sort
    loss.append(children[0].fitness(dm.data))
    vm = ViewManager(loss, dm.data[np.array(indices)])
    vm.draw()


if __name__ == '__main__':
    run()
