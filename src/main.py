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

    elif option == "ESL":
        plot_data = esl_processor.get_data_for_plotting()

    elif option == "SDAT_Import":
        new_sdat_processor = SDATProcessor(SDAT_import_location)
        new_sdat_processor.process_files()
        plot_data = new_sdat_processor.get_data_for_plotting()

    elif option == "ESL_Import":
        new_esl_processor = ESLProcessor(ESL_import_location)
        new_esl_processor.process_files()
        plot_data = new_esl_processor.get_data_for_plotting()
        
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

# set data_export_location
def set_data_export_location(location):
    global data_export_location
    data_export_location = location

# set data_export_URL
def set_data_export_URL(location):
    global data_export_URL
    data_export_URL = location

# set ESL import location
def set_ESL_import_location(location):
    global ESL_import_location
    ESL_import_location = location

# set SDAT import location
def set_SDAT_import_location(location):
    global SDAT_import_location
    SDAT_import_location = location

#create export function for CSV
def export_csv(sender, app_data):
    option = dpg.get_value(combo_id)
    if option == "SDAT":
        data = sdat_processor.get_data_for_plotting()

    elif option == "ESL":
        data = esl_processor.get_data_for_plotting()

    elif option == "SDAT_Import":
        new_sdat_processor = SDATProcessor(SDAT_import_location)
        new_sdat_processor.process_files()
        data = new_sdat_processor.get_data_for_plotting()

    elif option == "ESL_Import":
        new_esl_processor = ESLProcessor(ESL_import_location)
        new_esl_processor.process_files()
        data = new_esl_processor.get_data_for_plotting()
    
    csv_exporter = CSVExporter(data, data_export_location)
    csv_exporter.export()

# create export function for JSON
def export_json(sender, app_data):
    option = dpg.get_value(combo_id)
    if option == "SDAT":
        data = sdat_processor.get_data_for_plotting()

    elif option == "ESL":
        data = esl_processor.get_data_for_plotting()

    elif option == "SDAT_Import":
        new_sdat_processor = SDATProcessor(SDAT_import_location)
        new_sdat_processor.process_files()
        data = new_sdat_processor.get_data_for_plotting()

    elif option == "ESL_Import":
        new_esl_processor = ESLProcessor(ESL_import_location)
        new_esl_processor.process_files()
        data = new_esl_processor.get_data_for_plotting()
    
    json_exporter = JSONExporter(data, data_export_location)
    json_exporter.export()

# create export function for HTTP
def export_http(sender, app_data):
    option = dpg.get_value(combo_id)

    if option == "SDAT":
        data = sdat_processor.get_data_for_plotting()

    elif option == "ESL":
        data = esl_processor.get_data_for_plotting()

    elif option == "SDAT_Import":
        new_sdat_processor = SDATProcessor(SDAT_import_location)
        new_sdat_processor.process_files()
        data = new_sdat_processor.get_data_for_plotting()

    elif option == "ESL_Import":
        new_esl_processor = ESLProcessor(ESL_import_location)
        new_esl_processor.process_files()
        data = new_esl_processor.get_data_for_plotting()
    
    http_exporter = HTTPExporter(data, data_export_URL)
    
    try: 
        http_exporter.export()
    except:
        print("HTTP export failed")

with dpg.window(label="Energy Data Visualization") as main_window:
    # Dropdown to select between SDAT and ESL
    combo_id = dpg.add_combo(label="Choose data source", items=["SDAT", "ESL"], default_value="SDAT", callback=update_data, tag="combo_id")

    with dpg.menu_bar():
        with dpg.menu(label="Export as"):
            dpg.add_menu_item(label="CSV", tag="CSV", enabled=False, callback=export_csv)
            dpg.add_menu_item(label="JSON", tag="JSON", enabled=False, callback=export_json)
            dpg.add_menu_item(label="HTTP", tag="HTTP", enabled=False, callback=export_http)
        
        def call(sender, app_data):
            if sender == "SDAT_import":
                combo_id_items = dpg.get_item_configuration("combo_id")["items"]
                set_SDAT_import_location(app_data["file_path_name"])
                dpg.configure_item("combo_id", items=["SDAT_Import", combo_id_items[1]], default_value="SDAT", callback=update_data)

            elif sender == "ESL_import":
                combo_id_items = dpg.get_item_configuration("combo_id")["items"]
                set_ESL_import_location(app_data["file_path_name"])
                dpg.configure_item("combo_id", items=[combo_id_items[0], "ESL_Import"], default_value="SDAT", callback=update_data)

            elif sender == "Data_export":
                print("data exported: ", app_data["file_path_name"])
                dpg.enable_item("CSV")
                dpg.enable_item("JSON")
                set_data_export_location(app_data["file_path_name"])

            elif sender == "URL_export":
                dpg.enable_item("HTTP")
                set_data_export_URL(app_data)

        with dpg.menu(label="Settings"):
            dpg.add_file_dialog(directory_selector=True, show=False, tag="SDAT_import", callback=call)
            dpg.add_menu_item(label="directoy selection SDAT import", callback=lambda: dpg.show_item("SDAT_import"))

            dpg.add_file_dialog(directory_selector=True, show=False, tag="ESL_import", callback=call)
            dpg.add_menu_item(label="directoy selection ESL import", callback=lambda: dpg.show_item("ESL_import"))

            dpg.add_file_dialog(directory_selector=True, show=False, tag="Data_export", callback=call)
            dpg.add_menu_item(label="directoy selection data export", callback=lambda: dpg.show_item("Data_export"))
            
            with dpg.window(label="Delete Files", modal=True, show=False, tag="modal_id", no_title_bar=True):

                dpg.add_text("Please enter your URL for the HTTP export: ")
                dpg.add_separator()
                dpg.add_input_text(label="URL", default_value="https://api.npoint.io/bf1d2bef297f90b39861", tag="URL_export", callback=call)

                with dpg.group(horizontal=True):
                    dpg.add_button(label="OK", width=75, callback=lambda: dpg.configure_item("modal_id", show=False))
                    dpg.add_button(label="Cancel", width=75, callback=lambda: dpg.configure_item("modal_id", show=False))

            dpg.add_menu_item(label="HTTP-URL selection export", callback=lambda: dpg.configure_item("modal_id", show=True))

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
