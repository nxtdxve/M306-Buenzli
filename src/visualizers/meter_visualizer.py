import matplotlib.pyplot as plt
from numpy import block

class MeterVisualizer:
    def __init__(self, data_path):
        self.data_path = data_path
        self.data = None

    def process_files(self, processor):
        processor_instance = processor(self.data_path)
        processor_instance.process_files()
        self.data = processor_instance.get_data_for_plotting()

    def plot_data(self):
        if self.data is None:
            print("No data available for plotting.")
            return

        plt.figure(figsize=(14, 6))
        plt.plot(self.data.index, self.data['Consumption'], label='Consumption')
        plt.plot(self.data.index, self.data['Production'], label='Production')
        plt.xlabel('Timestamp')
        plt.ylabel('Usage')
        plt.title('Consumption and Production Over Time')
        plt.legend()
        plt.show(block=False)
