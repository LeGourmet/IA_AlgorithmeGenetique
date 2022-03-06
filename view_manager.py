import matplotlib.pyplot as plt


class ViewManager:
    def __init__(self):
        plt.ion()
        self.figure, axes = plt.subplots(1, 2)
        self.fig_path = axes[0]
        self.fig_loss = axes[1]

    def update(self, loss, data):
        self.fig_path.clear()
        self.fig_loss.clear()
        for i in range(len(data)):
            self.fig_path.plot([data[i - 1][0], data[i][0]], [data[i - 1][1], data[i][1]])
        for point in data:
            self.fig_path.plot(point[0], point[1], marker='o')

        self.fig_loss.set_xlabel('Epoch')
        self.fig_loss.set_ylabel('Loss')
        self.fig_loss.plot(loss)
        plt.pause(0.1)

        plt.tight_layout()
