from tqdm import tqdm
from data_manager import *
from view_manager import *
from individu import *
from genetics import *
import numpy as np


max_epoch = 1000
population_size = 100
keep = 0.2
mutation_rate = 0.006
target_loss = 3.14
data_size = 50
# add max nb of block for mutations ?
# todo longévité des individus (ne pas tuer tous les individus à chaque epoch (cf tp)) (enfaitnon c'est pas top après avoir testé ... )


def initialize_population(dm, population, losses):
    # init population (gene + loss) and theOne
    for _ in range(population_size):
        population.append(Individu(generateGenome(dm.size), dm.data))
    population = sort_population(population)
    losses.append(population[0].loss)
    theOne = population[0]
    return theOne


def display_evolution(dm, losses, theOne):
    # todo update matplotlib per n iteration
    print("best loss =", theOne.loss, "at epoch ", len(losses)-1)
    best_gene = np.array(theOne.genome)
    best_path = dm.data[best_gene]
    vm = ViewManager(losses, best_path)
    vm.draw()


def run_genetic(dm, population, losses, theOne):
    print("Genetic evolution in progress ...")
    for epoch in tqdm(range(max_epoch)):
        elite = population[:int(population_size * keep)]
        population = newGen(elite, population_size, mutation_rate, dm.data)
        population = sort_population(population)
        losses.append(population[0].loss)
        if theOne.loss > population[0].loss:
            theOne = population[0]
        if(epoch % (max_epoch//10) == 0):
            print("\nEpoch :", epoch, "- loss :", losses[-1])
        if(losses[-1] < target_loss):
            break
    return theOne


def print_parameters():
    print("==>> max_epoch: ", max_epoch)
    print("==>> population_size: ", population_size)
    print("==>> mutation_rate: ", mutation_rate)
    print("==>> target_loss: ", target_loss)
    print("==>> data_size: ", data_size)


def sort_population(population):
    population = sorted(population, key=lambda individu: individu.loss)
    return population


def run():
    print_parameters()

    file = "./circle50.npy"
    dm = DataManager(file=file, size=data_size)
    population = []
    losses = []

    theOne = initialize_population(dm, population, losses)
    theOne = run_genetic(dm, population, losses, theOne)
    display_evolution(dm, losses, theOne)


if __name__ == '__main__':
    run()
