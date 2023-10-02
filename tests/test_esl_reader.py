import pytest
from src.file_readers import ESLReader

def setup_function():
    global esl_reader
    esl_reader = ESLReader('test_esl_file.xml')

def test_get_interval():
    assert esl_reader.get_interval() == ('2019-01-01T00:00:00', '2019-01-31T00:00:00')

def test_get_values():
    assert esl_reader.get_values() == ('4755.3000', '14460.9000', '8258.1000', '3543.1000')
