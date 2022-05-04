import numpy as np
import random as rd
from tqdm import tqdm


class DataManager:
    """generates data for the travelling salesman problem
    data is of form int[n][2]"""

    def __init__(self, file=None, size=50):
        """generate data from a file (numpy array format)
        If no file is found, then data is randomly generated

        Args:
            file (string, optional): The file to load data from. Defaults to None.
            size (int, optional): the to generate if no file is found. Defaults to 50."""
        self.data = []
        self.size = size
        self.load_data(file, size)

    def load_data(self, file, size):
        print("Creating data ...")

        try:
            self.data = np.load(file)
        except (OSError, TypeError):
            print("Could not load file, using random data instead")
            for _ in tqdm(range(size)):
                self.data.append((rd.random(), rd.random()))

        self.size = len(self.data)
        self.data = self.data[:self.size]
        self.data = np.array(self.data)


if __name__ == '__main__':
    dm = DataManager()
    data = (dm.data)
    print("==>> data: ", data)
    print("==>> type(data): ", type(data))
    print("==>> dm.size: ", dm.size)
    print("==>> data.shape: ", np.array(data).shape)
