import os
import pandas as pd
from datetime import datetime, timedelta
from file_readers.sdat_reader import SDATReader

class SDATProcessor:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.data = pd.DataFrame()

    def process_files(self):
        # Liste aller SDAT-Dateien im Ordner
        files = [f for f in os.listdir(self.folder_path) if f.endswith('.xml')]
        
        for file in files:
            file_path = os.path.join(self.folder_path, file)
            
            # Verwenden Sie SDATReader, um die Daten zu lesen
            reader = SDATReader(file_path)
            document_id = reader.get_document_id()
            start_time, end_time = reader.get_interval()
            start_time = datetime.fromisoformat(start_time)  # Konvertieren Sie das Startdatum in ein datetime-Objekt
            resolution, unit = reader.get_resolution()
            resolution = int(resolution)  # Annahme: Auflösung ist in Minuten
            observations = reader.get_observations()
            
            # Generieren Sie Zeitstempel und teilen Sie die Beobachtungen in Verbrauch und Produktion auf
            timestamps = []
            consumption = []
            production = []
            
            for i, (seq, vol) in enumerate(observations):
                current_time = start_time + timedelta(minutes=i * resolution)
                timestamps.append(current_time)
                
                vol = float(vol)  # Annahme: Volumen ist eine Gleitkommazahl
                
                if 'ID735' in document_id:
                    consumption.append(0)
                    production.append(vol)
                elif 'ID742' in document_id:
                    consumption.append(vol)
                    production.append(0)
                else:
                    # Unbekannte ID, Sie können hier einen Fehler auslösen oder die Daten überspringen
                    continue
            
            # Erstellen Sie einen DataFrame für diese Datei
            df = pd.DataFrame({
                'Timestamp': timestamps,
                'Consumption': consumption,
                'Production': production
            })
            df.set_index('Timestamp', inplace=True)
            
            self.data = pd.concat([self.data, df])

    def get_data_for_plotting(self):
        return self.data

if __name__ == '__main__':
    processor = SDATProcessor('./data/sdat_files/')
    processor.process_files()
    plot_data = processor.get_data_for_plotting()
    print(plot_data)
