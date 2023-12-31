import sys
import os
import pandas as pd
import math
from datetime import datetime

dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(dir))
from file_readers import esl_reader


class ESLProcessor:
    """
    Class to process ESL (Energy System Language) files.

    Attributes:
        folder_path (str): The path to the folder containing the ESL files.
        data (DataFrame): Pandas DataFrame to store processed data.
        counter_data (DataFrame): Pandas DataFrame to store processed counter data.
    """

    def __init__(self, folder_path):
        """
        Initialize the ESLProcessor class.

        Args:
            folder_path (str): The path to the folder containing the ESL files.
        """
        self.folder_path = folder_path
        self.data = pd.DataFrame()
        self.counter_data = pd.DataFrame()

    def process_files(self):
        """
        Process all ESL files in the specified folder.

        Returns:
            list: A list of tuples containing timestamp, consumption, and production data.
        """
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

            # Fortschrittsbalken aktualisieren
            self.print_progress_bar(file_index + 1, total_files, prefix='Reading ESL:', suffix='Complete', length=50)

        return results

    def get_data_for_plotting(self):
        """
        Retrieve processed data suitable for plotting.

        Returns:
            DataFrame: A Pandas DataFrame containing processed data.
        """
        return self.data

    def print_progress_bar(self, iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█',
                           print_end="\r"):
        """
        Display a progress bar in the console.

        Args:
            iteration (int): Current iteration number.
            total (int): Total number of iterations.
            prefix (str): Prefix string to be displayed before the progress bar.
            suffix (str): Suffix string to be displayed after the progress bar.
            decimals (int): Number of decimal places to show the percentage to.
            length (int): Length of the progress bar.
            fill (str): Character to fill the progress bar with.
            print_end (str): End character to print at the end of the progress bar.
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)

    def counter(self, esl, sdat):
        """
        Counter function to combine data from both ESL and SDAT files.

        Args:
            esl (list): A list of tuples from ESL files.
            sdat (list): A list of tuples from SDAT files.
        """
        time_list = []
        consumption_list = []
        production_list = []
        reversed_2018_consumption = []
        reversed_2018_production = []
        min_time = esl[0][0]
        min_consumption = esl[0][1]
        min_production = esl[0][2]


        for i in esl:
            initial_time = i[0]
            initial_consumption = i[1]
            initial_production = i[2]
            for j in sdat:
                if initial_time[:7] == j[0][:7]:
                    if not math.isnan(j[1]):
                        initial_consumption += j[1]
                    if not math.isnan(j[2]):
                        initial_production += j[2]
                        time_list.append(j[0])
                        consumption_list.append(initial_consumption)
                        production_list.append(initial_production)


        df = pd.DataFrame({
            'Timestamp': time_list,
            'Consumption': consumption_list,
            'Production': production_list
        })
        df.set_index('Timestamp', inplace=True)

        self.counter_data = pd.concat([self.counter_data, df])
        self.counter_data.sort_index(inplace=True)


    def get_data_for_plotting_counter(self):
        """
        Retrieve processed counter data suitable for plotting.

        Returns:
            DataFrame: A Pandas DataFrame containing processed counter data.
        """
        return self.counter_data


if __name__ == "__main__":
    processor = ESLProcessor("./data/ESL-Files")
    thing = processor.process_files()
    for i in thing:
        print(i)

    print(processor.get_data_for_plotting())