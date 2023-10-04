# General imports
import pandas as pd
import dearpygui.dearpygui as dpg
import datetime

# Data Processors
from data_processors.sdat_processor import SDATProcessor
from data_processors.esl_processor import ESLProcessor

# Exporters
# from exporters.csv_exporter import CSVExporter
# from exporters.json_exporter import JSONExporter
# from exporters.http_exporter import HTTPExporter

""" if __name__ == '__main__':
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
    http_exporter.export() """


def update_data(sender, app_data):
    option = dpg.get_value(sender)

    if option == "SDAT":
        plot_data = sdat_processor.get_data_for_plotting()
        dpg.set_axis_limits(y_axis, 0, 8)
    else:
        plot_data = esl_processor.get_data_for_plotting()
        # ESL zoom should show y axis from 0 to 80000
        dpg.set_axis_limits(y_axis, 0, 80000)





    timestamps = pd.to_datetime(plot_data.index).view('int64') // 10 ** 9
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
    combo_id = dpg.add_combo(label="Choose data source", items=["SDAT", "ESL"], default_value="SDAT",
                             callback=update_data, width=200)

    with dpg.plot(label="Consumption and Production", height=-1, width=-1, use_24hour_clock=True) as plot_widget:
        legend = dpg.add_plot_legend()

        # Initial data
        plot_data = sdat_processor.get_data_for_plotting()
        timestamps = pd.to_datetime(plot_data.index).view('int64') // 10 ** 9
        timestamps = timestamps.astype(float).tolist()
        consumption_data = plot_data['Consumption'].tolist()
        production_data = plot_data['Production'].tolist()

        # Add the axes
        x_axis = dpg.add_plot_axis(dpg.mvXAxis, label="Time", time=True)

        y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="Value")

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
