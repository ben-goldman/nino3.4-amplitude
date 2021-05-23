#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 16:12:51 2020

@author: bengoldman
"""

# %%
import numpy as np
import netCDF4 as nc
import os


lat1 = 90
lat2 = 101
lon1 = 152
lon2 = 192

# %%
os.chdir("/Volumes/Extreme SSD/science_research/large_ensemble/CESM_LE/TREFHT/")

# Full forcing set
ff_set = np.zeros((2172, 34))
print("")
print("Full forcing")
for i in range(2, 36):
    if i < 10:
        f1 = nc.Dataset("b.e11.B20TRC5CNBDRD.f09_g16.00%s.cam.h0.TREFHT.192001-200512.nc" % i)
        f2 = nc.Dataset("b.e11.BRCP85C5CNBDRD.f09_g16.00%s.cam.h0.TREFHT.200601-208012.nc" % i)
        f3 = nc.Dataset("b.e11.BRCP85C5CNBDRD.f09_g16.00%s.cam.h0.TREFHT.208101-210012.nc" % i)

        ff_set[:, i-2] = np.concatenate((
            np.average(f1.variables["TREFHT"][:, lat1:lat2, lon1:lon2], axis=(1, 2)),
            np.average(f2.variables["TREFHT"][:, lat1:lat2, lon1:lon2], axis=(1, 2)),
            np.average(f3.variables["TREFHT"][:, lat1:lat2, lon1:lon2], axis=(1, 2))
            )) - 273
        f1.close()
        f2.close()
        f3.close()
    elif i < 34:
        f1 = nc.Dataset("b.e11.B20TRC5CNBDRD.f09_g16.0%s.cam.h0.TREFHT.192001-200512.nc" % i)
        f2 = nc.Dataset("b.e11.BRCP85C5CNBDRD.f09_g16.0%s.cam.h0.TREFHT.200601-208012.nc" % i)
        f3 = nc.Dataset("b.e11.BRCP85C5CNBDRD.f09_g16.0%s.cam.h0.TREFHT.208101-210012.nc" % i)

        ff_set[:, i-2] = np.concatenate((
            np.average(f1.variables["TREFHT"][:, lat1:lat2, lon1:lon2], axis=(1, 2)),
            np.average(f2.variables["TREFHT"][:, lat1:lat2, lon1:lon2], axis=(1, 2)),
            np.average(f3.variables["TREFHT"][:, lat1:lat2, lon1:lon2], axis=(1, 2))
            )) - 273
        f1.close()
        f2.close()
        f3.close()
    else:
        f1 = nc.Dataset("b.e11.B20TRC5CNBDRD.f09_g16.0%s.cam.h0.TREFHT.192001-200512.nc" % i)
        f2 = nc.Dataset("b.e11.BRCP85C5CNBDRD.f09_g16.0%s.cam.h0.TREFHT.200601-210012.nc" % i)

        ff_set[:, i-2] = np.concatenate((
            np.average(f1.variables["TREFHT"][:, lat1:lat2, lon1:lon2], axis=(1, 2)),
            np.average(f2.variables["TREFHT"][:, lat1:lat2, lon1:lon2], axis=(1, 2))
            )) - 273
        f1.close()
        f2.close()
    print(i, end=" ")

print("FF 1850 run")
ff_1850 = np.average(nc.Dataset("b.e11.B20TRC5CNBDRD.f09_g16.001.cam.h0.TREFHT.185001-200512.nc").variables["TREFHT"][:, lat1:lat2, lon1:lon2], axis=(1, 2)) - 273

# Control
print("")
print("Control")
for i in range(4, 22):
    if i < 10:
        f = nc.Dataset("b.e11.B1850C5CN.f09_g16.005.cam.h0.TREFHT.0%s0001-0%s9912.nc" % (i, i))
    elif i != 21:
        f = nc.Dataset("b.e11.B1850C5CN.f09_g16.005.cam.h0.TREFHT.%s0001-%s9912.nc" % (i, i))
    else:
        f = nc.Dataset("b.e11.B1850C5CN.f09_g16.005.cam.h0.TREFHT.210001-220012.nc")

    ctl_temp = np.average(f.variables["TREFHT"][:, lat1:lat2, lon1:lon2],
                          axis=(1, 2))-273
    if i == 4:
        ctl = ctl_temp
    else:
        ctl = np.concatenate((ctl, ctl_temp))
    print(i, end=" ")
    f.close()

os.chdir("/Volumes/Extreme SSD/science_research/large_ensemble/CESM1.1.LE_SF/TREFHT/")

ghg_set = np.zeros((1932, 20))
print("")
print("Greenhouse gasses")
for i in range(1, 21):
    if i < 10:
        f1 = nc.Dataset("b.e11.B20TRLENS_RCP85.f09_g16.xghg.00%s.cam.h0.TREFHT.192001-200512.nc" % i)
        f2 = nc.Dataset("b.e11.B20TRLENS_RCP85.f09_g16.xghg.00%s.cam.h0.TREFHT.200601-208012.nc" % i)
    else:
        f1 = nc.Dataset("b.e11.B20TRLENS_RCP85.f09_g16.xghg.0%s.cam.h0.TREFHT.192001-200512.nc" % i)
        f2 = nc.Dataset("b.e11.B20TRLENS_RCP85.f09_g16.xghg.0%s.cam.h0.TREFHT.200601-208012.nc" % i)

    ghg_set[:, i-1] = np.concatenate((
        np.average(f1.variables["TREFHT"][:, lat1:lat2, lon1:lon2], axis=(1, 2)),
        np.average(f2.variables["TREFHT"][:, lat1:lat2, lon1:lon2], axis=(1, 2))
        )) - 273
    print(i, end=" ")
    f1.close()
    f2.close()

# Aerosol Emissions
aer_set = np.zeros((1932, 20))
print("")
print("Aerosols")
for i in range(1, 21):
    if i < 10:
        f1 = nc.Dataset("b.e11.B20TRLENS_RCP85.f09_g16.xaer.00%s.cam.h0.TREFHT.192001-200512.nc" % i)
        f2 = nc.Dataset("b.e11.B20TRLENS_RCP85.f09_g16.xaer.00%s.cam.h0.TREFHT.200601-208012.nc" % i)
    else:
        f1 = nc.Dataset("b.e11.B20TRLENS_RCP85.f09_g16.xaer.0%s.cam.h0.TREFHT.192001-200512.nc" % i)
        f2 = nc.Dataset("b.e11.B20TRLENS_RCP85.f09_g16.xaer.0%s.cam.h0.TREFHT.200601-208012.nc" % i)

    aer_set[:, i-1] = np.concatenate((
        np.average(f1.variables["TREFHT"][:, lat1:lat2, lon1:lon2], axis=(1, 2)),
        np.average(f2.variables["TREFHT"][:, lat1:lat2, lon1:lon2], axis=(1, 2))
        )) - 273
    print(i, end=" ")
    f1.close()
    f2.close()

# Biomass burning
bmb_set = np.zeros((1320, 15))
print("")
print("Biomass")
for i in range(1, 16):
    if i < 10:
        f = nc.Dataset("b.e11.B20TRLENS_RCP85.f09_g16.xbmb.00%s.cam.h0.TREFHT.192001-202912.nc" % i)
    else:
        f = nc.Dataset("b.e11.B20TRLENS_RCP85.f09_g16.xbmb.0%s.cam.h0.TREFHT.192001-202912.nc" % i)
    bmb_set[:, i-1] = np.average(f.variables["TREFHT"][:, lat1:lat2, lon1:lon2],
                                 axis=(1, 2))-273
    print(i, end=" ")
    f.close()

# Land use/cover
luc_set = np.zeros((1320, 5))
print("")
print("Land use/cover")
for i in range(1, 6):
    f = nc.Dataset("b.e11.B20TRLENS_RCP85.f09_g16.xlulc.00%s.cam.h0.TREFHT.192001-202912.nc" % i)
    luc_set[:, i-1] = np.average(f.variables["TREFHT"][:, lat1:lat2, lon1:lon2],
                                 axis=(1, 2))-273
    print(i, end=" ")
    f.close()

# Fixed O3
ozo_set = np.zeros((612, 10))
print("")
print("Ozone")
for i in range(0, 10):
    f = nc.Dataset("b.e11.B20LE_fixedO3_00%s.cam.h0.TREFHT.195501-200512.nc" % i)
    ozo_set[:, i] = np.average(f.variables["TREFHT"][:, lat1:lat2, lon1:lon2],
                               axis=(1, 2))-273
    print(i, end=" ")
    f.close()

os.chdir("/Volumes/Extreme SSD/science_research/large_ensemble/CESM_LE/TREFHT/")

# FF OIC
print("")
print("OIC")
oic_set = np.zeros((960, 10))
for i in range(1, 11):
    if i == 1:
        f = nc.Dataset("b.e11.B20TRC5CNBDRD.f09_g16.OIC.001d.cam.h0.TREFHT.185001-199912.nc")
        oic_set[:, i-1] = np.average(f.variables["TREFHT"][840:, lat1:lat2, lon1:lon2],
                                     axis=(1, 2))-273
    elif i <= 9:
        f = nc.Dataset("b.e11.B20TRC5CNBDRD.f09_g16.OIC.00%s.cam.h0.TREFHT.192001-199912.nc" % i)
        oic_set[:, i-1] = np.average(f.variables["TREFHT"][:, lat1:lat2, lon1:lon2],
                                     axis=(1, 2))-273
    else:
        f = nc.Dataset("b.e11.B20TRC5CNBDRD.f09_g16.OIC.010.cam.h0.TREFHT.192001-199912.nc")
        oic_set[:, i-1] = np.average(f.variables["TREFHT"][:, lat1:lat2, lon1:lon2],
                                     axis=(1, 2))-273
    print(i, end=" ")
    f.close()
    
oic_1850 = np.average(nc.Dataset("b.e11.B20TRC5CNBDRD.f09_g16.OIC.001d.cam.h0.TREFHT.185001-199912.nc").variables["TREFHT"][:, lat1:lat2, lon1:lon2], axis=(1, 2)) - 273

# %%
f = nc.Dataset("b.e11.B20TRC5CNBDRD.f09_g16.001.cam.h0.TREFHT.185001-200512.nc")
lat = f.variables["lat"][:]
lon = f.variables["lon"][:]

# %%
os.chdir('/Users/bengoldman/ENSO-amplitude/Data')

np.savetxt("lat.csv", lat)
np.savetxt("lon.csv", lon)
np.savetxt("ff_set.csv", ff_set)
np.savetxt("ff_1850.csv", ff_1850)
np.savetxt("ctl.csv", ctl)
np.savetxt("ghg_set.csv", ghg_set)
np.savetxt("aer_set.csv", aer_set)
np.savetxt("bmb_set.csv", bmb_set)
np.savetxt("luc_set.csv", luc_set)
np.savetxt("ozo_set.csv", ozo_set)
np.savetxt("oic_set.csv", oic_set)
np.savetxt("oic_1850.csv", oic_1850)
