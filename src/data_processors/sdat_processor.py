import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from file_readers.sdat_reader import SDATReader


class SDATProcessor:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.data = pd.DataFrame()

    def process_files(self):
        # Liste aller SDAT-Dateien im Ordner
        files = [f for f in os.listdir(self.folder_path) if f.endswith('.xml')]
        total_files = len(files)

        # Füge enumerate hinzu, um den aktuellen Datei-Index zu erhalten
        for file_index, file in enumerate(files):
            file_path = os.path.join(self.folder_path, file)

            # Verwenden Sie SDATReader, um die Daten zu lesen
            reader = SDATReader(file_path)
            document_id = reader.get_document_id()
            start_time, end_time = reader.get_interval()
            start_time = datetime.fromisoformat(start_time[:-1])
            resolution, unit = reader.get_resolution()
            resolution = int(resolution)
            observations = reader.get_observations()



            # Generieren Sie Zeitstempel und teilen Sie die Beobachtungen in Verbrauch und Produktion auf
            timestamps = []
            consumption = []
            production = []

            for i, (seq, vol) in enumerate(observations):
                current_time = start_time + timedelta(minutes=i * resolution)
                timestamps.append(current_time)

                vol = float(vol)

                if 'ID735' in document_id:
                    consumption.append(None)
                    production.append(vol)
                elif 'ID742' in document_id:
                    consumption.append(vol)
                    production.append(None)
                else:
                    continue


            # Erstellen Sie einen DataFrame für diese Datei
            df = pd.DataFrame({
                'Timestamp': timestamps,
                'Consumption': consumption,
                'Production': production
            })
            df.set_index('Timestamp', inplace=True)


            self.data = pd.concat([self.data, df])

            # Benutze file_index + 1, weil file_index bei 0 startet
            self.print_progress_bar(file_index + 1, total_files, prefix='Reading SDAT:', suffix='Complete', length=50)

    def get_data_for_plotting(self):
        return self.data

    def print_progress_bar(self, iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█',
                           print_end="\r"):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            print_end   - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)


if __name__ == '__main__':
    processor = SDATProcessor('./data/sdat_files/')
    processor.process_files()
    plot_data = processor.get_data_for_plotting()
    print(plot_data)