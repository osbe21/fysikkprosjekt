import matplotlib.pyplot as plt


class DataLogger:
    def __init__(self, label):
        self.label = label
        self.x = []
        self.y = []
    
    def log(self, x, y):
        self.x.append(x)
        self.y.append(y)
    
    def plot(self):
        plt.plot(self.x, self.y, label=self.label)