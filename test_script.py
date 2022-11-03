# import ..agdata
import os
import agdata

RTDIR = os.getcwd()
OUTDAT = RTDIR + "/data/"

# agdata.acq_data(OUTDAT)
# df = pd.read_csv(OUTDAT + "/test.csv", usecols=['two'])
df = agdata.acq_data(OUTDAT)
print(df)
print(df['two'])
print(type(df))