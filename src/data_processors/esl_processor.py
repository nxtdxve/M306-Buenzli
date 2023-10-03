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
                
            df = pd.DataFrame({
                'Timestamp': timestamp,
                'Consumption': consumption,
                'Production': production
            })
            df.set_index('Timestamp', inplace=True)
            
            self.data = pd.concat([self.data, df])
        
        return results
    
    def get_data_for_plotting(self):
        return self.data



if __name__ == "__main__":
    processor = ESLProcessor("./data/ESL-Files")
    thing = processor.process_files()
    for i in thing:
        print(i)
    
    print(processor.get_data_for_plotting())