import numpy as np
import random as rd
from tqdm import tqdm


class DataManager:

    def __init__(self, file=None, size=np.inf):
        self.data = []
        self.size = size
        self.load_data(file, size)

    def load_data(self, file, size):
        print("Creating data ...")

        try:
            self.data = np.load("./arr.npy")
        except OSError:
            print("Could not load array")

        # for _ in tqdm(range(100)):
        #     self.data.append((rd.randint(0, 1000), rd.randint(0, 1000)))

        self.size = min(self.size, len(self.data))
        self.data = self.data[:self.size]
        self.data = np.array(self.data)


if __name__ == '__main__':
    dm = DataManager()
    data = (dm.data)
    print("==>> data: ", data)
    print("==>> type(data): ", type(data))
    print("==>> dm.size: ", dm.size)
    print("==>> data.shape: ", np.array(data).shape)
