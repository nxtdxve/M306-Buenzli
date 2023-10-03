import tkinter as tk
from tkinter import *
from tkinter import ttk
from datetime import datetime


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
        header = tk.Canvas(
            root, width=1200, height=75, bg="#f9f9f9", highlightthickness=0
        )
        header.place(x=0, y=0)

        export_dropdown = ttk.Combobox(
            header,
            values=["CSV", "JSON", "Hochladen"],
            width=10,
            font=("Arial", 13),
            state="readonly",
        )
        export_dropdown.place(relx=0.05, rely=0.5, height=50, anchor="center")
        export_dropdown.set("CSV")

        # Date Section
        date_text = tk.Label(header, text="Datum:", bg="#f9f9f9", font=("Arial", 20))
        date_text.place(relx=0.16, rely=0.5, anchor="center")
        start_date_year = ttk.Combobox(
            header,
            values=["2019", "2020", "2021", "2022"],
            width=4,
            font=("Arial", 13),
            state="readonly",
        )
        start_date_year.place(relx=0.23, rely=0.5, height=50, anchor="center")
        start_date_year.set("2019")
        start_date_month = ttk.Combobox(
            header,
            values=[str(i).zfill(2) for i in range(1, 13)],
            width=2,
            font=("Arial", 13),
            state="readonly",
        )
        start_date_month.place(relx=0.2725, rely=0.5, height=50, anchor="center")
        start_date_month.set("01")
        start_date_day = ttk.Combobox(
            header,
            values=[str(i).zfill(2) for i in range(1, 32)],
            width=2,
            font=("Arial", 13),
            state="readonly",
        )
        start_date_day.place(relx=0.3075, rely=0.5, height=50, anchor="center")
        start_date_day.set("01")
        to_text = tk.Label(header, text="-", bg="#f9f9f9", font=("Arial", 20))
        to_text.place(relx=0.3425, rely=0.5, anchor="center")
        end_date_year = ttk.Combobox(
            header,
            values=["2019", "2020", "2021", "2022"],
            width=4,
            font=("Arial", 13),
            state="readonly",
        )
        end_date_year.place(relx=0.3825, rely=0.5, height=50, anchor="center")
        end_date_year.set("2022")
        end_date_month = ttk.Combobox(
            header,
            values=[str(i).zfill(2) for i in range(1, 13)],
            width=2,
            font=("Arial", 13),
            state="readonly",
        )
        end_date_month.place(relx=0.425, rely=0.5, height=50, anchor="center")
        end_date_month.set("09")
        end_date_day = ttk.Combobox(
            header,
            values=[str(i).zfill(2) for i in range(1, 32)],
            width=2,
            font=("Arial", 13),
            state="readonly",
        )
        end_date_day.place(relx=0.46, rely=0.5, height=50, anchor="center")
        end_date_day.set("12")

        # Legend Section
        legend_text = tk.Label(
            header, text="Legende:", bg="#f9f9f9", font=("Arial", 20)
        )
        legend_text.place(relx=0.55, rely=0.5, anchor="center")
        blue_box = tk.Canvas(
            header, width=20, height=20, bg="#0000ff", highlightthickness=0
        )
        blue_box.place(relx=0.62, rely=0.3, anchor="center")
        blue_text = tk.Label(
            header, text="Gebrauchter Strom", bg="#f9f9f9", font=("Arial", 13)
        )
        blue_text.place(relx=0.7, rely=0.3, anchor="center")
        red_box = tk.Canvas(
            header, width=20, height=20, bg="#ff0000", highlightthickness=0
        )
        red_box.place(relx=0.62, rely=0.7, anchor="center")
        red_text = tk.Label(
            header, text="Produzierter Strom", bg="#f9f9f9", font=("Arial", 13)
        )
        red_text.place(relx=0.7, rely=0.7, anchor="center")

        # Diagram Section
        diagram_dropdown = ttk.Combobox(
            header,
            values=["Verbrauchsdiagramm", "Zählerstandsdiagramm"],
            width=20,
            font=("Arial", 13),
            state="readonly",
        )
        diagram_dropdown.place(relx=0.87, rely=0.5, height=50, anchor="center")

        # Check Dates
        self.check_dates(
            start_date_day,
            start_date_month,
            start_date_year,
            end_date_day,
            end_date_month,
            end_date_year,
        )

    def body(self, root):
        """
        Creates the body
        """
        body = tk.Canvas(
            root, width=1200, height=600, bg="#ffffff", highlightthickness=0
        )
        body.place(x=0, y=75)

    def check_dates(
        self,
        start_date_day,
        start_date_month,
        start_date_year,
        end_date_day,
        end_date_month,
        end_date_year,
    ):
        """
        Makes sure that the inputs are valid dates
        :param start_date_day:
        :param start_date_month:
        :param start_date_year:
        :param end_date_day:
        :param end_date_month:
        :param end_date_year:
        :return:

        """
        date_list = [
            start_date_year.get(),
            start_date_month.get(),
            start_date_day.get(),
            end_date_year.get(),
            end_date_month.get(),
            end_date_day.get(),
        ]
        start_date_day.bind(
            "<<ComboboxSelected>>",
            lambda event: self.validate_date(
                start_date_year,
                start_date_month,
                start_date_day,
                end_date_year,
                end_date_month,
                end_date_day,
            ),
        )
        print(start_date_day.get())
        start_date_month.bind(
            "<<ComboboxSelected>>",
            lambda event: self.validate_date(
                start_date_year,
                start_date_month,
                start_date_day,
                end_date_year,
                end_date_month,
                end_date_day,
            ),
        )
        print(start_date_month.get())
        start_date_year.bind(
            "<<ComboboxSelected>>",
            lambda event: self.validate_date(
                start_date_year,
                start_date_month,
                start_date_day,
                end_date_year,
                end_date_month,
                end_date_day,
            ),
        )
        print(start_date_year.get())
        end_date_day.bind(
            "<<ComboboxSelected>>",
            lambda event: self.validate_date(
                start_date_year,
                start_date_month,
                start_date_day,
                end_date_year,
                end_date_month,
                end_date_day,
            ),
        )
        print(end_date_day.get())
        end_date_month.bind(
            "<<ComboboxSelected>>",
            lambda event: self.validate_date(
                start_date_year,
                start_date_month,
                start_date_day,
                end_date_year,
                end_date_month,
                end_date_day,
            ),
        )
        print(end_date_month.get())
        end_date_year.bind(
            "<<ComboboxSelected>>",
            lambda event: self.validate_date(
                start_date_year,
                start_date_month,
                start_date_day,
                end_date_year,
                end_date_month,
                end_date_day,
            ),
        )
        print(end_date_year.get())

    def validate_date(
        self,
        start_date_year,
        start_date_month,
        start_date_day,
        end_date_year,
        end_date_month,
        end_date_day,
    ):
        """
        Validates the date
        :param start_date_year:
        :param start_date_month:
        :param start_date_day:
        :param end_date_year:
        :param end_date_month:
        :param end_date_day:
        :return:
        """
        date_list = [
            start_date_year.get(),
            start_date_month.get(),
            start_date_day.get(),
            end_date_year.get(),
            end_date_month.get(),
            end_date_day.get(),
        ]
        if start_date_year.get() == end_date_year.get():
            if start_date_month.get() == end_date_month.get():
                if start_date_day.get() > end_date_day.get():
                    end_date_day.set(start_date_day.get())
            elif start_date_month.get() > end_date_month.get():
                end_date_month.set(start_date_month.get())
                end_date_day.set(start_date_day.get())
        elif start_date_year.get() > end_date_year.get():
            end_date_year.set(start_date_year.get())
            end_date_month.set(start_date_month.get())
            end_date_day.set(start_date_day.get())

        if start_date_year.get() == "2022":
            if start_date_month.get() == "09":
                if start_date_day.get() > "12":
                    start_date_day.set("12")
            elif start_date_month.get() > "09":
                start_date_month.set("09")
                start_date_day.set("12")

        if end_date_year.get() == "2022":
            if end_date_month.get() == "09":
                if end_date_day.get() > "12":
                    end_date_day.set("12")
            elif end_date_month.get() > "09":
                end_date_month.set("09")
                end_date_day.set("12")

        if start_date_day.get() == "31" and start_date_month.get() in [
            "04",
            "06",
            "09",
            "11",
        ]:
            start_date_day.set("30")
        elif start_date_day.get() == "30" and start_date_month.get() == "02":
            start_date_day.set("28")
        elif start_date_day.get() == "29" and start_date_month.get() == "02":
            if start_date_year.get() == "2020":
                start_date_day.set("29")
            else:
                start_date_day.set("28")

        if end_date_day.get() == "31" and end_date_month.get() in [
            "04",
            "06",
            "09",
            "11",
        ]:
            end_date_day.set("30")
        elif end_date_day.get() == "30" and end_date_month.get() == "02":
            end_date_day.set("28")
        elif end_date_day.get() == "29" and end_date_month.get() == "02":
            if end_date_year.get() == "2020":
                end_date_day.set("29")
            else:
                end_date_day.set("28")


if __name__ == "__main__":
    visualizer = Visualizer()
