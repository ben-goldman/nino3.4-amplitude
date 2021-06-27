#! /usr/bin/env python3

import netCDF4 as nc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats, signal
from matplotlib import gridspec
from math import sqrt
from random import randint
import os
from matplotlib import cm, colors
import re

lat = np.loadtxt("../Data/lat.csv")
lon = np.loadtxt("../Data/lon.csv")
lon1 = np.loadtxt("../Data/lon1.csv")
lat1 = np.loadtxt("../Data/lat1.csv")
depth = np.loadtxt("../Data/depth.csv")/100

date_2172 = np.linspace(1920, 2100, 2172)
date_1872 = np.linspace(1850, 2005, 1872)
date_1032 = np.linspace(1920, 2005, 1032)
date_1932 = np.linspace(1920, 2080, 1932)
date_1320 = np.linspace(1920, 2029, 1320)
date_612 = np.linspace(1955, 2005, 612)
date_960 = np.linspace(1920, 1999, 960)
date_1800 = np.linspace(1850, 1999, 1800)
date_80 = np.linspace(1920, 1999, 80)
date_ctl_20600 = np.linspace(400, 2200, 21600)
date_ctl_1800 = np.linspace(400, 2200, 1800)


def envelope(ax, x, y, err, col):
    ax.plot(x, y, color=col)
    ax.fill_between(x, y-err, y+err, alpha=.2, color=col)


def figlett(ax, a):
    ax.text(0.01, 0.99, a, transform=ax.transAxes, va='top')

size1 = (4, 3)
size2 = (4, 5)
size3 = (6, 5)
mp = np.ones((400, 3))
mp[21:40] = [.6, .6, .6]
mp[-40:-21] = [.6, .6, .6]
mp[0:20, 0] = np.linspace(0, 1, 20)
mp[0:20, 1] = np.linspace(0, 1, 20)
mp[0:20, 2] = 1
mp[-21:-1, 0] =1
mp[-21:-1, 1] = np.linspace(1, 0, 20)
mp[-21:-1, 2] = np.linspace(1, 0, 20)
cmap = colors.ListedColormap(mp)

mp = np.zeros((2, 4))
mp[1, :] = [1, 1, 1, 1]
mp[0, :] = [1, 1, 1, 0]
bool_white = colors.ListedColormap(mp)

mp = np.zeros((2, 4))
mp[1, :] = [.5, .5, .5, 1]
mp[0, :] = [.5, .5, .5, 0]
bool_gray = colors.ListedColormap(mp)

def correlation_detrended(cs, ts, smooth=360):
    cs_det = cs
    ts_det = ts
    signal.detrend(ts_det[~np.isnan(ts_det)], overwrite_data=True)
    ts_det = pd.DataFrame(ts_det).rolling(smooth, center=True).mean().to_numpy()[:, 0]

    rs = np.zeros_like(cs[0])
    ps = np.zeros_like(cs[0])
    len_cs_slice = len(cs_det[0, :, 0])

    for i in range(len_cs_slice):
        len_cs_i = len(cs_det[0, i, :])
        for j in range(len_cs_i):
            if np.any(np.isnan(cs_det[:, i, j])):
                r, p = (np.nan, np.nan)
            else:
                signal.detrend(cs_det[:, i, j], overwrite_data=True)
                cs_det[:, i, j] = pd.DataFrame(cs_det[:, i, j]).rolling(smooth, center=True).mean().to_numpy()[:, 0]
                offset = int((smooth/2+120))
                r, p = stats.pearsonr(cs_det[offset:-(offset), i, j], ts_det[offset:-(offset)])
            rs[i, j] = r
            ps[i, j] = p
    return (rs, ps)

def three_contours(set1, set2, set3, ov1, ov2, ov3, ov4, ov5, ov6, suptitle, xlabel, xscale, ylabel, yscale):
    cmap = plt.get_cmap('coolwarm')
    norm = colors.Normalize(vmin=-1, vmax=1)
    cf = cm.ScalarMappable(norm=norm, cmap=cmap)

    fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, sharex=True, figsize=size2)
    ax1.contourf(xscale, yscale[:36], set1[:36], 32,  cmap=cmap, vmin=-1, vmax=1)
    ax1.contourf(xscale, yscale[:36], ov1[:36], cmap=bool_white)
    ax1.contourf(xscale, yscale[:36], ov4[:36], cmap=bool_gray)
    ax1.set_ylabel(ylabel)
    ax1.invert_yaxis()
    # ax1.set_yscale("log")
    figlett(ax1, "a) Full forcing")

    ax2.contourf(xscale, yscale[:36], set2[:36], 32, cmap=cmap, vmin=-1, vmax=1)
    ax2.contourf(xscale, yscale[:36], ov2[:36], cmap=bool_white)
    ax2.contourf(xscale, yscale[:36], ov5[:36], cmap=bool_gray)
    ax2.set_ylabel(ylabel)
    ax2.invert_yaxis()
    # ax2.set_yscale("log")
    figlett(ax2, "b) Greenhouse")

    ax3.contourf(xscale, yscale[:36], set3[:36], 32, cmap=cmap, vmin=-1, vmax=1)
    ax3.contourf(xscale, yscale[:36], ov3[:36], cmap=bool_white)
    ax3.contourf(xscale, yscale[:36], ov6[:36], cmap=bool_gray)
    ax3.set_xlabel(xlabel)
    ax3.set_ylabel(ylabel)
    ax3.invert_yaxis()
    # ax3.set_yscale("log")
    figlett(ax3, "c) Aerosols")

    fig.tight_layout()
    fig.subplots_adjust(right=.83)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.03, 0.7])
    fig.colorbar(cf, cax=cbar_ax)
    return fig

def get_ensemble(path, flavor, var):
    os.chdir(path)
    if flavor == 0:

        rex1 = re.compile(r'b\.e11\.[A-Z0-9_]*\.f09_g16\.[a-z]*(\.)?0(0[2-9]|1\d|2[0-9]|3[0123])\.pop\.h\.[A-Z]*\.192001-200512\.nc')
        rex2 = re.compile(r'b\.e11\.[A-Z0-9_]*\.f09_g16\.[a-z]*(\.)?0(0[2-9]|1\d|2[0-9]|3[0123])\.pop\.h\.[A-Z]*\.200601-208012\.nc')
        rex3 = re.compile(r'b\.e11\.[A-Z0-9_]*\.f09_g16\.[a-z]*(\.)?0(0[2-9]|1\d|2[0-9]|3[0123])\.pop\.h\.[A-Z]*\.208101-210012\.nc')
        rex4 = re.compile(r'b\.e11\.[A-Z0-9_]*\.f09_g16\.[a-z]*(\.)?03[45]\.pop\.h\.[A-Z]*\.192001-200512\.nc')
        rex5 = re.compile(r'b\.e11\.[A-Z0-9_]*\.f09_g16\.[a-z]*(\.)?03[45]\.pop\.h\.[A-Z]*\.200601-210012\.nc')

        set1 = [f for f in os.listdir() if rex1.match(f)]
        set2 = [f for f in os.listdir() if rex2.match(f)]
        set3 = [f for f in os.listdir() if rex3.match(f)]
        set4 = [f for f in os.listdir() if rex4.match(f)]
        set5 = [f for f in os.listdir() if rex5.match(f)]
        print(len(set1))
        print(len(set2))
        print(len(set3))
        print(len(set4))
        print(len(set5))
        
        s1 = nc.Dataset(set1[0]).variables[var][:, :, :].shape
        s2 = nc.Dataset(set2[0]).variables[var][:, :, :].shape
        s3 = nc.Dataset(set3[0]).variables[var][:, :, :].shape
        time = s1[0] + s2[0] + s3[0]
        print(s1[0])
        print(s2[0])
        print(s3[0])
        print(time)

        shape = (len(set1) + len(set4), time, s1[1], s1[2])
        print(shape)

        ensemble = np.zeros(shape)

        for i in range(len(set1)):
            f1 = nc.Dataset(set1[i])
            f2 = nc.Dataset(set2[i])
            f3 = nc.Dataset(set3[i])

            v1 = f1.variables[var][:, :, :]
            v2 = f2.variables[var][:, :, :]
            v3 = f3.variables[var][:, :, :]

            v1[v1.mask] = np.nan
            v2[v2.mask] = np.nan
            v3[v3.mask] = np.nan
            ensemble[i, :, :, :] = np.concatenate((v1, v2, v3))

            f1.close()
            f2.close()
            f3.close()

            print(i)

        for i in range(len(set4)):
            f1 = nc.Dataset(set4[i])
            f2 = nc.Dataset(set5[i])

            v1 = f1.variables[var][:, :, :]
            v2 = f2.variables[var][:, :, :]

            v1[v1.mask] = np.nan
            v2[v2.mask] = np.nan
            ensemble[i+32, :, :, :] = np.concatenate((v1, v2))

            f1.close()
            f2.close()
        
    elif flavor == 1:
        rex1 = re.compile(r'b\.e11\.[A-Z0-9_]*\.f09_g16\.[a-z]*(\.)?0(0[1-9]|1\d|2[0-9]|3[0123])\.pop\.h\.[A-Z]*\.192001-200512\.nc')
        rex2 = re.compile(r'b\.e11\.[A-Z0-9_]*\.f09_g16\.[a-z]*(\.)?0(0[1-9]|1\d|2[0-9]|3[0123])\.pop\.h\.[A-Z]*\.200601-208012\.nc')

        set1 = [f for f in os.listdir() if rex1.match(f)]
        set2 = [f for f in os.listdir() if rex2.match(f)]

        s1 = nc.Dataset(set1[0]).variables[var][:, :, :].shape
        s2 = nc.Dataset(set2[0]).variables[var][:, :, :].shape

        time = s1[0] + s2[0]

        shape = (len(set1), time, s1[1], s1[2])

        ensemble = np.zeros(shape)

        for i in range(len(set1)):
            f1 = nc.Dataset(set1[i])
            f2 = nc.Dataset(set2[i])

            v1 = f1.variables[var][:, :, :]
            v2 = f2.variables[var][:, :, :]

            v1[v1.mask] = np.nan
            v2[v2.mask] = np.nan
            ensemble[i, :, :, :] = np.concatenate((v1, v2))

            f1.close()
            f2.close()
    
    return ensemble
