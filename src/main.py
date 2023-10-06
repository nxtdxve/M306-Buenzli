# General imports
import pandas as pd
import json
import os
import dearpygui.dearpygui as dpg
from dearpygui_ext.themes import create_theme_imgui_light, create_theme_imgui_dark

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

definitions = [
    ["Export as", "Settings", "Choose data source", "Usage data", "Counter data", "Consumption", "Production", "Time", "directory selection SDAT import", "directory selection ESL import", "Consumption and Production", "Energy Data Visualization", "Light Mode", "Hint: Restart the application to apply changes."],
    ["Exportieren als", "Einstellungen", "Datenquelle auswählen", "Verbrauchsdaten", "Stromzählerdaten", "Verbrauch", "Produktion", "Zeit", "Verzeichnis für Verbrauchsdaten auswählen", "Verzeichnis für Stromzähler auswählen", "Verbrauch und Produktion", "Energiedaten Visualisierung", "Heller Modus", "Hinweis: Starten Sie die Anwendung neu, um die Änderungen zu übernehmen."],
    ["Exporter comme", "Paramètres", "Source de données", "Données de consommation", "Données de compteur", "Consommation", "Production", "Temps", "Répertoire pour les données de consommation", "Répertoire pour les données de compteur", "Consommation et production", "Visualisation des données énergétiques", "Mode clair", "Astuce: Redémarrez l'application pour appliquer les modifications."],
    ["Exportar como", "Configuración", "Fuente de datos", "Datos de consumo", "Datos del contador", "Consumo", "Producción", "Tiempo", "Directorio para los datos de consumo", "Directorio para los datos del contador", "Consumo y producción", "Visualización de datos energéticos", "Modo claro", "Consejo: Reinicie la aplicación para aplicar los cambios."]
]

english = definitions[0]
german = definitions[1]
french = definitions[2]
spanish = definitions[3]

if os.path.isfile("./src/settings.json") == False:
    with open("./src/settings.json", "w", encoding="utf-8") as settings_file:
        settings_list = {
            "language": "English",
            "theme": "Light",
            "ESL_import_location": "./data/ESL-Files/",
            "SDAT_import_location": "./data/SDAT-Files/"
        }
        json.dump(settings_list, settings_file, indent=4)

with open("./src/settings.json", "r", encoding="utf-8") as settings_file:
    settings_list = json.load(settings_file)
    global current_language
if settings_list["language"] == "English":
    current_language = english
elif settings_list["language"] == "German":
    current_language = german
elif settings_list["language"] == "French":
    current_language = french
elif settings_list["language"] == "Spanish":
    current_language = spanish

def set_language(language):
    global current_language
    if language == "English":
        current_language = english
    elif language == "German":
        current_language = german
    elif language == "French":
        current_language = french
    elif language == "Spanish":
        current_language = spanish
    with open("./src/settings.json", "r", encoding="utf-8") as settings_file:
        settings_list = json.load(settings_file)
    settings_list["language"] = language
    with open("./src/settings.json", "w", encoding="utf-8") as settings_file:
        json.dump(settings_list, settings_file, indent=4)

def update_data(sender, app_data):
    option = dpg.get_value(sender)
    
    if option == "SDAT":
        plot_data = sdat_processor.get_data_for_plotting()
        dpg.fit_axis_data(y_axis)
        get_data_min_max(plot_data)

    elif option == "ESL":
        plot_data = esl_processor.get_data_for_plotting_counter()
        dpg.fit_axis_data(y_axis)
        get_data_min_max(plot_data)

    elif option == current_language[3]:
        plot_data = sdat_processor.get_data_for_plotting()
        dpg.fit_axis_data(y_axis)
        get_data_min_max(plot_data)

    elif option == current_language[4]:
        plot_data = esl_processor.get_data_for_plotting_counter()
        dpg.fit_axis_data(y_axis)
        get_data_min_max(plot_data)
        
    timestamps = pd.to_datetime(plot_data.index).view('int64') // 10**9
    timestamps = timestamps.astype(float).tolist()
    consumption_data = plot_data['Consumption'].tolist()
    production_data = plot_data['Production'].tolist()

    dpg.set_value(consumption_line, (timestamps, consumption_data))
    dpg.set_value(production_line, (timestamps, production_data))

    dpg.fit_axis_data(y_axis)

def get_data_min_max(plot_data):
    consumption_data = plot_data['Consumption'].tolist()
    consumption_max = max(consumption_data)
    consumption_min = min(consumption_data)
    production_data = plot_data['Production'].tolist()
    production_max = max(production_data)
    production_min = min(production_data)
    data_max = max(consumption_max, production_max)
    data_min = min(consumption_min, production_min)
    dpg.set_axis_limits(y_axis, data_min, data_max)

def toggle_theme(sender, app_data):
    is_light_mode = dpg.get_value(sender)
    if is_light_mode:
        dpg.bind_theme(light_theme)
        with open("./src/settings.json", "r", encoding="utf-8") as settings_file:
            settings_list = json.load(settings_file)
        settings_list["theme"] = "Light"
        with open("./src/settings.json", "w", encoding="utf-8") as settings_file:
            json.dump(settings_list, settings_file, indent=4)
    else:
        dpg.bind_theme(dark_theme)
        with open("./src/settings.json", "r", encoding="utf-8") as settings_file:
            settings_list = json.load(settings_file)
        settings_list["theme"] = "Dark"
        with open("./src/settings.json", "w", encoding="utf-8") as settings_file:
            json.dump(settings_list, settings_file, indent=4)

# set ESL import location
def set_ESL_import_location(location):
    global ESL_import_location
    ESL_import_location = location
    with open("./src/settings.json", "r", encoding="utf-8") as settings_file:
        settings_list = json.load(settings_file)
    settings_list["ESL_import_location"] = location
    with open("./src/settings.json", "w", encoding="utf-8") as settings_file:
        json.dump(settings_list, settings_file, indent=4)

# set SDAT import location
def set_SDAT_import_location(location):
    global SDAT_import_location
    SDAT_import_location = location
    with open("./src/settings.json", "r", encoding="utf-8") as settings_file:
        settings_list = json.load(settings_file)
    settings_list["SDAT_import_location"] = location
    with open("./src/settings.json", "w", encoding="utf-8") as settings_file:
        json.dump(settings_list, settings_file, indent=4)

def reload_processor_ESL():
    with open("./src/settings.json", "r", encoding="utf-8") as settings_file:
        settings_list = json.load(settings_file)
    global ESL_import_location
    global esl_processor

    ESL_import_location = settings_list["ESL_import_location"]

    esl_processor = ESLProcessor(ESL_import_location)
    esl_processor.counter(esl_processor.process_files(), formatted_tuple_list)

def reload_processor_SDAT():
    with open("./src/settings.json", "r", encoding="utf-8") as settings_file:
        settings_list = json.load(settings_file)
    global SDAT_import_location
    global sdat_processor

    SDAT_import_location = settings_list["SDAT_import_location"]

    sdat_processor = SDATProcessor(SDAT_import_location)
    sdat_processor.process_files()

with open("./src/settings.json", "r", encoding="utf-8") as settings_file:
    settings_list = json.load(settings_file)
    global ESL_import_location
    global SDAT_import_location
    ESL_import_location = settings_list["ESL_import_location"]
    SDAT_import_location = settings_list["SDAT_import_location"]

# Prepare the SDAT data
global sdat_processor
sdat_processor = SDATProcessor(SDAT_import_location)
sdat_processor.process_files()

sdat_list_list = sdat_processor.get_data_for_plotting().reset_index().values.tolist()
formatted_tuple_list = []

for i in sdat_list_list:
    timestamp = pd.Timestamp(i[0])
    formatted_time = timestamp.strftime("%Y-%m-%dT%H:%M:%S")
    formatted_tuple = (formatted_time, i[1], i[2])
    formatted_tuple_list.append(formatted_tuple)

# Prepare the ESL data
global esl_processor
esl_processor = ESLProcessor(ESL_import_location)
esl_processor.counter(esl_processor.process_files(), formatted_tuple_list)

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
    
# set ESL_import_location to value defined in settings.json
with open("./src/settings.json", "r", encoding="utf-8") as settings_file:
    settings_list = json.load(settings_file)
ESL_import_location = settings_list["ESL_import_location"]

# set SDAT_import_location to value defined in settings.json
with open("./src/settings.json", "r", encoding="utf-8") as settings_file:
    settings_list = json.load(settings_file)
SDAT_import_location = settings_list["SDAT_import_location"]

def call(sender, app_data):
            if sender == "SDAT_import":
                combo_id_items = dpg.get_item_configuration("combo_id")["items"]
                set_SDAT_import_location(app_data["file_path_name"])
                reload_processor_SDAT()
                dpg.configure_item("combo_id", items=[current_language[3], combo_id_items[1]], default_value=current_language[3], callback=update_data)
                update_data("combo_id", None)

            elif sender == "ESL_import":
                combo_id_items = dpg.get_item_configuration("combo_id")["items"]
                set_ESL_import_location(app_data["file_path_name"])
                reload_processor_ESL()
                dpg.configure_item("combo_id", items=[combo_id_items[0], current_language[4]], default_value=combo_id_items[0], callback=update_data)
                update_data("combo_id", None)

            elif sender == "CSV_export":
                set_data_export_location(app_data["file_path_name"])
                export_csv(sender, app_data)
            
            elif sender == "JSON_export":
                set_data_export_location(app_data["file_path_name"])
                export_json(sender, app_data)

            elif sender == "URL_export":
                set_data_export_URL(app_data)
                export_http(sender, app_data)

#create export function for CSV
def export_csv(sender, app_data):
    option = dpg.get_value(combo_id)
    if option == "SDAT":
        data = esl_processor.get_data_for_plotting()

    elif option == "ESL":
        data = esl_processor.get_data_for_plotting()

    elif option == current_language[3]:
        data = esl_processor.get_data_for_plotting_counter()

    elif option == current_language[4]:
        data = esl_processor.get_data_for_plotting_counter()
    
    csv_exporter = CSVExporter(data, data_export_location)
    csv_exporter.export()

# create export function for JSON
def export_json(sender, app_data):
    option = dpg.get_value(combo_id)
    if option == "SDAT":
        data = esl_processor.get_data_for_plotting()

    elif option == "ESL":
        data = esl_processor.get_data_for_plotting()

    elif option == current_language[3]:
        data = esl_processor.get_data_for_plotting_counter()

    elif option == current_language[4]:
        data = esl_processor.get_data_for_plotting_counter()
    
    json_exporter = JSONExporter(data, data_export_location)
    json_exporter.export()

# create export function for HTTP
def export_http(sender, app_data):
    option = dpg.get_value(combo_id)

    if option == "SDAT":
        data = sdat_processor.get_data_for_plotting()

    elif option == "ESL":
        data = esl_processor.get_data_for_plotting_counter()

    elif option == current_language[3]:
        data = esl_processor.get_data_for_plotting_counter()

    elif option == current_language[4]:
        data = esl_processor.get_data_for_plotting_counter()
    
    http_exporter = HTTPExporter(data, data_export_URL)
    
    try: 
        http_exporter.export()
    except:
        print("HTTP export failed")

with dpg.window(label=current_language[11]) as main_window:
    # Dropdown to select between SDAT and ESL
    items = ["SDAT", "ESL"]
    def_val = "SDAT"
    with open("./src/settings.json", "r", encoding="utf-8") as settings_file:
        settings_list = json.load(settings_file)
    if settings_list["SDAT_import_location"] != "":
        items[0] = current_language[3]
        def_val = current_language[3]
    if settings_list["ESL_import_location"] != "":
        items[1] = current_language[4]

    combo_id = dpg.add_combo(label=current_language[2], items=items, default_value=def_val, callback=update_data, tag="combo_id")

    with dpg.menu_bar():
        with dpg.menu(label=current_language[0]):
            dpg.add_file_dialog(directory_selector=True, show=False, tag="CSV_export", callback=call, height=300)
            dpg.add_menu_item(label="CSV", callback=lambda: dpg.show_item("CSV_export"))

            dpg.add_file_dialog(directory_selector=True, show=False, tag="JSON_export", callback=call, height=300)
            dpg.add_menu_item(label="JSON", callback=lambda: dpg.show_item("JSON_export"))

            with dpg.window(label="New export URL", modal=True, show=False, tag="modal_id", no_title_bar=True):

                dpg.add_text("Please enter your URL for the HTTP export: ")
                dpg.add_separator()
                dpg.add_input_text(label="URL", default_value="https://api.npoint.io/bf1d2bef297f90b39861", tag="URL_export", callback=call)

                with dpg.group(horizontal=True):
                    dpg.add_button(label="OK", width=75, callback=lambda: dpg.configure_item("modal_id", show=False))
                    dpg.add_button(label="Cancel", width=75, callback=lambda: dpg.configure_item("modal_id", show=False))

            dpg.add_menu_item(label="HTTP-URL", callback=lambda: dpg.configure_item("modal_id", show=True))

        with dpg.menu(label=current_language[1]):
            dpg.add_file_dialog(directory_selector=True, show=False, tag="SDAT_import", callback=call)
            dpg.add_menu_item(label=current_language[8], callback=lambda: dpg.show_item("SDAT_import"))

            dpg.add_file_dialog(directory_selector=True, show=False, tag="ESL_import", callback=call)
            dpg.add_menu_item(label=current_language[9], callback=lambda: dpg.show_item("ESL_import"))

            light_mode_toggle = dpg.add_checkbox(label=current_language[12], callback=toggle_theme)
        
        with dpg.menu(label="Language"):
            dpg.add_menu_item(label="English", callback=lambda: set_language("English"))
            dpg.add_menu_item(label="German", callback=lambda: set_language("German"))
            dpg.add_menu_item(label="French", callback=lambda: set_language("French"))
            dpg.add_menu_item(label="Spanish", callback=lambda: set_language("Spanish"))

            with dpg.group(horizontal=True):
                dpg.add_text(default_value=current_language[13], color=(255, 0, 0, 255))
    
    with dpg.plot(label=current_language[10], height=-1, width=-1):
        dpg.add_plot_legend()

        # Axes
        dpg.add_plot_axis(dpg.mvXAxis, label=current_language[7], time=True)
        y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="kWh")
        
        # Initial data
        plot_data = sdat_processor.get_data_for_plotting()
        timestamps = pd.to_datetime(plot_data.index).view('int64') // 10**9
        timestamps = timestamps.astype(float).tolist()
        consumption_data = plot_data['Consumption'].tolist()
        production_data = plot_data['Production'].tolist()
        
        # Adding the consumption line
        consumption_line = dpg.add_line_series(timestamps, consumption_data, label=current_language[5], parent=y_axis)
        
        # Adding the production line
        production_line = dpg.add_line_series(timestamps, production_data, label=current_language[6], parent=y_axis)

# Initialize the data
update_data(combo_id, None)
light_theme = create_theme_imgui_light()
dark_theme = create_theme_imgui_dark()

# set theme to value defined in settings.json
with open("./src/settings.json", "r", encoding="utf-8") as settings_file:
    settings_list = json.load(settings_file)
if settings_list["theme"] == "Light":
    dpg.bind_theme(light_theme)
    dpg.set_value(light_mode_toggle, True)
else:
    dpg.bind_theme(dark_theme)
    dpg.set_value(light_mode_toggle, False)

with open("./src/settings.json", "r", encoding="utf-8") as settings_file:
    settings_list = json.load(settings_file)


dpg.create_viewport(title=current_language[11], width=800, height=600)
dpg.setup_dearpygui()

dpg.set_viewport_small_icon("./src/icon.ico")
dpg.set_viewport_large_icon("./src/icon.ico")

dpg.show_viewport()
dpg.set_primary_window(main_window, True)
dpg.start_dearpygui()
dpg.destroy_context()
