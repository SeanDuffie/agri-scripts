""" @file database.py
    @author Sean Duffie
    @brief A Python SQL wrapper class
"""
import datetime
import logging
import sqlite3

import pandas as pd

# from typing import Any, Dict, Protocol, Union
# from typing_extensions import TypeAlias, Annotated

# COL: TypeAlias = Dict[]

# Initial Logger Settings
FMT_MAIN = "%(asctime)s\t| %(levelname)s\t| DATABASE: %(message)s"
logging.basicConfig(format=FMT_MAIN, level=logging.INFO,
            datefmt="%Y-%m-%d %H:%M:%S")


class Database():
    """ This class serves as a wrapper for my SQL database.
    
        Create Connection
        Create Table
            from dataframe
            from headers
        Delete Table
        List Tables
        Export to pandas dataframe
        Export to csv
        Insert Row
        Delete Row
        TODO: Select cursor options
            - Select Datetime range
        FIXME: Table might need to be objectified
    """
    def __init__(self, db_name: str = "my_database.db", db_path: str = "./") -> None:
        """ Constructor for the database class
        
        The SQLite3 connection and cursor are both constructed on initial setup, but if
        close() is ever called then it must be reopened using create_connection() later on.

        Args:
            fname (str): filename for the database to store to and read from
        """
        # Generate the connection to the database file, if there is no file then create a new one
        self.db_name = db_name
        self.db_path = db_path
        self.create_connection(db_file=db_name, db_path=db_path)
        if self.con is None or self.cursor is None:
            logging.error("Failed to make connection!")


    def create_connection(self, db_file: str = "my_database.db", db_path: str = "./") -> sqlite3.Connection:
        """ Creates the connection with the sqlite database file

        Args:
            db_file (str, optional): the name of the file that will contain the database.
                                        Defaults to "my_database.db".

        Returns:
            sqlite3.Connection: The sqlite object that interacts with the database
        """
        try:
            # Create a connection to the SQL database file
            self.con = sqlite3.connect(f"{db_path}{db_file}")
            # Create a cursor
            self.cursor = self.con.cursor()
        except sqlite3.Error as e:
            logging.error("Failed to create connection!")
            print(e)

    def create_table(self, t_name: str, cols, ref: tuple = None) -> bool:
        """ Create a new table from scratch with a given set of headers

        Example:
            table = [
                ("name", "text", "NOT NULL"),
                ("begin_date", "text", ""),
                ("end_date", "text", "")
            ]

        Args:
            t_name (str): table name, used to access the specific data table in the database
            cols (list): if creating a new table, specify the header names. Defaults to None.
            ref (tuple, optional): reference table

        Returns:
            bool: Was the table created successfully?
        """
        t_cols = ""
        # Iterate through the parameter to determine what columns to add
        for i, ent in enumerate(cols):
            if i == len(cols)-1:
                t_cols += f"{ent[0]} {ent[1]} {ent[2]}"
            else:
                t_cols += f"{ent[0]} {ent[1]} {ent[2]},\n"

        # Format the SQL string command that will be executed
        if ref is not None:
            sql_table_formatted = f"""CREATE TABLE IF NOT EXISTS {t_name} (
                                        {t_cols},
                                        Foreign Key ({ref[0]}) REFERENCES {ref[1]} ({ref[2]})
                                    );"""
        else:
            sql_table_formatted = f"""CREATE TABLE IF NOT EXISTS {t_name} (
                                        {t_cols}
                                    );"""
        # if ref is not None:
        #     sql_table_formatted = f"""CREATE TABLE IF NOT EXISTS {t_name} (
        #                                 id integer AUTO_INCREMENT PRIMARY KEY,
        #                                 {t_cols},
        #                                 Foreign Key ({ref[0]}) REFERENCES {ref[1]} ({ref[2]})
        #                             );"""
        # else:
        #     sql_table_formatted = f"""CREATE TABLE IF NOT EXISTS {t_name} (
        #                                 id integer AUTO_INCREMENT PRIMARY KEY,
        #                                 {t_cols}
        #                             );"""

        # Attempt to execute the specified
        try:
            self.cursor.execute(sql_table_formatted)
            self.con.commit()
            return True
        except sqlite3.Error as e:
            logging.error("Failed to create table from scratch!")
            print(e)
            return False

    def drop_table(self, t_name: str) -> bool:
        """ Deletes the specified table from the database

        Args:
            t_name (str): table name designated to be deleted

        Returns:
            bool: Success or Failure
        """
        sql_format = f"DROP TABLE IF EXISTS {t_name};"

        # Attempt to delete/drop the table, but catch any errors
        try:
            self.cursor.execute(sql_format)
            self.con.commit()
            return True
        except sqlite3.Error as e:
            logging.error("Failed to drop table!")
            print(e)
            return False

    def list_tables(self):
        """ Lists all tables currently present in the database """
        sql_format = "SELECT name FROM sqlite_master WHERE type='table';"

        try:
            self.cursor.execute(sql_format)
            print(self.cursor.fetchall())
        except sqlite3.Error as e:
            logging.error("Failed to list tables!")
            print(e)

    def insert_row(self, t_name: str, row, headers: str = ""):
        """ Inserts a row into the specified table

        TODO: Add Error handling for validating the row format
        TODO: [Maybe?] Add a check to make sure there isn't duplicate data

        Args:
            t_name (str): Name of the table to be modified
            row (list): Row to be appended to the table

        Returns:
            bool: Success
        """
        sql_format = f"INSERT INTO {t_name} {headers} VALUES {row}"

        try:
            self.cursor.execute(sql_format)
            self.con.commit()
            return True
        except sqlite3.Error as e:
            logging.error("Failed insert row into table %s!", t_name)
            print(e)
            return False

    def delete_row(self, t_name: str, index: int):
        """ Deletes row at specified index
        
        TODO: Add error handling for certain index exceptions
        TODO: Add ability to delete by datetime

        Args:
            t_name (str): Name of the table to be modified
            index (int): index of the row to be deleted

        Returns:
            bool: Success
        """
        sql_format = f"DELETE FROM {t_name} WHERE 'index' = {index}"

        try:
            self.cursor.execute(sql_format)
            self.con.commit()
            return True
        except sqlite3.Error as e:
            logging.error("Failed delete row from table %s at index %d!", t_name, index)
            print(e)
            return False

    def df_to_table(self, df: pd.DataFrame, t_name: str) -> bool:
        """ Save a pandas dataframe to a table in the existing database

        Args:
            df (pd.DataFrame): input pandas dataframe
        
        Returns:
            bool: Success or not
        """
        # Attempt to create
        try:
            df.to_sql(t_name, self.con, if_exists="fail", index=False)
            self.con.commit()
            return True
        except sqlite3.Error as e:
            logging.error("Failed to create a table from dataframe!")
            print(e)
            return False

    def get_df(self, t_name: str) -> pd.DataFrame:
        """ Returns a pandas dataframe retrieved from the database table

        TODO: add ability to control the rows/columns included in the dataframe

        Args:
            t_name (str): name of the table being requested

        Returns:
            pd.DataFrame: database populated pandas dataframe
        """
        return pd.read_sql(
            sql=f"select * from {t_name}",
            con=self.con
        )
        # def dt(timestamp):
        #     return datetime.datetime.strptime(timestamp, "%Y-m-%d %H:M:S")
        # db["Date"] = db["Date"].apply(dt, 1)

    def export_csv(self, t_name: str, out_path: str = "."):
        """ Generate a csv from a specified table

        TODO: add ability to control the rows/columns going into the csv

        Args:
            t_name (str): name of the table in the database, also serves as name of output csv file
            out_path (str, optional): location of output csv. Defaults to ".".
        """
        df = self.get_df(t_name=t_name)
        df.to_csv(f"{out_path}/{t_name}.csv", header=True, index=False)

    def custom_sql_command(self, cmd: str):
        """ This is a custom function for me to test new sql functions

        Args:
            cmd (str): pre-formatted SQL string command

        Returns:
            bool: Success or failure
        """
        try:
            self.cursor.execute(cmd)
            self.con.commit()
            return True
        except sqlite3.Error as e:
            logging.error("Custom SQL command failed!")
            print(e)
            return False

    def close(self):
        """ Close the connection (Usually not needed)
            Database must call create_connection again to be usable
        """
        self.cursor.close()
        self.con.close()


def clean_old_set():
    """ This function was used to convert the old dataset to the new Database format.
        Shouldn't be needed anymore but is kept for reference.
    """
    def timeform(ts: str):
        return datetime.datetime.strptime(ts, "%Y-%m-%d_%Hh")

    dat = pd.read_csv(filepath_or_buffer="./data/palm1/dat.csv")
    # print(dat)
    dat = dat.drop("Month", axis=1)
    dat = dat.drop("Day", axis=1)
    dat = dat.drop("Hour", axis=1)
    dat = dat.drop("Amount Watered", axis=1)
    dat = dat.drop("Watered?", axis=1)
    dat = dat.drop("Days without water", axis=1)

    # print(dat)
    dat["Date"] = dat["Date"].apply(timeform, 1)
    print(dat)

if __name__ == "__main__":
    # Initialize Database
    db = Database(db_name="test.db")

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
        ("Soil Moisture", "integer", ""),
        ("Light Intensity", "integer", ""),
        ("Temperature", "real", ""),
        ("Humidity", "real", "")
    ]
    db.create_table("palm", table)
    df2 = pd.read_csv(filepath_or_buffer="./dat_palm.csv")
    # keys = f"{df2.keys().to_list()}".replace("[","(").replace("]",")").replace("'","")
    start = datetime.datetime.now()
    for pd_row in df2.itertuples(index=True, name=None):
        print(type(pd_row))
        db.insert_row(t_name="palm", row=pd_row)
    stop = datetime.datetime.now()
    # print(db.get_df("palm"))

    elapsed = stop-start
    count = df2.shape[0]
    print(f"Inserted {count} rows in {elapsed} seconds ({elapsed/count} per row)")
    db.list_tables()
