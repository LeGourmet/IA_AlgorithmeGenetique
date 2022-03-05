from individu import *
import numpy as np
import random as rd


def generateGenome(size):
    """generate a new random genome, each nuber is unique
    Args: size : size of the genome
    """
    return rd.sample(range(size), size)


def newGen(parents, nbchild, data):
    """breeds a new generation from given parents

    Args:
        parents : Genes of the parents
        nbchild : number of children to produce
    """
    var = int(np.ceil(nbchild / len(parents)))  # nb de baise/parents
    childrens = []
    honeyMoon = []                          # tableau de chasse de chaque parent

    for i in range(len(parents)):
        tmp = np.arange(0, len(parents))    # tous les parents possible
        tmp = np.delete(tmp, i)                   # un parents ne se baise pas lui meme
        np.random.shuffle(tmp)              # randomise le tout
        honeyMoon.append(tmp[:var])         # prend les premiers parents
    honeyMoon = np.transpose(np.array(honeyMoon))

    for c in range(nbchild):
        i = c // var
        j = c % var
        childrens.append(croisement(parents[i].genome, parents[honeyMoon[j][i]].genome, data))
        # Todo mutation

    return childrens


def croisement(p1, p2, data):
    size = len(p1)
    done = [False] * size
    cycles = []

    # identifie les cycles
    for i in range(size):
        if done[i]:
            continue
        done[i] = True
        cycles.append([i])
        gene = p2[i]

        while gene != p1[i]:
            indice = p1.index(gene)
            done[indice] = True
            cycles[-1].append(indice)
            gene = p2[indice]

    # creer fils (recombine les cycles)
    b = False
    genome = []

    for c in cycles:
        for i in c:
            genome.append(p1[i] if b else p2[i])
        b = not b

    return Individu(genome, data)
