import os
import numpy as np
import random as rd
from tqdm import tqdm


class DataManager:
    def __init__(self, file=None):
        self.data = np.array(None)
        self.size = None
        self.load_data(file)

    def load_data(self, file):
        if (file is not None) and (os.path.isfile("./model/" + file)):
            print("Loading", file, "...")
            # Todo
        else:
            self.size = 15
            print("Creating data ...")
            for _ in tqdm(range(self.size)):
                np.append(self.data, (rd.randint(2, 48), rd.randint(2, 48)))
