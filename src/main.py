from tqdm import tqdm
from data_manager import *
from view_manager import *
from individual import *
from genetics import *
import numpy as np

# data
file = "./data/circle_50.npy"
# file = "./"  # uncomment to load random data instead of file
data_size = 50

# stop conditions
max_epoch = 2000
target_loss = 5

# training parameters
keep_percent = 0.18
population_size = 100
mutation_rate = 0.006

# display options
refresh = 10
show_progress = True  # real time plot, but slower

# Managers
data_manager = DataManager(file=file, size=data_size)
view_manager = ViewManager()


def initialize_population(losses):
    """initialize random population and find the best individual, fill the first loss
    TheOne is the best individual across the whole evolution

    Args:
        data_manager (DataManager): the data manager
        losses (float[]): loss over time

    Returns:
        Individual, Individual[]: the best individual, the whole population
    """
    population = []
    for _ in range(population_size):
        population.append(Individual(generateGenome(data_manager.size), data_manager.data))
    population = sort_population(population)
    losses.append(population[0].loss)
    theOne = population[0]
    return theOne, population


def update_evolution_graph(losses, first_individual, final=False):
    """display on screen the graph of losses and best path

    Args:
        losses (float[]): loss over time
        last_gene (Individual): Individual from whom the path will be displayed
        final (bool, optional): Locks the plot for final display. Defaults to False.
    """
    best_gene = np.array(first_individual.genome)
    best_path = data_manager.data[best_gene]
    if show_progress:
        view_manager.update(losses, best_path)
    if final:
        view_manager.freeze(losses, best_path)


def disaply_evolution_info(last_individual, losses, theOne, epoch):
    """display in both the terminal and in a window the advancement of the evolution

    Args:
        last_individual (Individual): the individual to display
        losses (float[]): loss over time
        theOne (Individual): best individual
        epoch (int): the epoch
    """
    if(epoch % (max_epoch // 10) == 0):  # update every 10% of progress
        print("\nEpoch :", epoch, "- loss :", losses[-1])
        print("Best loss :", theOne.loss, "at epoch ", np.argmin(losses), "\n")
    if(epoch % refresh == 0):
        update_evolution_graph(losses, last_individual)


def run_genetic(population, losses, theOne):
    """Do the genetic evolution,
    stops when the target or maximum number of epochs is reached

    Args:
        population (Individual[]): the population to evolve
        losses (float[]): loss over time
        theOne (Individual): best individual

    Returns:
        Individual: The best individual across all epochs
    """
    print("Genetic evolution in progress ...")

    for epoch in tqdm(range(max_epoch)):
        elite = population[:int(population_size * keep_percent)]
        population = newGen(elite, population_size, mutation_rate, data_manager.data)
        population = sort_population(population)
        theOne = update_loss(population[0], losses, theOne)

        if(losses[-1] < target_loss):
            break

        disaply_evolution_info(population[0], losses, theOne, epoch)

    print("\n(epoch", len(losses) - 1, ") - Finished genetic evolution")
    print("Best loss :", theOne.loss, "at epoch ", np.argmin(losses))
    return theOne


def update_loss(best_candidate, losses, theOne):
    """update the losses array and update theOne if new best is found

    Args:
        best_candidate (Individual): the best candidate to replace theOne and update loss
        losses (float[]): loss over time
        theOne (Individual): best individual

    Returns:
        (Individual): best individual
    """

    losses.append(best_candidate.loss)
    if theOne.loss > best_candidate.loss:
        theOne = best_candidate
    return theOne


def print_parameters():
    """display parameters"""
    print("==>> max_epoch: ", max_epoch)
    print("==>> population_size: ", population_size)
    print("==>> mutation_rate: ", mutation_rate)
    print("==>> target_loss: ", target_loss)
    print("==>> data_size: ", data_size)


def sort_population(population):
    """sort the population according to the loss of each individual

    Args:
        population (Individual[]): the population

    Returns:
        (Individual[]): the sorted population
    """
    population = sorted(population, key=lambda individu: individu.loss)
    return population


def run():
    print_parameters()

    losses = []

    theOne, population = initialize_population(losses)
    theOne = run_genetic(population, losses, theOne)
    update_evolution_graph(losses, theOne, final=True)


if __name__ == '__main__':
    run()
