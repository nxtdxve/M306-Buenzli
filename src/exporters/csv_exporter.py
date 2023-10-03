import os
import pandas as pd

class CSVExporter:
    def __init__(self, data, output_folder, sensor_id_col=None):
        self.data = data
        self.output_folder = output_folder
        self.sensor_id_col = sensor_id_col

    def export(self):
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

                export_data = pd.DataFrame({
                    'Timestamp': unix_timestamps,
                    'Value': values
                })

                output_file_path = os.path.join(self.output_folder, f"{sensor_id}.csv")
                export_data.to_csv(output_file_path, index=False)
