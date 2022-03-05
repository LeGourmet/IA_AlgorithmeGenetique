from typing import List
from data_manager import DataManager
from individu import *
import numpy as np
import random as rd
from tqdm import tqdm


def generateGenome(size):
    """generate a new random genome, each number is unique
    Args: size : size of the genome
    """
    return rd.sample(range(size), size)


def newGen(population, population_size, mutation_rate, data):
    """breeds a new generation from given parents

    Args:
        parents : Genes of the parents
        nbchild : number of children to produce
        mutation_rate : Percent of genes to modify
    """
    children = []
    # population_size, nb_parents_kept, children = keep_parents(population, keep)

    breed_per_parents = int(np.ceil(population_size / len(population)))  # nb de baise/parents
    honeyMoon = []  # tableau de chasse de chaque parent

    for i in range(len(population)):
        tmp = np.arange(0, len(population))    # tous les parents possible
        tmp = np.delete(tmp, i)                # un parents ne se baise pas lui meme
        # randomise le tout - todo check si nécéssaire (plus rapide avec shuffle, what ? )
        np.random.shuffle(tmp)
        honeyMoon.append(tmp[:breed_per_parents])         # prend les premiers parents
    honeyMoon = (np.array(honeyMoon))

    # todo find a betterway to breed parents when nb_parents && nb_children is small
    for c in range(population_size):
        i = c // breed_per_parents
        j = c % breed_per_parents
        g1 = population[i].genome
        g2 = population[honeyMoon[i][j]].genome
        new_genome = crossover(g1, g2)
        new_genome = mutation(new_genome, mutation_rate)
        children.append(Individu(new_genome, data))
    np.random.shuffle(children)

    # for c in children:
    # c.genome = mutation(c.genome, mutation_rate)
    # c.age += 1

    return children


def keep_parents(population, keep):
    population_size = len(population)
    nb_parents_kept = population_size * keep
    childrentemp = population[:int(nb_parents_kept)]
    children = [c for c in childrentemp if c.age > 5]
    nb_parents_kept = len(children)
    return population_size, nb_parents_kept, children


# todo return 2 children
def crossover(g1, g2):
    size = len(g1)
    done = [False] * size
    cycles = []

    # identifie les cycles
    for i in range(size):
        if done[i]:
            continue
        done[i] = True
        cycles.append([i])
        gene = g2[i]

        while gene != g1[i]:
            indice = g1.index(gene)
            done[indice] = True
            cycles[-1].append(indice)
            gene = g2[indice]

    # creer fils (recombine les cycles)
    b = False
    genome = []

    for c in cycles:
        for i in c:
            genome.append(g1[i] if b else g2[i])
        b = not b

    return genome


def mutation(genome, mutation_rate: float):
    if(rd.random() > mutation_rate):
        return genome
    nb_genes = len(genome)-1
    mutation_rate = np.clip(mutation_rate, 0.0, 1.0)
    nb_mutations = int(np.ceil(nb_genes * rd.random()))

    for _ in range(nb_mutations):
        index1 = rd.randint(0, nb_genes)  # gene to mutate (index)
        index2 = rd.randint(0, nb_genes)  # gene to mutate (index)
        gene1 = genome[index1]
        gene2 = genome[index2]
        genome[index2] = gene1
        genome[index1] = gene2

    return genome


if __name__ == '__main__':
    dm = DataManager()

    population = []

    for _ in tqdm(range(100)):
        population.append(Individu(generateGenome(dm.size), dm.data))

    population[8].age = 8
    population[6].age = 8
    population[7].age = 8

    population = newGen(population, .2, 0.02, dm.data)

    gene = population[0].genome
    print("==>> population[0].genome: ", gene)
