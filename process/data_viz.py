""" @file database.py
    @author Sean Duffie
    @brief A Python SQL wrapper class
    
    FIXME: This file got mutilated in a merge conflict, fix later and reorient towards data vizualization
"""
import datetime
import logging

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
        """
        TODO: Dataframe or path?
        """
        # # Validate Path
        # if path == "" or not os.path.exists(path):
        #     logging.info("Path blank, use tkinter dialog to pick.")
        #     path = filedialog.askopenfilename(
        #         title="Select Current Data File",
        #         filetypes=[
        #             ("CSV Reports", "csv")
        #         ],
        #         initialdir=f"{RTDIR}/database/")
        #     if path == "":
        #         logging.error("Tkinter Filedialog cancelled.")
        #         sys.exit(1)


        # logging.info("Opening file:\t%s", self.data_path)
        # # self.d_frame: pd.DataFrame = pd.DataFrame([])
        # self.d_frame: pd.DataFrame = pd.read_csv(self.data_path)
        self.d_frame = dframe
        
        def timestamp2UTC(tstamp: str):
            """ Function to apply to the dataframe to convert the timestamps to plottable utc ints

            Args:
                tstamp (str): Raw strng timestamp from dataframe

            Returns:
                int: utc value, seconds passed since 1970.
            """
            # TODO: do the to_datetime thing
            dt = datetime.datetime.strptime(tstamp, "%Y-%m-%d_%Hh")
            utc = int(datetime.datetime.timestamp(dt))
            return utc
        self.d_frame["UTC"] = self.d_frame["Date"].apply(timestamp2UTC)

    def gen_plot(self, y_label: str, x_label: str = "UTC", title: str = "", start: int=0, stop: int=-1):
        """_summary_

        Args:
            y_label (str): _description_
            x_label (str, optional): _description_. Defaults to "UTC".
            title (str, optional): _description_. Defaults to "".
            start (int, optional): _description_. Defaults to 0.
            stop (int, optional): _description_. Defaults to -1.

        Returns:
            _type_: _description_
        """
        # Determine the end of the dataset sample
        SEG = True
        if stop == -1:
            stop = len(self.d_frame)-1
        if start > stop:
            logging.error("Starting point must be before stopping point.")
            return False
        if title == "":
            title = f"{y_label}_vs_{x_label}"
        if start == 0 and stop == len(self.d_frame)-1:
            SEG = False

        # First and last hour
        first = self.d_frame["UTC"][start]
        last = self.d_frame["UTC"][stop]

        tstmp1 = datetime.datetime.strftime(datetime.datetime.fromtimestamp(first), "%d-%Hh")
        tstmp2 = datetime.datetime.strftime(datetime.datetime.fromtimestamp(last), "%d-%Hh")
        if SEG:
            title = f"{title}_{tstmp1}to{tstmp2}"

        # Generate the range that will be labeled on the graph
        h_ticks: range = range(first, last + 86400,86400)             # Actual values on the graph
        d_ticks: range = range(int(first/86400), int(last/86400) + 1)    # Marked for the viewer

        # Generate plot data
        plt.plot(self.d_frame[x_label][start:stop], self.d_frame[y_label][start:stop])

        # Label Data
        plt.title(title)
        plt.xlabel(x_label)
        plt.xticks(ticks=h_ticks, labels=d_ticks)
        plt.ylabel(y_label)
        plt.savefig(f"{self.dir_path}/{title}.png")
        plt.close()

    def gen_scatter(self):
        """_summary_
        """

    def gen_bar(self):
        """_summary_
        """

if __name__ == "__main__":
    # Initialize Database
    db = Database(f_name="test.db")

    # Drop existing table for testing purposes
    db.list_tables()
    db.drop_table("AeroGarden")

    # Read data from old csv and populate table all at once
    df1 = pd.read_csv(filepath_or_buffer="./dat_aerogarden.csv")
    start = datetime.datetime.now()
    db.df_to_table(df=df1, t_name="AeroGarden")
    stop = datetime.datetime.now()
    # print(db.get_df("AeroGarden"))
    elapsed = stop-start
    count = df1.shape[0]
    print(f"Inserted {count} rows in {elapsed} seconds ({elapsed/count} per row)")

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
    start = datetime.datetime.now()
    for pd_row in df2.itertuples(index=True, name=None):
        db.insert_row(t_name="palm", row=pd_row)
    stop = datetime.datetime.now()
    # print(db.get_df("palm"))

    elapsed = stop-start
    count = df2.shape[0]
    print(f"Inserted {count} rows in {elapsed} seconds ({elapsed/count} per row)")
    db.list_tables()
