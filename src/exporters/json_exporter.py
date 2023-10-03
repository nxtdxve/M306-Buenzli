import os
import json
import pandas as pd

class JSONExporter:
    def __init__(self, data, output_folder, sensor_id_col=None):
        self.data = data
        self.output_folder = output_folder
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

        output_file_path = os.path.join(self.output_folder, "output.json")
        with open(output_file_path, 'w') as f:
            json.dump(json_output, f, indent=4)
