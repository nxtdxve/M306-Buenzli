# main.py

from data_processors.esl_processor import ESLProcessor  # Importieren Sie SDATProcessor aus dem data_processors-Ordner
import matplotlib.pyplot as plt

def plot_data(data):
    plt.figure(figsize=(14, 6))
    plt.plot(data.index, data['Consumption'], label='Consumption')
    plt.plot(data.index, data['Production'], label='Production')
    plt.xlabel('Timestamp')
    plt.ylabel('Usage')
    plt.title('Consumption and Production Over Time')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    # Erstellen Sie eine Instanz von SDATProcessor und verarbeiten Sie die Dateien
    processor = ESLProcessor('./data/ESL-Files/')  # Pfad könnte je nach Struktur unterschiedlich sein
    processor.process_files()
    
    # Daten für das Plotting abrufen
    data_for_plotting = processor.get_data_for_plotting()

    # Daten plotten
    plot_data(data_for_plotting)
