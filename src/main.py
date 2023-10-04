# General imports
import pandas as pd
import dearpygui.dearpygui as dpg

# Data Processors
from data_processors.sdat_processor import SDATProcessor
from data_processors.esl_processor import ESLProcessor

# Exporters
from exporters.csv_exporter import CSVExporter
from exporters.json_exporter import JSONExporter
from exporters.http_exporter import HTTPExporter

""" 
if __name__ == '__main__':
    # Processing ESL files
    esl_processor = ESLProcessor('./data/ESL-Files/')
    esl_processor.process_files()
    esl_data = esl_processor.get_data_for_plotting()

    # Exporting ESL data to CSV
    esl_csv_exporter = CSVExporter(esl_data, "./output/csv/")
    esl_csv_exporter.export()

    # Exporting ESL data to JSON
    esl_json_exporter = JSONExporter(esl_data, "./output/json/")
    esl_json_exporter.export()

    # Exporting ESL data to an HTTP server
    http_exporter = HTTPExporter(esl_data, "https://api.npoint.io/bf1d2bef297f90b39861")
    http_exporter.export() 
"""

def update_data(sender, app_data):
    option = dpg.get_value(sender)
    
    if option == "SDAT":
        plot_data = sdat_processor.get_data_for_plotting()
    else:
        plot_data = esl_processor.get_data_for_plotting()
        
    timestamps = pd.to_datetime(plot_data.index).view('int64') // 10**9
    timestamps = timestamps.astype(float).tolist()
    consumption_data = plot_data['Consumption'].tolist()
    production_data = plot_data['Production'].tolist()

    dpg.set_value(consumption_line, (timestamps, consumption_data))
    dpg.set_value(production_line, (timestamps, production_data))

# Prepare the SDAT data
sdat_processor = SDATProcessor('./data/SDAT-Files/')
sdat_processor.process_files()

# Prepare the ESL data
esl_processor = ESLProcessor('./data/ESL-Files/')
esl_processor.process_files()

# Create a Dear PyGui context
dpg.create_context()

with dpg.window(label="Energy Data Visualization") as main_window:
    # Dropdown to select between SDAT and ESL
    combo_id = dpg.add_combo(label="Choose data source", items=["SDAT", "ESL"], default_value="SDAT", callback=update_data)

    with dpg.menu_bar():

        with dpg.menu(label="Export as"):
            dpg.add_menu_item(label="CSV", enabled=False)
            dpg.add_menu_item(label="JSON", enabled=False)
            dpg.add_menu_item(label="HTTP", enabled=False)
        
        def call(sender, app_data):
            if sender == "SDAT_import":
                print("SDAT imported: ", app_data["file_path_name"])
            elif sender == "ESL_import":
                print("ESL imported: ", app_data["file_path_name"])
            elif sender == "SDAT_export":
                print("SDAT exported: ", app_data["file_path_name"])
            elif sender == "ESL_export":
                print("ESL exported: ", app_data["file_path_name"])

        with dpg.menu(label="Settings"):
            dpg.add_file_dialog(directory_selector=True, show=False, tag="SDAT_import", callback=call)
            dpg.add_menu_item(label="directoy selection SDAT import", callback=lambda: dpg.show_item("SDAT_import"))
            dpg.add_file_dialog(directory_selector=True, show=False, tag="ESL_import", callback=call)
            dpg.add_menu_item(label="directoy selection ESL import", callback=lambda: dpg.show_item("ESL_import"))
            dpg.add_file_dialog(directory_selector=True, show=False, tag="SDAT_export", callback=call)
            dpg.add_menu_item(label="directoy selection SDAT export", callback=lambda: dpg.show_item("SDAT_export"))
            dpg.add_file_dialog(directory_selector=True, show=False, tag="ESL_export", callback=call)
            dpg.add_menu_item(label="directoy selection ESL export", callback=lambda: dpg.show_item("ESL_export"))

        """
        with dpg.menu(label="Graph selection"):
            dpg.add_menu_item(label="SDAT", check=True)
            dpg.add_menu_item(label="ESL")
        """
    
    with dpg.plot(label="Consumption and Production", height=400, width=-1):
        dpg.add_plot_legend()
        dpg.add_plot_axis(dpg.mvXAxis, label="Time")
        y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="Value")
        
        # Initial data
        plot_data = sdat_processor.get_data_for_plotting()
        timestamps = pd.to_datetime(plot_data.index).view('int64') // 10**9
        timestamps = timestamps.astype(float).tolist()
        consumption_data = plot_data['Consumption'].tolist()
        production_data = plot_data['Production'].tolist()
        
        # Adding the consumption line
        consumption_line = dpg.add_line_series(timestamps, consumption_data, label="Consumption", parent=y_axis)
        
        # Adding the production line
        production_line = dpg.add_line_series(timestamps, production_data, label="Production", parent=y_axis)

# Initialize the data
update_data(combo_id, None)

dpg.create_viewport(title='Energy Data Visualization', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window(main_window, True)
dpg.start_dearpygui()
dpg.destroy_context()
