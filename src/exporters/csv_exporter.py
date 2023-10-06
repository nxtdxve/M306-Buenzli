import os
import pandas as pd

class CSVExporter:
    """
    Class to export data to CSV files.
    
    Attributes:
        data (DataFrame): Pandas DataFrame containing the data to export.
        output_folder (str): The path to the folder where the CSV files will be saved.
        sensor_id_col (str, optional): The column name in the DataFrame that contains the sensor IDs.
    """
    def __init__(self, data, output_folder, sensor_id_col=None):
        """
        Initialize the CSVExporter class.

        Args:
            data (DataFrame): Pandas DataFrame containing the data to export.
            output_folder (str): The path to the folder where the CSV files will be saved.
            sensor_id_col (str, optional): The column name in the DataFrame that contains the sensor IDs.
        """
        self.data = data
        self.output_folder = output_folder
        self.sensor_id_col = sensor_id_col

    def export(self):
        """
        Export the data to CSV files. 
        
        If sensor_id_col is provided, separate CSV files will be generated for each sensor ID.
        The files are saved in the specified output folder.
        """
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
