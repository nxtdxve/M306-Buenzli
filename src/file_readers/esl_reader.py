import xml.etree.ElementTree as ET


class ESLReader:
    """ """
    def __init__(self, filename):
        self.tree = ET.parse(filename)
        self.root = self.tree.getroot()

    def get_interval(self):
        """ """
        startTime = self.root.find(".//TimePeriod").attrib["end"]
        endTime = self.root.find(".//Header").attrib["created"]
        return f"Starting Time:\n{startTime}\nEnd Time:\n{endTime}"

    def get_values(self):
        """ """
        values = []
        bunch = self.root.find(".//TimePeriod")
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
    esl = ESLReader(
        "data\ESL-Files\EdmRegisterWertExport_20190131_eslevu_20190322160349.xml"
    )
    print("-----------------------")
    print(esl.get_interval())
    print("-----------------------")
    print(esl.get_values())
    print("-----------------------")
