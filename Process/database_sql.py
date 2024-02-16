""" @file database.py
    @author Sean Duffie
    @brief A Python SQL wrapper class
"""
import logging
import sqlite3

import pandas as pd

# from typing import Any, Dict, Protocol, Union
# from typing_extensions import TypeAlias, Annotated

# COL: TypeAlias = Dict[]

# Initial Logger Settings
FMT_MAIN = "%(asctime)s\t| %(levelname)s\t| %(message)s"
logging.basicConfig(format=FMT_MAIN, level=logging.INFO,
            datefmt="%Y-%m-%d %H:%M:%S")


class Database():
    """ This class serves as a wrapper for my SQL database.

        

    """
    def __init__(self, fname: str, tname: str, cols) -> None:
        self.con = self.create_connection(db_file=fname)

        if self.con is None:
            logging.error("Failed to make connection!")

        if not self.create_table(self.con, tname, cols=cols):
            logging.error("Failed to create table!")

        # Create a cursor
        self.cursor = self.con.cursor()

    def create_connection(self, db_file: str = "my_database.sqlite") -> sqlite3.Connection:
        """_summary_

        Args:
            db_file (str, optional): the name of the file that will contain the database.
                                        Defaults to "my_database.sqlite".

        Returns:
            _type_: _description_
        """
        conn = None

        try:
            # Create a connection to the SQL database file
            conn = sqlite3.connect(db_file)
        except sqlite3.Error as e:
            print(e)

        return conn

    def table_from_df(self, df: pd.DataFrame, tname: str) -> bool:
        """_summary_

        Args:
            df (pd.DataFrame): _description_
        """
        return df.to_sql(tname, self.con, if_exists="fail", index=True)

    def get_df(self, tname: str) -> pd.DataFrame:
        """_summary_

        Args:
            table (str): _description_

        Returns:
            _type_: _description_
        """
        return pd.read_sql(f"select * from {tname}", self.con)

    def create_table(self,
                     conn: sqlite3.Connection,
                     t_name: str,
                     cols,
                     ref: tuple | None = None) -> bool:
        """_summary_

        Args:
            conn (sqlite3.Connection): _description_.
            t_name (str): 

        Returns:
            bool: Was the table created successfully?
        """
        t_cols = ""
        for i, ent in enumerate(cols):
            if i == len(cols)-1:
                t_cols += f"{ent[0]} {ent[1]} {ent[2]}"
            else:
                t_cols += f"{ent[0]} {ent[1]} {ent[2]},\n"

        if ref is not None:
            sql_table_formatted = f"""CREATE TABLE IF NOT EXISTS {t_name} (
                                        id integer AUTO_INCREMENT PRIMARY KEY,
                                        {t_cols},
                                        Foreign Key ({ref[0]}) REFERENCES {ref[1]} ({ref[2]})
                                    );"""
        else:
            sql_table_formatted = f"""CREATE TABLE IF NOT EXISTS {t_name} (
                                        id integer AUTO_INCREMENT PRIMARY KEY,
                                        {t_cols}
                                    );"""

        # sql_table_formatted = f"""CREATE TABLE IF NOT EXISTS {t_name} (
        #                             id integer PRIMARY KEY,
        #                             name text NOT NULL,
        #                             priority integer,
        #                             status_id integer NOT NULL,
        #                             project_id integer NOT NULL,
        #                             begin_date text NOT NULL,
        #                             end_date text NOT NULL,
        #                             FOREIGN KEY (project_id) REFERENCES projects (id)
        #                         );"""

        print(sql_table_formatted)

        try:
            cur = conn.cursor()
            cur.execute(sql_table_formatted)
        except sqlite3.Error as e:
            print(e)
        # conn.commit()

        return True

if __name__ == "__main__":
    dat = pd.read_csv(filepath_or_buffer="./data/AeroGarden1/dat.csv")

    table = [
        ("name", "text", "NOT NULL"),
        ("begin_date", "text", ""),
        ("end_date", "text", "")
    ]
    db = Database(tname="tbl", fname="test.db", cols=table)
    db.table_from_df(dat, "csv")
    print(db.get_df("csv"))
