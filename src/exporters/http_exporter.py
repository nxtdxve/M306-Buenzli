import requests
import pandas as pd
import json

class HTTPExporter:
    def __init__(self, data, endpoint_url, sensor_id_col=None):
        self.data = data
        self.endpoint_url = endpoint_url
        self.sensor_id_col = sensor_id_col

    def export(self):
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
