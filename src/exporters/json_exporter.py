import os
import json
import pandas as pd

class JSONExporter:
    """
    Class to export data to a JSON file.

    Attributes:
        data (DataFrame): Pandas DataFrame containing the data to export.
        output_folder (str): The folder where the JSON file will be saved.
        sensor_id_col (str, optional): The column name in the DataFrame that contains sensor IDs.
    """
    def __init__(self, data, output_folder, sensor_id_col=None):
        """
        Initialize the JSONExporter class.

        Args:
            data (DataFrame): Pandas DataFrame containing the data to export.
            output_folder (str): The folder where the JSON file will be saved.
            sensor_id_col (str, optional): The column name in the DataFrame that contains sensor IDs.
        """
        self.data = data
        self.output_folder = output_folder
        self.sensor_id_col = sensor_id_col

    def export(self):
        """
        Export the data to a JSON file.

        If sensor_id_col is provided, data for each sensor ID will be grouped together.
        The resulting JSON file is saved to the specified output folder.
        """
        json_output = []

        if self.sensor_id_col:
            for sensor_id in ['ID742', 'ID735']:
                filtered_data = self.data[self.data[self.sensor_id_col] == sensor_id]
        else:
            filtered_data = self.data

        for col_name in ['Consumption', 'Production']:
            if col_name in filtered_data.columns:
                sensor_id = 'ID742' if col_name == 'Consumption' else 'ID735'
                values = filtered_data[col_name]
                unix_timestamps = pd.to_datetime(filtered_data.index).view('int64') // 10**9
                
                data_points = [
                    {
                        "ts": str(ts),
                        "value": val
                    }
                    for ts, val in zip(unix_timestamps, values)
                ]
                
                sensor_data = {
                    "sensorId": sensor_id,
                    "data": data_points
                }

                json_output.append(sensor_data)

        output_file_path = os.path.join(self.output_folder, "output.json")
        with open(output_file_path, 'w') as f:
            json.dump(json_output, f, indent=4)
