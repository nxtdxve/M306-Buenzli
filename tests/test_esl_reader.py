import pytest
from src.file_readers import ESLReader

def setup_function():
    global esl_reader
    esl_reader = ESLReader('test_esl_file.xml')

def test_get_interval():
    assert esl_reader.get_interval() == ['2019-01-01T00:00:00']

def test_get_values():
    assert esl_reader.get_values() == [('2019-01-01T00:00:00', 19216.2, 11801.2)]



