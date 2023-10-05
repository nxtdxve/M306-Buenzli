"""
Tests mit ChatGPT generiert und danach angepasst und erweitert was nicht funktioniert hat

promt:
makes tests for each function of sdat_processor.py with pytest
file: sdat_processor.py
"""

import pandas as pd
import pytest
import sys
import io
from src.data_processors import SDATProcessor  # Stellen Sie sicher, dass Sie Ihren Modulnamen hier verwenden


@pytest.fixture
def processor():
    folder_path = 'test_data/sdat'  # Ersetzen Sie dies durch den entsprechenden Pfad
    return SDATProcessor(folder_path)


def test_init(processor):
    assert processor.folder_path == 'test_data/sdat'
    assert processor.data_list == []


def test_process_files(processor):
    # Sie können diesen Test implementieren, indem Sie Mock-Daten oder -Dateien bereitstellen
    processor.process_files()
    assert len(processor.data_list) == 384


def test_get_data_for_plotting(processor):
    processor.process_files()
    plot_data = processor.get_data_for_plotting()
    assert isinstance(plot_data, pd.DataFrame)
    # Fügen Sie bei Bedarf spezifischere Aussagen zum DataFrame hinzu


def test_process_value_list(processor):
    processor.process_files()
    sdat_list_list = processor.get_data_for_plotting().reset_index().values.tolist()
    values = []
    for i in sdat_list_list:
        values.append(i[1])
    print(values)
    result = processor.process_value_list(values)
    print(result)
    assert result == 1.8416666666666666


def test_print_progress_bar(capfd, processor):
    # Erfassen der gedruckten Ausgabe
    sys.stdout = io.StringIO()

    # Ersetzen Sie 'YourClass' durch den Namen Ihrer Klasse
    processor.print_progress_bar(50, 100, prefix='Progress:', suffix='Complete', length=20)

    captured_output = sys.stdout.getvalue()
    sys.stdout.close()
    sys.stdout = sys.__stdout__  # Stellen Sie sys.stdout wieder her

    # Überprüfen, ob die Ausgabe den Erwartungen entspricht
    expected_output = "\rProgress: |██████████----------| 50.0% Complete\r"
    assert captured_output == expected_output
