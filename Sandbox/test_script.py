# import ..agdata
import os
import pandas as pd

RTDIR = os.getcwd()
OUTDAT = RTDIR

# agdata.acq_data(OUTDAT)
df = pd.read_csv(OUTDAT + "/test.csv", usecols=['two'])
print(df)
print(df['two'])
print(type(df))