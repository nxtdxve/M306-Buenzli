import xml.etree.ElementTree as ET

class SDATReader:
    """
    A class used to read and extract information from SDAT XML files.

    Attributes
    ----------
    tree : ElementTree
        The parsed XML tree.
    root : Element
        The root element of the XML tree.

    Methods
    -------
    get_document_id():
        Returns the DocumentID from the XML file.
    get_interval():
        Returns the StartDateTime and EndDateTime from the XML file.
    get_resolution():
        Returns the Resolution and its Unit from the XML file.
    get_observations():
        Returns a list of Observations, each as a tuple containing Sequence and Volume.
    """

    def __init__(self, filename):
        """
        Constructs all the necessary attributes for the SDATReader object.

        Parameters
        ----------
        filename : str
            The name of the SDAT XML file to be read.
        """
        self.tree = ET.parse(filename)
        self.root = self.tree.getroot()

    def get_document_id(self):
        """
        Extracts and returns the DocumentID from the XML file.

        Returns
        -------
        str
            DocumentID extracted from the XML file.
        """
        return self.root.find('.//rsm:DocumentID', namespaces={'rsm': 'http://www.strom.ch'}).text

    def get_interval(self):
        """
        Extracts and returns the StartDateTime and EndDateTime from the XML file.

        Returns
        -------
        tuple
            A tuple containing the StartDateTime and EndDateTime.
        """
        start_time = self.root.find('.//rsm:StartDateTime', namespaces={'rsm': 'http://www.strom.ch'}).text
        end_time = self.root.find('.//rsm:EndDateTime', namespaces={'rsm': 'http://www.strom.ch'}).text
        return start_time, end_time

    def get_resolution(self):
        """
        Extracts and returns the Resolution and its Unit from the XML file.

        Returns
        -------
        tuple
            A tuple containing the Resolution and its Unit.
        """
        resolution = self.root.find('.//rsm:Resolution/rsm:Resolution', namespaces={'rsm': 'http://www.strom.ch'}).text
        unit = self.root.find('.//rsm:Resolution/rsm:Unit', namespaces={'rsm': 'http://www.strom.ch'}).text
        return resolution, unit

    def get_observations(self):
        """
        Extracts and returns a list of Observations from the XML file.
        Each observation is represented as a tuple containing the Sequence and Volume.

        Returns
        -------
        list
            A list of tuples, where each tuple contains Sequence and Volume of an Observation.
        """
        observations = []
        for obs in self.root.findall('.//rsm:Observation', namespaces={'rsm': 'http://www.strom.ch'}):
            sequence = obs.find('.//rsm:Sequence', namespaces={'rsm': 'http://www.strom.ch'}).text
            volume = obs.find('.//rsm:Volume', namespaces={'rsm': 'http://www.strom.ch'}).text
            observations.append((sequence, volume))
        return observations

if __name__ == '__main__':
    reader = SDATReader('././data/SDAT-Files/20190313_093127_12X-0000001216-O_E66_12X-LIPPUNEREM-T_ESLEVU121963_-279617263.xml')
    print(reader.get_document_id())
    print(reader.get_interval())
    print(reader.get_resolution())
    print(reader.get_observations())
