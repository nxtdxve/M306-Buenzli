import xml.etree.ElementTree as ET


class ESLReader:
    """
    Class to read ESL (Energy System Language) files.

    Attributes:
        tree (ElementTree): The parsed XML tree.
        root (Element): The root of the XML tree.
    """
    
    def __init__(self, filename):
        """
        Initialize the ESLReader class.

        Args:
            filename (str): The path of the ESL file to read.
        """
        self.tree = ET.parse(filename)
        self.root = self.tree.getroot()
    
    def get_interval(self):
        """
        Get the time interval of the ESL data.

        Returns:
            str: The start and end time of the data in the ESL file.
        """
        startTime = self.root.find('.//TimePeriod').attrib['end']
        endTime = self.root.find('.//Header').attrib['created']
        return startTime, endTime
    
    def get_values(self):
        """
        Get specific values from the ESL file based on OBIS codes.

        Returns:
            tuple: A tuple containing four values corresponding to OBIS codes 1-1:1.8.1,
            1-1:1.8.2, 1-1:2.8.1 and 1-1:2.8.2.
        """
        values = []
        bunch = self.root.find('.//TimePeriod')
        for child in bunch:
            if child.attrib["obis"] == "1-1:1.8.1":
                values.append(child.attrib["value"])
            elif child.attrib["obis"] == "1-1:1.8.2":
                values.append(child.attrib["value"])
            elif child.attrib["obis"] == "1-1:2.8.1":
                values.append(child.attrib["value"])
            elif child.attrib["obis"] == "1-1:2.8.2":
                values.append(child.attrib["value"])
        
        return values[0], values[1], values[2], values[3]


if __name__ == "__main__":
    esl = ESLReader('././data/ESL-Files/EdmRegisterWertExport_20190131_eslevu_20190322160349.xml')
    print("-----------------------")
    print(esl.get_interval())
    print("-----------------------")
    print(esl.get_values())
    print("-----------------------")
