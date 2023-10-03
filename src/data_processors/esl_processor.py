import sys
import os
import pandas as pd
from datetime import datetime
dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(dir))
from file_readers import esl_reader

class ESLProcessor:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.data = pd.DataFrame()

    def process_files(self):
        files = [f for f in os.listdir(self.folder_path) if f.endswith('.xml')]
        results = []

        for file in files:
            try:
                esl = esl_reader.ESLReader(os.path.join(self.folder_path, file))

                consumption = esl.get_usage()
                production = esl.get_production()

                dataset = (consumption[0][0], consumption[0][1], production[0][1])

                results.append(dataset) if dataset not in results else print("duplicate found", dataset)

            except:
                continue
        
        return results



if __name__ == "__main__":
    processor = ESLProcessor("./data/ESL-Files")
    thing = processor.process_files()
    for i in thing:
        print(i)