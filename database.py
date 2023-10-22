"""_summary_
"""
import datetime
import logging
import os
import sys
from tkinter import filedialog

import matplotlib.pyplot as plt
import pandas as pd

RTDIR: str = os.getcwd()

class Database:
    """_summary_
    """
    def __init__(self, path):
        """
        TODO: Dataframe or path?
        """
        # Initial Logger Settings
        fmt_main = "%(asctime)s\t| %(levelname)s\t| %(message)s"
        logging.basicConfig(format=fmt_main, level=logging.INFO,
                    datefmt="%Y-%m-%d %H:%M:%S")

        # Validate Path
        if path == "" or not os.path.exists(path):
            logging.info("Path blank, use tkinter dialog to pick.")
            path = filedialog.askopenfilename(
                title="Select Current Data File",
                filetypes=[
                    ("CSV Reports", "csv")
                ],
                initialdir=f"{RTDIR}\\database\\")
            if path == "":
                logging.error("Tkinter Filedialog cancelled.")
                sys.exit(1)

        logging.info("Opening file:\t%s", path)
        # self.d_frame: pd.DataFrame = pd.DataFrame([])
        self.d_frame: pd.DataFrame = pd.read_csv(path)

    def gen_plot(self, title: str, x_label: str, y_label: str, start: int=0, stop: int=-1):
        # Determine the end of the dataset sample
        if stop == -1:
            stop = len(self.d_frame)-1

        # First and last hour
        first_datetime = datetime.datetime.strptime(self.d_frame["Name"][start], "%Y-%m-%d_%Hh")
        last_datetime = datetime.datetime.strptime(self.d_frame["Name"][stop], "%Y-%m-%d_%Hh")
        first_hour = int(datetime.datetime.timestamp(first_datetime))
        last_hour = int(datetime.datetime.timestamp(last_datetime))

        # Generate the range that will be labeled on the graph
        h_ticks: range = range(first_hour, last_hour + 1,86400)             # The actual values on the graph
        d_ticks: range = range(0, int((last_hour-first_hour)/86400) + 1)    # What will be marked for the viewer

        # Generate plot data
        plt.plot(self.d_frame[x_label], self.d_frame[y_label])

        # Label Data
        plt.title(title)
        plt.xlabel(x_label)
        plt.xticks(ticks=h_ticks, labels=d_ticks)
        plt.ylabel(y_label)
        plt.savefig(f"data/{title}.png")
        plt.close()

    def gen_scatter(self):
        pass
    
    def gen_bar(self):
        pass

if __name__ == "__main__":
    db = Database("./data/palm1/dat.csv")
    db.gen_plot(
        title="Soil Moisture",
        x_label="Name",
        y_label="Soil Moisture"
    )
