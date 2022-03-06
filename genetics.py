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
    # population_size, nb_parents_kept, children = keep_parents(population, keep)
    breed_per_parents, honeyMoon = get_mating_pool(population, population_size)
    # todo find a betterway to breed parents when nb_parents or nb_children is small (avoid out of range)
    return evolve(population, population_size, mutation_rate, data, breed_per_parents, honeyMoon)


def evolve(population, population_size, mutation_rate, data, breed_per_parents, honeyMoon):
    children = []
    for c in (range(population_size)):
        i = c // breed_per_parents
        j = c % breed_per_parents
        g1 = population[i].genome
        g2 = population[honeyMoon[i][j]].genome
        new_genome = crossover(g1, g2)
        new_genome = mutation(new_genome, mutation_rate)
        children.append(Individu(new_genome, data))
    return children


def get_mating_pool(population, population_size):
    breed_per_parents = int(np.ceil(population_size / len(population)))  # nb de baise/parents
    honeyMoon = []  # tableau de chasse de chaque parent
    for i in range(len(population)):
        tmp = np.arange(0, len(population))    # tous les parents possible
        tmp = np.delete(tmp, i)                # un parents ne se baise pas lui meme
        # randomise le tout - todo check si nécéssaire (plus rapide avec shuffle, what ? )
        np.random.shuffle(tmp)
        honeyMoon.append(tmp[:breed_per_parents])         # prend les premiers parents
    honeyMoon = (np.array(honeyMoon))
    return breed_per_parents, honeyMoon


def keep_parents(population, keep):
    # unused
    population_size = len(population)
    nb_parents_kept = population_size * keep
    childrentemp = population[:int(nb_parents_kept)]
    children = [c for c in childrentemp if c.age > 5]
    nb_parents_kept = len(children)
    return population_size, nb_parents_kept, children


# todo return 2 children
def crossover(g1, g2):
    size = len(g1)
    gene_already_treated = [False] * size
    cycles = []

    # identifie les cycles
    for gene1 in range(size):
        if gene_already_treated[gene1]:
            continue
        gene_already_treated[gene1] = True
        cycles.append([gene1])
        gene2 = g2[gene1]

        while gene2 != g1[gene1]:
            gene_index = g1.index(gene2)
            gene_already_treated[gene_index] = True
            cycles[-1].append(gene_index)
            gene2 = g2[gene_index]

    # creer fils (recombine les cycles)
    alternate_cycle = False
    genome = []

    for cycle in cycles:
        for gene2 in cycle:
            genome.append(g1[gene2] if alternate_cycle else g2[gene2])
        alternate_cycle = not alternate_cycle

    return genome


def crossover2(g1, g2):
    offspring1 = []
    offspring2 = []

    cut1 = rd.randint(0, len(g1))
    cut2 = rd.randint(0, len(g2))

    start = min(cut1, cut2)
    end = max(cut1, cut2)

    for i in range(start, end):
        offspring1.append(g1[i])

    offspring2 = [g for g in g2 if g not in offspring1]

    return offspring1 + offspring2


def crossover3(g1, g2):
    offspring1 = []
    offspring2 = []

    cut = rd.randint(0, len(g1))

    for i in range(0, cut):
        offspring1.append(g1[i])

    offspring2 = [g for g in g2 if g not in offspring1]

    return offspring1 + offspring2


def mutation(genome, mutation_rate: float):
    nb_genes = len(genome) - 1
    for index1 in range(len(genome)):
        if(rd.random() < mutation_rate):
            index2 = rd.randint(0, nb_genes)
            genome[index1], genome[index2] = genome[index2], genome[index1]
    return genome


def mutation2(genome, mutation_rate: float):
    nb_genes = len(genome) - 1
    for _ in range(nb_genes):
        if(rd.random() < mutation_rate):
            index1 = rd.randint(0, nb_genes)
            index2 = rd.randint(0, nb_genes)
            genome[index1], genome[index2] = genome[index2], genome[index1]
    return genome


def mutation3(genome, mutation_rate: float):
    if(rd.random() > mutation_rate):
        return genome
    nb_genes = len(genome) - 1
    nb_mutations = int(np.ceil(nb_genes * rd.random()))
    for _ in range(nb_mutations):
        index1 = rd.randint(0, nb_genes)
        index2 = rd.randint(0, nb_genes)
        genome[index1], genome[index2] = genome[index2], genome[index1]
    return genome


if __name__ == '__main__':
    dm = DataManager()

    population = []

    for _ in tqdm(range(100)):
        population.append(Individu(generateGenome(dm.size), dm.data))

    gene = population[0].genome
    print("==>> population[0].genome: ", gene)
