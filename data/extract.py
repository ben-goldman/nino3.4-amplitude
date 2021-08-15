#!/usr/bin/env python

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import netCDF4 as nc

PATH_FF = "/Volumes/Extreme SSD/DATA/stacked/CESM1/TREFHT/"
PATH_SF = "/Volumes/Extreme SSD/DATA/stacked/CESM1SF/TREFHT/"

FILE_FF = "b.e11.BRCP85C5CNBDRD.f09_g16.all.cam.h0.TREFHT.192001-210012.nc"
FILES_SF = [
    "b.e11.B20TRLENS_RCP85.f09_g16.xghg.all.cam.h0.TREFHT.192001-208012.nc",
    "b.e11.B20TRLENS_RCP85.f09_g16.xaer.all.cam.h0.TREFHT.192001-208012.nc",
    "b.e11.B20TRLENS_RCP85.f09_g16.xbmb.all.cam.h0.TREFHT.192001-202912.nc",
    "b.e11.B20TRLENS_RCP85.f09_g16.xlulc.all.cam.h0.TREFHT.192001-202912.nc"]

nino34 = [[90, 101],
          [152, 192]]


def extract_nino_34(file, nino34 = [[90, 101], [152, 192]]):
    f = nc.Dataset(file)
    nino = f.variables["TREFHT"][:,
                                 :,
                                 nino34[0][0]:nino34[0][1],
                                 nino34[1][0]:nino34[1][1]].mean((2, 3))
    return nino

def get_variance(x, win = 240):
    out = x.rolling(win, center = True).var().to_numpy()[:, 0]
    return out
