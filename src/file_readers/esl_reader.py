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
        data = self.root.findall('.//TimePeriod')

        start_times = []

        for item in data:
            start_times.append(item.attrib["end"])

        return start_times[::-1]
    
    def get_values(self):
        """
        Get specific values from the ESL file based on OBIS codes.

        Returns:
            tuple: A tuple containing four values corresponding to OBIS codes 1-1:1.8.1,
            1-1:1.8.2, 1-1:2.8.1 and 1-1:2.8.2.
        """
        values = []
        dates = []
        bunch = self.root.findall('.//TimePeriod')

        for item in bunch:
            dates.append(item.attrib["end"])
            for child in item:
                if child.attrib["obis"] == "1-1:1.8.1":
                    values.append(child.attrib["value"])
                elif child.attrib["obis"] == "1-1:1.8.2":
                    values.append(child.attrib["value"])
                elif child.attrib["obis"] == "1-1:2.8.1":
                    values.append(child.attrib["value"])
                elif child.attrib["obis"] == "1-1:2.8.2":
                    values.append(child.attrib["value"])
        
        return values
    
    def get_usage(self):
        """
        Get total electricity usage from the ESL file.

        Returns:
            tuple: A tuple containing four values corresponding to OBIS codes 1-1:1.8.1,
            1-1:1.8.2, 1-1:2.8.1 and 1-1:2.8.2.
        """
        bunch = self.root.findall('.//TimePeriod')
        bunch = bunch[::-1]
        usage = []

        for item in bunch:
            subtotal = 0
            for child in item:
                if child.attrib["obis"] == "1-1:1.8.1":
                    subtotal += float(child.attrib["value"])
                elif child.attrib["obis"] == "1-1:1.8.2":
                    subtotal += float(child.attrib["value"])
            
            usage.append((item.attrib["end"], round(subtotal, 4))) if subtotal > 0 else None
        
        return usage

    def get_production(self):
        """
        Get total electricity production from the ESL file.

        Returns:
            tuple: A tuple containing four values corresponding to OBIS codes 1-1:1.8.1,
            1-1:1.8.2, 1-1:2.8.1 and 1-1:2.8.2.
        """
        bunch = self.root.findall('.//TimePeriod')
        bunch = bunch[::-1]
        prod = []

        for item in bunch:
            subtotal = 0
            for child in item:
                if child.attrib["obis"] == "1-1:2.8.1":
                    subtotal += float(child.attrib["value"])
                elif child.attrib["obis"] == "1-1:2.8.2":
                    subtotal += float(child.attrib["value"])
            
            prod.append((item.attrib["end"], round(subtotal, 4))) if subtotal > 0 else None
        
        return prod
    
    def get_values(self):
        used = self.get_usage()
        produced = self.get_production()
        result = []

        for i in used:
            for j in produced:
                if i[0] == j[0]:
                    result.append((i[0], i[1], j[1]))
        return result



if __name__ == "__main__":
    esl = ESLReader('././data\ESL-Files\EdmRegisterWertExport_20201003_eslevu_20201003051024.xml')

    print(esl.get_usage())
    print(esl.get_production())
    print(esl.get_values())