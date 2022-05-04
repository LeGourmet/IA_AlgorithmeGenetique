from data_manager import DataManager
from individual import *
import numpy as np
import random as rd
from tqdm import tqdm


def generateGenome(size):
    """generate a new random genome, each number is unique
    Args: size : size of the genome
    """
    return rd.sample(range(size), size)


def newGen(selected_parents, target_size, mutation_rate, data):
    """Creates a new generation of children from given parents
    first a mating matrix is calculated, then the new gen is produced and returned

    Args:
        population (individual[m]): Parents already selected for next gen
        population_size (int): number of children to produce
        mutation_rate (float): mutation rate
        data (int[n][2]): the data to compute the loss of each new individual
    Returns:
        (individual[population_size]): the new generation
    """
    honeyMoon = get_mating_pool(selected_parents, target_size)

    # create children
    children_genes = breed_parents(selected_parents, honeyMoon)
    missing_genes = fill_missing_population(selected_parents, target_size, len(children_genes))
    children_genes += (missing_genes)

    # mutate children
    children_genes = [mutation(children_genes[i], mutation_rate) for i in range(target_size)]

    # create new individuals
    individuals = [Individual(children_genes[i], data) for i in range(target_size)]
    return individuals


def breed_parents(selected_parents, honeyMoon):
    """Breed evry provided parents according to the mating matrix
    Args: selected_parents (individual[m]): Parents already selected for next gen
          honeyMoon (int[m][n]): mating matrix """
    children_genes = []
    for i in range(honeyMoon.shape[0]):
        for j in range(honeyMoon.shape[1]):
            g1 = selected_parents[i].genome
            g2 = selected_parents[honeyMoon[i][j]].genome
            new_genome = crossover(g1, g2)
            children_genes.append(new_genome)
    return children_genes


def fill_missing_population(selected_parents, target_size, nb_child):
    """Fill the missing population with random parents until the target size is reached

    Args: selected_parents (individual[m]): Parents already selected for next gen
            target_size (int): number of children desired
            nb_child (int[n]): number of children already produced"""
    additional_genes = []
    if(nb_child < target_size):
        missing_cheildren = target_size - nb_child
        for i in range(missing_cheildren):
            random_selected = rd.randint(0, len(selected_parents) - 1)
            g1 = selected_parents[random_selected].genome
            additional_genes.append(g1)
    return additional_genes


def get_mating_pool(selected_population, target_size):
    """generates a mating matrix
    for each parent(row), there are corresponding parents to mate with (columns)

    Args:
        population (individual[n]): the parent population to generate the matrix from
        population_size (int): number of children to produce
    Returns:
        int, int[][]: number of breeds per parents, the mating matrix
    """
    selected_size = len(selected_population)
    breed_per_parents = np.ceil(target_size / selected_size).astype(int)
    honeyMoon = []  # mating matrix
    for i in range(selected_size):
        tmp = np.arange(0, len(selected_population))
        tmp = np.delete(tmp, i)  # remove self
        np.random.shuffle(tmp)
        honeyMoon.append(tmp[:breed_per_parents])  # only keep first parents

    honeyMoon = np.array(honeyMoon)
    # honeyMoon = np.transpose(honeyMoon)
    return honeyMoon


def crossover(g1, g2):
    """best crossover found
    Cycle crossover is used to avoid collisions,
    Cycles are found from g1 and g2, and then are alternatively added to the offspring.
    2 different offspring could be produced this way,
    but (g1,g2) will produce the complementary offspring from (g2, g1)

    Args:
        g1 (int[n]): gene 1
        g2 (int[n]): gene 2
    Returns:
        int[n]: crossover between g1 and g2
    """
    # init
    genome_size = len(g1)
    gene_already_treated = [False] * genome_size
    cycles = []
    genome = []

    # Cycle identification
    for gene1 in range(genome_size):
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

    # Offspring creation (alternate cycles)
    alternate_cycle = False
    for cycle in cycles:
        for gene2 in cycle:
            genome.append(g1[gene2] if alternate_cycle else g2[gene2])
        alternate_cycle = not alternate_cycle

    return genome


def crossover2(g1, g2):
    """Crossover 2 genes
    creates 2 cuts, genome from g1 is kept from 0 to cut1,
    then genome from g2 from cut1 to cut2
    and genome from g1 from cut2 to end
    Collision are taken into account, but this leads to loss of genetic information

    Args:
        g1 (int[n]): gene 1
        g2 (int[n]): gene 2
    Returns:
        int[n]: crossover between g1 and g2
    """
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
    """Crossover 2 genes
    Creates a cut, genome from g1 is kept from 0 to cut,
    Then genome from g2 from cut1 to end
    Collision are taken into account, but this leads to loss of genetic information

    Args:
        g1 (int[n]): gene 1
        g2 (int[n]): gene 2

    Returns:
        int[n]: crossover between g1 and g2
    """
    offspring1 = []
    offspring2 = []

    cut = rd.randint(0, len(g1))

    for i in range(0, cut):
        offspring1.append(g1[i])

    offspring2 = [g for g in g2 if g not in offspring1]

    return offspring1 + offspring2


def mutation(genome, mutation_rate: float):
    """mutates a genome
    This method is the best working so far,
    each gene is evaluated for a chance to mutate
    mutation is done by swapping a gene with another random one

    Args:
        genome (int[n]): gene to mutate
        mutation_rate (float): mutation probability
    Returns:
        int[n]: mutated gene
    """
    nb_genes = len(genome) - 1
    for index1 in range(nb_genes+1):
        if(rd.random() < mutation_rate):
            index2 = rd.randint(0, nb_genes)
            genome[index1], genome[index2] = genome[index2], genome[index1]
    return genome


def mutation2(genome, mutation_rate: float):
    """mutates a genome
    does a random roll for each gene,
    if roll is successful then 2 random genes are selected and swapped

    Args:
        genome (int[n]): gene to mutate
        mutation_rate (float): mutation probability
    Returns:
        int[n]: mutated gene
    """
    nb_genes = len(genome) - 1
    for _ in range(nb_genes):
        if(rd.random() < mutation_rate):
            index1 = rd.randint(0, nb_genes)
            index2 = rd.randint(0, nb_genes)
            genome[index1], genome[index2] = genome[index2], genome[index1]
    return genome


def mutation3(genome, mutation_rate: float):
    """mutates a genome
    does a random roll for mutation of the whole genome
    if roll is successful then a random number of genes are selected to be swapped

    Args:
        genome (int[n]): gene to mutate
        mutation_rate (float): mutation probability
    Returns:
        int[n]: mutated gene"""
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
    """script test"""
    dm = DataManager()

    population = []

    for _ in tqdm(range(100)):
        population.append(Individual(generateGenome(dm.size), dm.data))

    gene = population[0].genome
    print("==>> population[0].genome: ", gene)
