"""
Tests mit ChatGPT generiert und danach angepasst und erweitert was nicht funktioniert hat

promt:
makes tests for each function of json_exporter.py with pytest
file: json_exporter.py
"""

import pytest
import os
from src.exporters import JSONExporter
from src.data_processors import ESLProcessor
from src.data_processors import SDATProcessor
import pandas as pd

@pytest.fixture
def folder_path():
    return "exported_files/json"

def test_init(folder_path):
    processor = ESLProcessor("test_data/esl")
    esl_data = processor.get_data_for_plotting_counter()
    json_exporter = JSONExporter(esl_data, folder_path)
    assert json_exporter.data is esl_data
    assert json_exporter.output_folder == "exported_files/json"
    assert json_exporter.sensor_id_col is None

def test_export(folder_path):


    if os.path.exists(folder_path):
        # Eine Schleife durch alle Dateien im Ordner durchführen und sie löschen
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)


    processor = ESLProcessor("test_data/esl")
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
    esl_data = processor.get_data_for_plotting_counter()


    json_exporter = JSONExporter(esl_data, folder_path)
    json_exporter.export()
    assert os.path.exists("exported_files/json/output.json")
