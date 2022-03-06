from typing import final
from tqdm import tqdm
from data_manager import *
from view_manager import *
from individu import *
from genetics import *
import numpy as np


max_epoch = 2000
population_size = 100
keep = 0.2
mutation_rate = 0.007
target_loss = 3.14
data_size = 50
refresh = 20
show_progress = True  # real time plot, but slower


def initialize_population(dm, population, losses):
    # init population (gene + loss) and theOne
    for _ in range(population_size):
        population.append(Individu(generateGenome(dm.size), dm.data))
    population = sort_population(population)
    losses.append(population[0].loss)
    theOne = population[0]
    return theOne


def display_evolution_graph(vm, dm, losses, last_gene, final=False):
    best_gene = np.array(last_gene.genome)
    best_path = dm.data[best_gene]
    if show_progress:
        vm.update(losses, best_path)
    if final:
        vm.update(losses, best_path, final=True)


def disaply_evolution_info(vm, dm, population, losses, theOne, epoch):
    if(epoch % (max_epoch // 10) == 0):  # update every 10% of progress
        print("\nEpoch :", epoch, "- loss :", losses[-1])
        print("\nBest loss =", theOne.loss, "at epoch ", len(losses) - 1)
    if(epoch % refresh == 0):
        display_evolution_graph(vm, dm, losses, population[0])


def run_genetic(vm, dm, population, losses, theOne):
    print("Genetic evolution in progress ...")
    for epoch in tqdm(range(max_epoch)):
        elite = population[:int(population_size * keep)]
        population = newGen(elite, population_size, mutation_rate, dm.data)
        population = sort_population(population)
        theOne = update_loss(population, losses, theOne)
        disaply_evolution_info(vm, dm, population, losses, theOne, epoch)
        if(losses[-1] < target_loss):
            break
    print("\nFinished genentic evolution with best loss =", theOne.loss, "at epoch ", len(losses) - 1)
    return theOne


def update_loss(population, losses, theOne):
    losses.append(population[0].loss)
    if theOne.loss > population[0].loss:
        theOne = population[0]
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
    vm = ViewManager()
    population = []
    losses = []

    theOne = initialize_population(dm, population, losses)
    theOne = run_genetic(vm, dm, population, losses, theOne)
    display_evolution_graph(vm, dm, losses, theOne, final=True)


if __name__ == '__main__':
    run()
