""" @file database.py
    @author Sean Duffie
    @brief A Python SQL wrapper class
    
    FIXME: This file got mutilated in a merge conflict, fix later and reorient towards data vizualization
    TODO: Rename to visualizer.py
    FIXME: plt.ticks got messed up in gen_plot(), fix them
"""
import datetime
import logging

import matplotlib.pyplot as plt
import pandas as pd

# from typing import Any, Dict, Protocol, Union
# from typing_extensions import TypeAlias, Annotated

# Initial Logger Settings
FMT_MAIN = "%(asctime)s\t| %(levelname)s\t| Database:\t%(message)s"
logging.basicConfig(format=FMT_MAIN, level=logging.INFO,
            datefmt="%Y-%m-%d %H:%M:%S")

class Vizualizer:
    """_summary_
    """
    def __init__(self, dframe: pd.DataFrame):
        self.d_frame = dframe

    def gen_plot(self, y_label: str, x_label: str = "Date", title: str = "", start: int=0, stop: int=-1):
        """_summary_

        Args:
            y_label (str): _description_
            x_label (str, optional): _description_. Defaults to "Date".
            title (str, optional): _description_. Defaults to "".
            start (int, optional): _description_. Defaults to 0.
            stop (int, optional): _description_. Defaults to -1.

        Returns:
            _type_: _description_
        """
        y_label = y_label.replace(" ", "_")
        # Determine the end of the dataset sample
        SEG = True
        if stop == -1:
            stop = len(self.d_frame)-1
        assert stop > start
        if start > stop:
            logging.error("Starting point must be before stopping point.")
            return False
        if title == "":
            title = f"{y_label}_vs_{x_label}"
        if start == 0 and stop == len(self.d_frame)-1:
            SEG = False

        # First and last hour
        first = self.d_frame["Date"][start]
        last = self.d_frame["Date"][stop]

        tstmp1 = datetime.datetime.strftime(first, "%d-%Hh")
        tstmp2 = datetime.datetime.strftime(last, "%d-%Hh")
        if SEG:
            title = f"{title}_{tstmp1}to{tstmp2}"

        # # Generate the range that will be labeled on the graph
        # h_ticks: range = range(first, last + 86400,86400)             # Actual values on the graph
        # d_ticks: range = range(int(first/86400), int(last/86400) + 1)    # Marked for the viewer

        # Generate plot data
        plt.plot(self.d_frame[x_label][start:stop], self.d_frame[y_label][start:stop])

        # Label Data
        plt.title(title)
        plt.xlabel(x_label)
        plt.xticks(rotation=15)
        # plt.xticks(ticks=h_ticks, labels=d_ticks)
        plt.ylabel(y_label)
        plt.savefig(f"./{title}.png")
        plt.close()

    def gen_scatter(self):
        """_summary_
        """

    def gen_bar(self):
        """_summary_
        """

if __name__ == "__main__":
    from ..database import Database

    # Initialize Database
    db = Database(f_name="test.db")

    # Drop existing table for testing purposes
    db.list_tables()
    db.drop_table("AeroGarden")

    # Read data from old csv and populate table all at once
    df1 = pd.read_csv(filepath_or_buffer="./dat_aerogarden.csv")
    START = datetime.datetime.now()
    db.df_to_table(df=df1, t_name="AeroGarden")
    STOP = datetime.datetime.now()
    # print(db.get_df("AeroGarden"))
    ELAPSED = STOP-START
    count = df1.shape[0]
    print(f"Inserted {count} rows in {ELAPSED} seconds ({ELAPSED/count} per row)")

    # Drop existing table for testing purposes
    db.drop_table("palm")

    # Read data from old csv and populate table one row at a time (significantly slower)
    table = [
        ("Date", "text", ""),
        ("Soil Moisture", "text", ""),
        ("Light Intensity", "text", ""),
        ("Temperature", "text", ""),
        ("Humidity", "text", "")
    ]
    db.create_table("palm", table)
    df2 = pd.read_csv(filepath_or_buffer="./dat_palm.csv")
    # keys = f"{df2.keys().to_list()}".replace("[","(").replace("]",")").replace("'","")
    START = datetime.datetime.now()
    for pd_row in df2.itertuples(index=True, name=None):
        db.insert_row(t_name="palm", row=pd_row)
    STOP = datetime.datetime.now()
    # print(db.get_df("palm"))

    ELAPSED = STOP-START
    count = df2.shape[0]
    print(f"Inserted {count} rows in {ELAPSED} seconds ({ELAPSED/count} per row)")
    db.list_tables()
