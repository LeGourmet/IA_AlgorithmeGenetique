import os
import numpy as np
import random as rd
from tqdm import tqdm


class DataManager:
    def __init__(self, file=None):
        self.data = None
        self.size = None
        self.load_data(file)

    def load_data(self, file):
        if (file is not None) and (os.path.isfile("./model/" + file)):
            print("Loading", file, "...")
            # Todo
        else:
            self.size = 15
            tmp = []
            print("Creating data ...")
            for _ in tqdm(range(self.size)):
                tmp.append((rd.randint(2, 48), rd.randint(2, 48)))
            self.data = np.array(tmp)

    def generate_population(self):
        return rd.sample(range(self.size), self.size)
