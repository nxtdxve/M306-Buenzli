"""
Tests mit ChatGPT generiert und danach angepasst und erweitert was nicht funktioniert hat

promt:
makes tests for each function of esl_processor.py with pytest
file: esl_processor.py
"""

import os
import pandas as pd
import pytest
from datetime import datetime
from _pytest import monkeypatch
from src.data_processors import ESLProcessor
from src.data_processors import SDATProcessor

# Mocken Sie die ESLReader-Klasse für den Test

@pytest.fixture
def processor():
    folder_path = 'test_data/esl'
    return ESLProcessor(folder_path)


def test_init(processor):
    assert processor.folder_path == 'test_data/esl'
    assert processor.data.empty
    assert processor.counter_data.empty

def test_process_files(processor):
    esl_data = processor.process_files()
    assert len(esl_data) == 3
    assert esl_data[0] == ('2019-02-01T00:00:00', 21869.2, 11803.3)

def test_print_progress_bar(capfd, processor):
    # Erfassen der gedruckten Ausgabe
    processor.print_progress_bar(50, 100, prefix='Progress:', suffix='Complete', length=20)
    captured_output = capfd.readouterr()
    # Überprüfen, ob die Ausgabe den Erwartungen entspricht
    expected_output = "\rProgress: |██████████----------| 50.0% Complete\r"
    assert captured_output.out == expected_output

def test_counter(processor):
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
    assert len(processor.counter_data) == 192


def test_get_data_from_plotting_counter(processor):
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
    assert len(processor.get_data_for_plotting_counter()) == 192
    assert processor.get_data_for_plotting_counter().index[0] == "2019-03-11T23:00:00"
    assert processor.get_data_for_plotting_counter().index[191] == "2019-03-13T22:45:00"



