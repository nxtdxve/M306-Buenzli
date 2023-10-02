import sys
import os
dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(dir))
from file_readers import esl_reader

class ESLProcessor:
    for esl_file in os.listdir("././data/ESL-Files"):
        try: 
            if esl_file.endswith(".xml"):
                esl = esl_reader.ESLReader("././data/ESL-Files/" + esl_file)
                print(esl.get_interval(), esl.get_values())
        except:
            continue
        

if __name__ == "__main__":
    processor = ESLProcessor()
    