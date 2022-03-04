import os
import random as rd
from tqdm import tqdm


class DataManager:
    def __init__(self, file=None, size=100):
        self.data = []
        self.size = 0
        self.load_data(file, size)

    def load_data(self, file, size):
        if (file is not None) and (os.path.isfile("./model/" + file)):
            print("Loading", file, "...")
            # Todo loader
        else:
            self.size = size
            print("Creating data ...")
            for _ in tqdm(range(self.size)):
                self.data.append((rd.randint(0, 1000), rd.randint(0, 1000)))
