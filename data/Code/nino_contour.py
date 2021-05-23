#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 17 11:51:06 2020

@author: bengoldman
"""
import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
from eofs.standard import Eof
from matplotlib import cm
import cartopy.crs as ccrs
import cartopy

# %%
f1 = nc.Dataset("/Volumes/Extreme SSD/science_research/obs_data/HadISST_sst.nc")

sst1 = f1.variables["sst"][:, 59:120, 300:359]
sst2 = f1.variables["sst"][:, 59:120, 0:100]
sst = np.concatenate((sst1, sst2), axis=2)

lats = np.flip(f1.variables["latitude"][59:120])
lons1 = f1.variables["longitude"][300:359]
lons2 = f1.variables["longitude"][0:100] + 360
lons = np.concatenate((lons1, lons2), axis=0)

# %%
sst[sst == - 1e+30] = np.nan

solver = Eof(sst)
eof1 = np.flip(solver.eofsAsCorrelation(neofs=2)[1], axis=0)

# %%

# %%
proj = ccrs.PlateCarree(central_longitude=180)

fig = plt.figure(figsize=(15, 5))
ax = fig.add_subplot(111, projection=proj)

ax.contourf(lons, lats, eof1, cmap="coolwarm", transform=ccrs.PlateCarree(central_longitude=0))

ax.coastlines()
ax.add_feature(cartopy.feature.LAND, edgecolor='black')

fig.colorbar(cm.ScalarMappable(cmap="coolwarm"), ax=ax)
fig.suptitle("ENSO Temperature Anomaly Pattern", y=.91)
