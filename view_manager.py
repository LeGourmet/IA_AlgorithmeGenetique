import matplotlib.pyplot as plt


class ViewManager:
    def __init__(self, loss, data):
        self.loss_curve = loss
        self.lines = []
        self.points = []
        self.compute(data)

    def compute(self, data):
        self.points = data
        for i in range(len(data)):
            self.lines.append([[data[i - 1][0], data[i][0]], [data[i - 1][1], data[i][1]]])

    def draw(self):
        plt.figure()

        for line in self.lines:
            plt.plot(line[0], line[1])
        for point in self.points:
            plt.plot(point[0], point[1], marker='o')

        plt.figure()
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.plot(self.loss_curve)

        plt.show()
