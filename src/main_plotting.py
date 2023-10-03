import dearpygui.dearpygui as dpg
from data_processors.esl_processor import ESLProcessor
from data_processors.sdat_processor import SDATProcessor
import pandas as pd

class Plotdata():
    def __init__(self):
        esl = ESLProcessor('./data/ESL-Files/')
        esl.process_files()
        data_for_plotting_esl = esl.get_data_for_plotting()

        sdat = SDATProcessor('./data/SDAT-Files/')
        sdat.process_files()
        data_for_plotting_sdat = sdat.get_data_for_plotting()

        self.data_esl = data_for_plotting_esl
        self.data_sdat = data_for_plotting_sdat
    
    def get_data_esl(self):
        return self.data_esl
    
    def get_data_sdat(self):
        return self.data_sdat
    
    def plot_data(self):
        cons = self.get_data_esl()["Consumption"].values.tolist()
        prod = self.get_data_esl()["Production"].values.tolist()
        timestamps = self.get_data_esl().index.values.tolist()

        dpg.create_context()
        
        x_axis = []
        y_axis1 = []
        y_axis2 = []

        for i in range(len(timestamps)):
            x_axis.append(i)
            y_axis1.append(cons[i])
            y_axis2.append(prod[i])
        
        with dpg.window(label="Plotted Data thingy", width=400, height=400):
            with dpg.plot(label="Plot that stuff", height=400, width=-1):
                dpg.add_plot_legend()

                # create x axis
                dpg.add_plot_axis(dpg.mvXAxis, label="Time", no_gridlines=True, no_tick_marks=True)

                # create y axis and series 1
                dpg.add_plot_axis(dpg.mvYAxis, label="Consumption", no_gridlines=True, no_tick_marks=True)
                dpg.add_line_series(x_axis, y_axis1, label="Consumption", parent=dpg.last_item())

                # create y axis and series 2
                dpg.add_plot_axis(dpg.mvYAxis, label="Production", no_gridlines=True, no_tick_marks=True)
                dpg.add_line_series(x_axis, y_axis2, label="Production", parent=dpg.last_item())

        dpg.create_viewport(title='Custom Title', width=800, height=600)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()
    
    def plot_data_big(self):
        cons = self.get_data_sdat()["Consumption"].values.tolist()
        prod = self.get_data_sdat()["Production"].values.tolist()
        timestamps = self.get_data_sdat().index.values.tolist()

        dpg.create_context()
        
        x_axis = []
        y_axis1 = []
        y_axis2 = []

        for i in range(len(timestamps)):
            x_axis.append(i)
            y_axis1.append(cons[i])
            y_axis2.append(prod[i])
        
        with dpg.window(label="Plotted Data thingy", width=400, height=400):
            with dpg.plot(label="Plot that stuff", height=400, width=-1):
                dpg.add_plot_legend()

                # create x axis
                dpg.add_plot_axis(dpg.mvXAxis, label="Time", no_gridlines=True, no_tick_marks=True)

                # create y axis and series 1
                dpg.add_plot_axis(dpg.mvYAxis, label="Consumption", no_gridlines=True, no_tick_marks=True)
                dpg.add_line_series(x_axis, y_axis1, label="Consumption", parent=dpg.last_item())

                # create y axis and series 2
                dpg.add_plot_axis(dpg.mvYAxis, label="Production", no_gridlines=True, no_tick_marks=True)
                dpg.add_line_series(x_axis, y_axis2, label="Production", parent=dpg.last_item())

        dpg.create_viewport(title='Custom Title', width=800, height=600)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()
        


if __name__ == '__main__':
    plt = Plotdata()
    plt.plot_data()
    plt.plot_data_big()
