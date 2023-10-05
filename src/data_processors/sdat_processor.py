import os
import pandas as pd
from datetime import datetime, timedelta
import sys
dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(dir))
from file_readers.sdat_reader import SDATReader

class SDATProcessor:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.data_list = []

    def process_files(self):
        files = [f for f in os.listdir(self.folder_path) if f.endswith('.xml')]
        total_files = len(files)

        for file_index, file in enumerate(files):
            file_path = os.path.join(self.folder_path, file)
            
            reader = SDATReader(file_path)
            document_id = reader.get_document_id()
            start_time, end_time = reader.get_interval()
            start_time = datetime.fromisoformat(start_time)
            resolution, unit = reader.get_resolution()
            resolution = int(resolution)
            observations = reader.get_observations()

            for i, (seq, vol) in enumerate(observations):
                current_time = start_time + timedelta(minutes=i * resolution)
                vol = float(vol)

                data_dict = {
                    'Timestamp': current_time,
                    'Consumption': None,
                    'Production': None
                }

                if 'ID735' in document_id:
                    data_dict['Production'] = vol
                elif 'ID742' in document_id:
                    data_dict['Consumption'] = vol
                else:
                    continue
                
                self.data_list.append(data_dict)

            self.print_progress_bar(file_index + 1, total_files, prefix='Reading SDAT:', suffix='Complete', length=50)
        
        # Erstellen Sie den DataFrame nachdem alle Dateien verarbeitet wurden
        self.data = pd.DataFrame(self.data_list)
        self.data.set_index('Timestamp', inplace=True)

    def get_data_for_plotting(self):
        # Konvertieren Sie die Datenliste direkt hier in einen DataFrame
        plot_data = pd.DataFrame(self.data_list)
        plot_data.set_index('Timestamp', inplace=True)
        return plot_data

    def print_progress_bar(self, iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', print_end="\r"):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)

if __name__ == '__main__':
    processor = SDATProcessor('./data/SDAT-Files')
    processor.process_files()
    plot_data = processor.get_data_for_plotting()
    print(plot_data)
    plot_data.to_csv('./output/debug/final_output.csv')
