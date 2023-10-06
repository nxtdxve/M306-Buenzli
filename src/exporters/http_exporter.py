import requests
import pandas as pd
import json

class HTTPExporter:
    """
    Class to export data via HTTP POST requests.

    Attributes:
        data (DataFrame): Pandas DataFrame containing the data to export.
        endpoint_url (str): The endpoint URL where the HTTP POST request will be sent.
        sensor_id_col (str, optional): The column name in the DataFrame that contains sensor IDs.
    """
    def __init__(self, data, endpoint_url, sensor_id_col=None):
        """
        Initialize the HTTPExporter class.

        Args:
            data (DataFrame): Pandas DataFrame containing the data to export.
            endpoint_url (str): The endpoint URL where the HTTP POST request will be sent.
            sensor_id_col (str, optional): The column name in the DataFrame that contains sensor IDs.
        """
        self.data = data
        self.endpoint_url = endpoint_url
        self.sensor_id_col = sensor_id_col

    def export(self):
        """
        Export the data via HTTP POST requests.

        If sensor_id_col is provided, data for each sensor ID will be grouped together.
        The data is sent to the specified endpoint URL.

        Returns:
            response: HTTP Response object
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

        # Send HTTP POST request
        response = requests.post(self.endpoint_url, json=json_output)

        if response.status_code == 200:
            print("Successfully posted data.")
        else:
            print(f"Failed to post data. Status code: {response.status_code}, Reason: {response.text}")

        return response 
    