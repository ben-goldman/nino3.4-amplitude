#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 11:00:38 2020

@author: bengoldman
"""

import numpy as np
import netCDF4 as nc
import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from math import sqrt
from random import randint


# %%


os.chdir('/Users/bengoldman/ENSO-amplitude/Data')

ctl_cvdp = nc.Dataset("/Volumes/Extreme SSD/science_research/cvdp_data/CESM1_LENS_Coupled_Control.cvdp_data.401-2200.nc")
ctl_amoc = ctl_cvdp.variables["amoc_timeseries_ann"][:]
ctl_amo = ctl_cvdp.variables["amo_timeseries_mon"][:]

np.savetxt("ctl_amoc.csv", ctl_amoc)
np.savetxt("ctl_amo.csv", ctl_amo)
