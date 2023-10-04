import sys
import os
import pandas as pd
from datetime import datetime
dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(dir))
from file_readers import esl_reader

class ESLProcessor:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.data = pd.DataFrame()

    def process_files(self):
        files = [f for f in os.listdir(self.folder_path) if f.endswith('.xml')]
        results = []
        total_files = len(files)  # Gesamtanzahl der Dateien

        for file_index, file in enumerate(files):
            timestamp = []
            consumption = []
            production = []

            try:
                esl = esl_reader.ESLReader(os.path.join(self.folder_path, file))
                dataset = esl.get_values()

                for i in dataset:
                    if i not in results:
                        timestamp.append(i[0])
                        consumption.append(i[1])
                        production.append(i[2])
                        results.append(i)

            except:
                continue
                
            df = pd.DataFrame({
                'Timestamp': timestamp,
                'Consumption': consumption,
                'Production': production
            })
            df.set_index('Timestamp', inplace=True)
            
            self.data = pd.concat([self.data, df])

            # Fortschrittsbalken aktualisieren
            self.print_progress_bar(file_index + 1, total_files, prefix='Reading ESL:', suffix='Complete', length=50)

        return results
    
    def get_data_for_plotting(self):
        return self.data

    def print_progress_bar(self, iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', print_end="\r"):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)


if __name__ == "__main__":
    processor = ESLProcessor("./data/ESL-Files")
    thing = processor.process_files()
    for i in thing:
        print(i)
    
    print(processor.get_data_for_plotting())
