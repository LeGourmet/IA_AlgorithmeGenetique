import numpy as np


def newGen(parents, nbchild):
    # nb de baise/parents
    var = np.ceil(nbchild/parents)
    children = np.array(None)
    # tableau de chasse de chaque parent
    honeyMoon = np.array(None)

    for i in range(len(parents)):
        # tous les parents possible
        tmp = np.arange(0, len(parents))
        # un parents ne se baise pas lui meme
        np.delete(tmp, i)
        # randomise le tout
        np.random.shuffle(tmp)
        # prend les premiers parents
        np.append(honeyMoon, tmp[:var])
    # transpose la matrice
    np.rot90(honeyMoon)

    for c in range(nbchild):
        i = c//var
        j = c%var

        np.append(children, croisement(parents[j], parents[honeyMoon[i][j]]))

    return children


def croisement(p1, p2):
    return