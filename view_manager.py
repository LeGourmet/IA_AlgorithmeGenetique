import matplotlib.pyplot as plt
from numpy import block

from data_manager import DataManager


class ViewManager:
    def __init__(self):
        # plt.ion()
        self.figure, axes = plt.subplots(1, 2, figsize=(10, 4))
        axes[0].set_aspect(1)

        self.fig_path = axes[0]
        self.fig_loss = axes[1]
        # plt.tight_layout()

    def update(self, losses, best_path, final=False):
        self.fig_path.clear()
        self.fig_loss.clear()
        for i in range(len(best_path)):
            self.fig_path.plot([best_path[i - 1][0], best_path[i][0]], [best_path[i - 1][1], best_path[i][1]])
        for point in best_path:
            self.fig_path.plot(point[0], point[1], marker='o')

        self.fig_loss.set_xlabel('Epoch')
        self.fig_loss.set_ylabel('Loss')
        self.fig_loss.plot(losses)

        if final:
            plt.show(block=True)
        else:
            plt.pause(0.01)
