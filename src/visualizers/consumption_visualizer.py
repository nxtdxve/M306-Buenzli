import matplotlib.pyplot as plt

class ConsumptionVisualizer:
    def __init__(self, data):
        self.data = data

    def plot_data(self):
        plt.figure(figsize=(14, 6))
        plt.plot(self.data.index, self.data['Consumption'], label='Consumption')
        plt.plot(self.data.index, self.data['Production'], label='Production')
        plt.xlabel('Timestamp')
        plt.ylabel('Volume')
        plt.title('Consumption and Production Over Time')
        plt.legend()
        plt.show()

    def show(self):
        self.plot_data()
