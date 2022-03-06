from tqdm import tqdm
from data_manager import *
from view_manager import *
from individu import *
from genetics import *
import numpy as np


max_epoch = 8000
population_size = 100
keep = 0.2
mutation_rate = 0.001
target_loss = 4
# add max nb of block for mutations ?
# todo longévité des individus (ne pas tuer tous les individus à chaque epoch (cf tp)) (enfaitnon c'est pas top après avoir testé ... )


def run():
    dm = DataManager()
    population = []
    loss = []

    # init population (gene + loss) and theOne
    for _ in range(population_size):
        population.append(Individu(generateGenome(dm.size), dm.data))

    population = sorted(population, key=lambda individu: individu.loss)
    loss.append(population[0].loss)
    theOne = population[0]

    print("Genetic evolution in progress ...")
    for epoch in tqdm(range(max_epoch)):
        elite = population[:int(population_size * keep)]
        population = newGen(elite, population_size, mutation_rate, dm.data)
        population = sorted(population, key=lambda individu: individu.loss)
        loss.append(population[0].loss)
        if theOne.loss > population[0].loss:
            theOne = population[0]
        if(epoch % (max_epoch//10) == 0):
            print("\nEpoch :", epoch, "- loss :", loss[-1])
        if(loss[-1] < target_loss):
            break

    # todo update matplotlib per n iteration
    print("best loss =", theOne.loss)
    best_gene = np.array(theOne.genome)
    best_path = dm.data[best_gene]
    vm = ViewManager(loss, best_path)
    vm.draw()


if __name__ == '__main__':
    run()
