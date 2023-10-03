from data_processors.sdat_processor import SDATProcessor  # Importieren Sie SDATProcessor aus dem data_processors-Ordner
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plot_data(data):
    # create the root window
    root = tk.Tk()
    root.title("SDAT-Plotter")
    root.geometry("800x600")

    # create the plot
    fig = plt.figure(figsize=(14, 6))
    ax = fig.add_subplot(111)
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Volume')
    ax.set_title('Consumption and Production Over Time')
    ax.legend()

    # create the canvas
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

    root.mainloop()

if __name__ == '__main__':
    # Erstellen Sie eine Instanz von SDATProcessor und verarbeiten Sie die Dateien
    processor = SDATProcessor('./data/SDAT-Files/')  # Pfad könnte je nach Struktur unterschiedlich sein
    processor.process_files()
    
    # Daten für das Plotting abrufen
    data_for_plotting = processor.get_data_for_plotting()

    # Daten plotten
    plot_data(data_for_plotting)
