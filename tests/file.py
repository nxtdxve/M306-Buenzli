import os
from src.exporters import HTTPExporter
from src.data_processors import ESLProcessor
from src.data_processors import SDATProcessor
import pandas as pd

if __name__ == '__main__':
    processor = ESLProcessor('test_data/esl')
    sdat_processor = SDATProcessor("test_data/sdat")
    sdat_processor.process_files()
    sdat_list_list = sdat_processor.get_data_for_plotting().reset_index().values.tolist()
    formatted_tuple_list = []

    for i in sdat_list_list:
        timestamp = pd.Timestamp(i[0])
        formatted_time = timestamp.strftime('%Y-%m-%dT%H:%M:%S')
        formatted_tuple = (formatted_time, i[1], i[2])
        formatted_tuple_list.append(formatted_tuple)

    processor.counter(processor.process_files(), formatted_tuple_list)
    print(processor.get_data_for_plotting_counter().index[0])
    print(processor.get_data_for_plotting_counter().iloc[0][0])
    print(processor.get_data_for_plotting_counter().iloc[0][1])
    print(processor.get_data_for_plotting_counter().index[191])
    print(processor.get_data_for_plotting_counter().iloc[191][0])
    print(processor.get_data_for_plotting_counter().iloc[191][1])


