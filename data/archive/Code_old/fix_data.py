import netCDF4 as nc
import numpy as np
import os

os.chdir("/Volumes/Extreme SSD/LE/TEMPWEP/ff")
for file in os.listdir():
    f = nc.Dataset(file, mode="a")
    del f.variables["TEMPWEP"].valid_range
    print(f.variables["TEMPWEP"])
    f.close()
