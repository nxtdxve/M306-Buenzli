from collections import defaultdict
import numpy as np
import os
import pandas as pd
from datetime import datetime, timedelta
import sys

dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(dir))

# Assume this import works as in your original code
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
            start_time = datetime.fromisoformat(start_time[:-1])
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

        # Aggregating data by Timestamp
        aggregated_data = defaultdict(lambda: {'Consumption': [], 'Production': []})
        for data_dict in self.data_list:
            timestamp = data_dict['Timestamp']
            aggregated_data[timestamp]['Consumption'].append(data_dict['Consumption'])
            aggregated_data[timestamp]['Production'].append(data_dict['Production'])

        # Processing the aggregated data
        processed_data_list = []
        for timestamp, data in aggregated_data.items():
            consumption_values = [x for x in data['Consumption'] if x is not None]
            production_values = [x for x in data['Production'] if x is not None]

            processed_data_dict = {
                'Timestamp': timestamp,
                'Consumption': self.process_value_list(consumption_values),
                'Production': self.process_value_list(production_values)
            }
            processed_data_list.append(processed_data_dict)

        self.data = pd.DataFrame(processed_data_list)
        self.data.set_index('Timestamp', inplace=True)
        self.data.sort_index(inplace=True)

    def get_data_for_plotting(self):
        return self.data

    def process_value_list(self, values):
        if not values:
            return 0
        non_zero_values = [x for x in values if x != 0]
        if not non_zero_values:
            return 0
        return np.mean(non_zero_values)  # Take average of all non-zero numbers

    def print_progress_bar(self, iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█',
                           print_end="\r"):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)


if __name__ == '__main__':
    processor = SDATProcessor('../data/SDAT-Files')
    processor.process_files()
    plot_data = processor.get_data_for_plotting()
    print(plot_data)
