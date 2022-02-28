import numpy as np
from tqdm import tqdm
from data_manager import *
from view_manager import *

epoch = 20


def run():
    dm = DataManager()
    loss = []
    indices = None

    for _ in tqdm(range(epoch)):
        indices = dm.generate_population()
        loss.append(0)

    vm = ViewManager(loss, dm.data[np.array(indices)])
    vm.draw()


if __name__ == '__main__':
    run()
