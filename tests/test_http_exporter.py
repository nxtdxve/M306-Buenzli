"""
Tests mit ChatGPT generiert und danach angepasst und erweitert was nicht funktioniert hat

promt:
makes tests for each function of http_exporter.py with pytest
file: http_exporter.py
"""

import pytest
from src.exporters import HTTPExporter
from src.data_processors import ESLProcessor
from src.data_processors import SDATProcessor
import pandas as pd

@pytest.fixture
def url():
    return "https://api.npoint.io/bf1d2bef297f90b39861"

def test_init(url):
    processor = ESLProcessor("test_data/esl")
    esl_data = processor.get_data_for_plotting_counter()
    http_exporter = HTTPExporter(esl_data, url)
    assert http_exporter.data is esl_data
    assert http_exporter.endpoint_url == "https://api.npoint.io/bf1d2bef297f90b39861"
    assert http_exporter.sensor_id_col is None


def test_export(url):
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

    http_exporter = HTTPExporter(esl_data, url)
    response = http_exporter.export()

    # Überprüfen Sie, ob der HTTP-Response-Statuscode 200 ist (erfolgreich)
    assert response.status_code == 200




