import tkinter as tk
from tkinter import *


class Visualizer:
    """
    Visualizer class
    """

    def __init__(self):
        """
        Constructor
        """
        root = tk.Tk()
        self.open_gui(root)

    def open_gui(self, root):
        """
        Opens the GUI

        :param root: The root window
        :type root: tk.Tk

        :return: None
        """
        root.title("M306-Buenzli")
        root.geometry("1200x675")
        root.resizable(False, False)
        self.header(root)
        self.body(root)
        root.mainloop()

    def header(self, root):
        """
        Creates the header
        """
        header = tk.Canvas(root, width=1200, height=75, bg="#f9f9f9", highlightthickness=0)
        header.place(x=0, y=0)

        export_options = ['CSV', 'JSON', 'Hochladen']
        StringVar().set('CSV')
        export_dropdown = tk.OptionMenu(header, StringVar(), *export_options)
        export_dropdown.config(height=50, bg='#cccccc', width=len(max(export_options, key=len)))
        export_dropdown.place(relx=0.05, rely=0.5, anchor="center", height=50)

        date_text = tk.Label(header, text="Datum:", bg="#f9f9f9", font=("Arial", 20))
        date_text.place(relx=0.2, rely=0.5, anchor="center")
        start_date_input = tk.Entry(header, width=10, bg="#cccccc", highlightthickness=0, highlightbackground="#e9e9e9",
                                    borderwidth=0, font=("Arial", 13), justify="center")
        start_date_input.place(relx=0.28, rely=0.5, height=50, anchor="center")
        end_date_input = tk.Entry(header, width=10, bg="#cccccc", highlightthickness=0, highlightbackground="#e9e9e9",
                                  borderwidth=0, font=("Arial", 13), justify="center")
        end_date_input.place(relx=0.38, rely=0.5, height=50, anchor="center")

        legend_text = tk.Label(header, text="Legende:", bg="#f9f9f9", font=("Arial", 20))
        legend_text.place(relx=0.5, rely=0.5, anchor="center")
        blue_box = tk.Canvas(header, width=20, height=20, bg="#0000ff", highlightthickness=0)
        blue_box.place(relx=0.57, rely=0.3, anchor="center")
        red_box = tk.Canvas(header, width=20, height=20, bg="#ff0000", highlightthickness=0)
        red_box.place(relx=0.57, rely=0.7, anchor="center")
        blue_text = tk.Label(header, text="Gebrauchter Strom", bg="#f9f9f9", font=("Arial", 13))
        blue_text.place(relx=0.65, rely=0.3, anchor="center")
        red_text = tk.Label(header, text="Produzierter Strom", bg="#f9f9f9", font=("Arial", 13))
        red_text.place(relx=0.65, rely=0.7, anchor="center")

        options = ["Verbrauchsdiagramm", "Zählerstandsdiagramm"]
        dropdown = tk.OptionMenu(header, StringVar(), *options)
        dropdown.config(width=20, bg="#cccccc", highlightthickness=0, highlightbackground="#e9e9e9", borderwidth=0,
                        font=("Arial", 13))
        dropdown.place(relx=0.85, rely=0.5, anchor="center", height=50)

    def body(self, root):
        """
        Creates the body
        """
        body = tk.Canvas(root, width=1200, height=600, bg="#ffffff", highlightthickness=0)
        body.place(x=0, y=75)


if __name__ == "__main__":
    visualizer = Visualizer()
