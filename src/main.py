# Data Processors
from data_processors.sdat_processor import SDATProcessor
from data_processors.esl_processor import ESLProcessor

# Visualizers
from visualizers.consumption_visualizer import ConsumptionVisualizer
from visualizers.meter_visualizer import MeterVisualizer

# Exporters
from exporters.csv_exporter import CSVExporter
from exporters.json_exporter import JSONExporter
from exporters.http_exporter import HTTPExporter

if __name__ == '__main__':
    # Processing ESL files
    esl_processor = ESLProcessor('./data/ESL-Files/')
    esl_processor.process_files()
    esl_data = esl_processor.get_data_for_plotting()

    # Exporting ESL data to CSV
    esl_csv_exporter = CSVExporter(esl_data, "./output/csv/")
    esl_csv_exporter.export()

    # Exporting ESL data to JSON
    esl_json_exporter = JSONExporter(esl_data, "./output/json/")
    esl_json_exporter.export()

    # Exporting ESL data to an HTTP server
    http_exporter = HTTPExporter(esl_data, "https://api.npoint.io/bf1d2bef297f90b39861")
    http_exporter.export()