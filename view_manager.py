import matplotlib.pyplot as plt


class ViewManager:
    """manages the display of evolution plot
    2 sub plots are displayed : the loss over time, and the best path found
    """
    def __init__(self):
        """Initialize the sub plots, square aspect ratio is used"""
        self.figure, axes = plt.subplots(1, 2, figsize=(10, 4))
        axes[0].set_aspect(1)

        self.fig_path = axes[0]
        self.fig_loss = axes[1]

    def update(self, losses, path, final=False):
        """Update the plot (resource intensive !)

        Args:
            losses (float[]): loss over time
            path (int[n][2]): path to display, data is ordered
            final (bool, optional): Locks the plot for final display. Defaults to False.
        """
        self.fig_path.clear()
        self.fig_loss.clear()
        for i in range(len(path)):
            self.fig_path.plot([path[i - 1][0], path[i][0]], [path[i - 1][1], path[i][1]])
        for point in path:
            self.fig_path.plot(point[0], point[1], marker='o')

        self.fig_loss.set_xlabel('Epoch')
        self.fig_loss.set_ylabel('Loss')
        self.fig_loss.plot(losses)

        if final:
            plt.show(block=True)
        else:
            plt.pause(0.01)
