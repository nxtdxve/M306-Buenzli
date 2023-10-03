# main.py

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from data_processors.sdat_processor import SDATProcessor
import matplotlib.pyplot as plt

def plot_data(data, root):
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(data.index, data['Consumption'], label='Consumption')
    ax.plot(data.index, data['Production'], label='Production')
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Volume')
    ax.set_title('Consumption and Production Over Time')
    ax.legend()
    
    # Embed the Matplotlib figure into tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

    # Add the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Matplotlib in Tkinter")
    
    # Erstellen Sie eine Instanz von SDATProcessor und verarbeiten Sie die Dateien
    processor = SDATProcessor('./data/SDAT-Files/')  # Pfad könnte je nach Struktur unterschiedlich sein
    processor.process_files()
    
    # Daten für das Plotting abrufen
    data_for_plotting = processor.get_data_for_plotting()

    # Daten plotten
    plot_data(data_for_plotting, root)
    root.mainloop()
