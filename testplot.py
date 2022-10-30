
import os
from os.path import exists
import json
import matplotlib.pyplot as plt

# Acquire Initial Data
RTDIR = os.getcwd()
IMGDIR = RTDIR + "/autocaps/"
OUTDAT = RTDIR + "/data/"

# Read data history
if (exists(OUTDAT + "dat.json")):
    print("Loading current file...")
    f = open(OUTDAT + "dat.json")
    data = json.load(f)
    f.close()
else:
    data = {
        "TIME": list(),
        "LIGHT": [],
        "SOIL": [],
        "TEMPC": [],
        "TEMPF": [],
        "HUMID": []
    }

## Start Generate Plots ##
cnt = 0
iter = []
hrs = []
for stamp in data["TIME"]:
    cnt += 1
    iter.append(cnt)
    hrs.append(int(stamp[11:13]))

# Plot Total Soil Moisture
plt.plot(iter, data["SOIL"])
plt.xlabel("Time (Hours)")
plt.ylabel("Soil Moisture")
plt.savefig("data/Soil_Moisture_custom.png")
plt.close()