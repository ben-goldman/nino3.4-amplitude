#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 14:01:34 2020

@author: bengoldman
"""
# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats, signal
from matplotlib import gridspec
from math import sqrt
from random import randint
import os
from matplotlib import cm
import sys
from helpers import *

# %%
from variance import *

# %%
os.chdir("../Data")

ctl = np.loadtxt("ctl.csv")
ff_set = np.loadtxt("ff_set.csv")
ff_1850 = np.loadtxt("ff_1850.csv")
ghg_set = np.loadtxt("ghg_set.csv")
aer_set = np.loadtxt("aer_set.csv")
bmb_set = np.loadtxt("bmb_set.csv")
luc_set = np.loadtxt("luc_set.csv")
ozo_set = np.loadtxt("ozo_set.csv")
oic_set = np.loadtxt("oic_set.csv")
oic_1850 = np.loadtxt("oic_1850.csv")
ctl_amoc = np.loadtxt("ctl_amoc.csv")
ctl_amo = np.loadtxt("ctl_amo.csv")
lat = np.loadtxt("lat.csv")
lon = np.loadtxt("lon.csv")
lon1 = np.loadtxt("lon1.csv")
depth = np.loadtxt("depth.csv")

# %%
os.chdir('/Users/bengoldman/ENSO-amplitude/Figures')

# %%
ctl_var = pd.DataFrame(ctl).rolling(240, center=True).var().to_numpy()[:, 0]
ff_var_set = pd.DataFrame(ff_set).rolling(240, center=True).var().to_numpy()
ff_1850_var = pd.DataFrame(ff_1850).rolling(240, center=True).var().to_numpy()
ghg_var_set = pd.DataFrame(ghg_set).rolling(240, center=True).var().to_numpy()
aer_var_set = pd.DataFrame(aer_set).rolling(240, center=True).var().to_numpy()
bmb_var_set = pd.DataFrame(bmb_set).rolling(240, center=True).var().to_numpy()
luc_var_set = pd.DataFrame(luc_set).rolling(240, center=True).var().to_numpy()
ozo_var_set = pd.DataFrame(ozo_set).rolling(240, center=True).var().to_numpy()
oic_var_set = pd.DataFrame(oic_set).rolling(240, center=True).var().to_numpy()
oic_1850_var = pd.DataFrame(oic_1850).rolling(240, center=True).var().to_numpy()

# %%
ff_var_mean = np.mean(ff_var_set, axis=1)
ghg_var_mean = np.mean(ghg_var_set, axis=1)
aer_var_mean = np.mean(aer_var_set, axis=1)
bmb_var_mean = np.mean(bmb_var_set, axis=1)
luc_var_mean = np.mean(luc_var_set, axis=1)
ozo_var_mean = np.mean(ozo_var_set, axis=1)
oic_var_mean = np.mean(oic_var_set, axis=1)

ff_var_se = stats.sem(ff_var_set, axis=1)
ghg_var_se = stats.sem(ghg_var_set, axis=1)
aer_var_se = stats.sem(aer_var_set, axis=1)
bmb_var_se = stats.sem(bmb_var_set, axis=1)
luc_var_se = stats.sem(luc_var_set, axis=1)
ozo_var_se = stats.sem(ozo_var_set, axis=1)
oic_var_se = stats.sem(oic_var_set, axis=1)

ctl_mean = np.nanmean(ctl_var)
ctl_sd = np.nanstd(ctl_var)
ctl_mean_ = np.linspace(ctl_mean, ctl_mean, 2172)

# CTL AMOC/AMO is averaged after year 750 to account for drift
ctl_amoc_mean = np.mean(ctl_amoc[750:])
ctl_amoc_sd = np.std(ctl_amoc[750:])

ctl_amo_mean = np.mean(ctl_amo)
ctl_amo_sd = np.std(ctl_amo)

# %%
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

# %%
ctl_var_nan = ctl_var[~np.isnan(ctl_var)]

x = np.linspace(0.7, 2, 500)

ctl_var_div_20 = np.zeros((1000, 20))
for i in range(20):
    ctl_var_div_20[:, i] = ctl_var_nan[i*1000:(i+1)*1000]

ctl_var_div_10 = np.zeros((2000, 10))
for i in range(10):
    ctl_var_div_10[:, i] = ctl_var_nan[i*2000:(i+1)*2000]

ctl_var_div_5 = np.zeros((4000, 5))
for i in range(5):
    ctl_var_div_5[:, i] = ctl_var_nan[i*4000:(i+1)*4000]

ctl_var_div_20_pdf = np.zeros((500, 20))
for i in range(20):
    ctl_var_div_20_pdf[:, i] = stats.gaussian_kde(ctl_var_div_20[:, i]).evaluate(x)

ctl_var_div_10_pdf = np.zeros((500, 10))
for i in range(10):
    ctl_var_div_10_pdf[:, i] = stats.gaussian_kde(ctl_var_div_10[:, i]).evaluate(x)

ctl_var_div_5_pdf = np.zeros((500, 5))
for i in range(5):
    ctl_var_div_5_pdf[:, i] = stats.gaussian_kde(ctl_var_div_5[:, i]).evaluate(x)

ctl_var_pdf = stats.gaussian_kde(ctl_var_nan).evaluate(x)

# %%
gs = gridspec.GridSpec(20, 3)

fig = plt.figure(figsize=size1)

for i in range(20):
    ax = fig.add_subplot(gs[i, 0])
    ax.plot(x, ctl_var_div_20_pdf[:, i])
#    ax.set_xticklabels([])

for i in range(10):
    ax = fig.add_subplot(gs[2*i:2*i+2, 1])
    ax.plot(x, ctl_var_div_10_pdf[:, i])

for i in range(5):
    ax = fig.add_subplot(gs[4*i:4*i+4, 2])
    ax.plot(x, ctl_var_div_5_pdf[:, i])

#fig.tight_layout(pad=.1)
fig.savefig("1.pdf", format="pdf")

# %%
fig, (axx) = plt.subplots(3, 2, sharex='col', sharey="row", figsize=size1)
fig.subplots_adjust(wspace=.1)

envelope(axx[0, 0], date_2172, ff_var_mean, ff_var_se, "C0")

envelope(axx[0, 1], date_1932, ghg_var_mean, ghg_var_se, "C1")

envelope(axx[1, 0], date_1932, aer_var_mean, aer_var_se, "C2")

envelope(axx[1, 1], date_1320, bmb_var_mean, bmb_var_se, "C3")

envelope(axx[2, 0], date_1320, luc_var_mean, luc_var_se, "C4")

envelope(axx[2, 1], date_612, ozo_var_mean, ozo_var_se, "C5")

axx[2, 0].set_xlabel("Date")
axx[2, 1].set_xlabel("Date")
axx[0, 0].set_ylabel("Variance")
axx[1, 0].set_ylabel("Variance")
axx[2, 0].set_ylabel("Variance")


sizes = np.array(((35, 15), (20, 5), (20, 10)))
letts = np.array((("a) FF", "b) xGHG"), ("c) xAER", "d) xBMB"), ("e) xLULC", "f) xO3")))
for m in range(3):
    for n in range(2):
        axx[m, n].hlines(ctl_mean, 1920, 2100)
        axx[m, n].fill_between(date_2172, ctl_mean+ctl_sd/sqrt(sizes[m, n]), ctl_mean-ctl_sd/sqrt(sizes[m, n]), color="k", alpha=.1)
        axx[m, n].fill_between(date_2172, ctl_mean+2*ctl_sd/sqrt(sizes[m, n]), ctl_mean-2*ctl_sd/sqrt(sizes[m, n]), color="k", alpha=.1)
        axx[m, n].fill_between(date_2172, ctl_mean+3*ctl_sd/sqrt(sizes[m, n]), ctl_mean-3*ctl_sd/sqrt(sizes[m, n]), color="k", alpha=.1)
        figlett(axx[m, n], letts[m, n])
        axx[m, n].set_ylim(1,1.8)

fig.tight_layout()
fig.subplots_adjust()
fig.savefig("variance_1.pdf")

# %%

fig = plt.figure(figsize=size1)
ax = fig.add_subplot(111)

envelope(ax, date_2172, ff_var_mean, ff_var_se, col="C0")
ax.hlines(ctl_mean, 1920, 2100, color="k")
ax.fill_between(date_2172, ctl_mean+ctl_sd/sqrt(35), ctl_mean-ctl_sd/sqrt(35), color="k", alpha=.1)
ax.fill_between(date_2172, ctl_mean+2*ctl_sd/sqrt(35), ctl_mean-2*ctl_sd/sqrt(35), color="k", alpha=.1)
ax.fill_between(date_2172, ctl_mean+3*ctl_sd/sqrt(35), ctl_mean-3*ctl_sd/sqrt(35), color="k", alpha=.1)

ax.set_xlabel("Date")
ax.set_ylabel("Variance")


fig.tight_layout(pad=0)
plt.savefig("variance_2.pdf")

plt.show()

# %%

fig = plt.figure(figsize=size1)
ax = fig.add_subplot(111)

ax.plot(date_2172, ff_var_set, color="C0", alpha=.3)
ax.set_ylabel("Variance")
ax.set_xlabel("Date")
fig.tight_layout()

plt.savefig("variance_3.pdf")
plt.show()

# %%
fig = plt.figure(figsize=size1)
ax = fig.add_subplot(111)

envelope(ax, date_2172, ff_var_mean, ff_var_se, col="C0")
envelope(ax, date_960, oic_var_mean, oic_var_se, col="r")
ax.plot(date_1872, ff_1850_var, color="b")
ax.plot(date_1800, oic_1850_var, color="g")

ax.hlines(ctl_mean, 1920, 2100)
ax.fill_between(date_2172, ctl_mean+ctl_sd/sqrt(35), ctl_mean-ctl_sd/sqrt(35), color="k", alpha=.1)
ax.fill_between(date_2172, ctl_mean+2*ctl_sd/sqrt(35), ctl_mean-2*ctl_sd/sqrt(35), color="k", alpha=.1)
ax.fill_between(date_2172, ctl_mean+3*ctl_sd/sqrt(35), ctl_mean-3*ctl_sd/sqrt(35), color="k", alpha=.1)

ax.set_xlabel("Date")
ax.set_ylabel("Variance")

ax.legend(["LENS","OIC", "LENS model 1", "OIC model 1"])
ax.set_ylim(0.9, 2.0)

fig.tight_layout()
fig.subplots_adjust(top=.94)
fig.savefig("3.pdf", format="pdf")

# %%

print("\n FF")
ff_bs = np.zeros((2172, 1000))
for i in range(1000):
    ff_bs[:, i] = -(ff_var_set[:, randint(0, 34-1)] - ff_var_set[:, randint(0, 34-1)])

print("\n GHG")
ghg_bs = np.zeros((1932, 1000))
for i in range(1000):
    ghg_bs[:, i] = -(ghg_var_set[:, randint(0, 20-1)] - ff_var_set[:1932, randint(0, 34-1)])

print("\n AER")
aer_bs = np.zeros((1932, 1000))
for i in range(1000):
    aer_bs[:, i] = -(aer_var_set[:, randint(0, 20-1)] - ff_var_set[:1932, randint(0, 34-1)])

print("\n BMB")
bmb_bs = np.zeros((1320, 1000))
for i in range(1000):
    bmb_bs[:, i] = -(bmb_var_set[:, randint(0, 15-1)] - ff_var_set[:1320, randint(0, 34-1)])

print("\n LUC")
luc_bs = np.zeros((1320, 1000))
for i in range(1000):
    luc_bs[:, i] = -(luc_var_set[:, randint(0, 5-1)] - ff_var_set[:1320, randint(0, 34-1)])

print("\n OZO")
ozo_bs = np.zeros((612, 1000))
for i in range(1000):
    ozo_bs[:, i] = -(ozo_var_set[:, randint(0, 10-1)] - ff_var_set[420:1032, randint(0, 34-1)])

ff_1850_var_centd = ff_1850_var-np.nanmean(ff_1850_var)

# %%
ff_bs_mean = np.mean(ff_bs, axis=1)
ghg_bs_mean = np.nanmean(ghg_bs, axis=1)
aer_bs_mean = np.mean(aer_bs, axis=1)
bmb_bs_mean = np.mean(bmb_bs, axis=1)
luc_bs_mean = np.mean(luc_bs, axis=1)
ozo_bs_mean = np.mean(ozo_bs, axis=1)

ff_bs_se = np.std(ff_bs, axis=1)/sqrt(35)
ghg_bs_se = np.std(ghg_bs, axis=1)/sqrt(20)
aer_bs_se = np.std(aer_bs, axis=1)/sqrt(20)
bmb_bs_se = np.std(bmb_bs, axis=1)/sqrt(15)
luc_bs_se = np.std(luc_bs, axis=1)/sqrt(5)
ozo_bs_se = np.std(ozo_bs, axis=1)/sqrt(10)

bs_sum_mean = ghg_bs_mean.copy()
bs_sum_mean[120:-120] += aer_bs_mean[120:-120]
bs_sum_mean[120:1200] += bmb_bs_mean[120:-120]
bs_sum_mean[120:1200] += luc_bs_mean[120:-120]
print(bs_sum_mean.shape)
bs_sum_mean[540:912] += ozo_bs_mean[120:-120]



# %%
letts = np.array((("a) +GHG", "b) +AER"), ("c) +BMB", "d) +LULC"), ("e) +O3", "f) Sum")))

fig, (axx) = plt.subplots(3, 2, sharex='col', sharey="row", figsize=size3)


envelope(axx[0, 0], date_1932, ghg_bs_mean, ghg_bs_se, "C1")

envelope(axx[0, 1], date_1932, aer_bs_mean, aer_bs_se, "C2")

envelope(axx[1, 0], date_1320, bmb_bs_mean, bmb_bs_se, "C3")

envelope(axx[1, 1], date_1320, luc_bs_mean, luc_bs_se, "C4")

envelope(axx[2, 0], date_612, ozo_bs_mean, ozo_bs_se, "C5")

(x, y, err) = (date_2172, ff_var_mean-np.nanmean(ff_var_mean), ff_var_se)
line, = axx[2, 1].plot(x, y, color="C0")
axx[2, 1].fill_between(x, y-err, y+err, alpha=.2, color="C0")

line2, = axx[2, 1].plot(date_1932, bs_sum_mean, color="C1")
axx[2, 1].legend([line, line2], ["FF", "Sum"], fontsize="small")

axx[2, 0].set_xlabel("Date")
axx[2, 1].set_xlabel("Date")
axx[0, 0].set_ylabel("Variance")
axx[1, 0].set_ylabel("Variance")
axx[2, 0].set_ylabel("Variance")

for m in range(3):
    for n in range(2):
        axx[m, n].set_ylim(-.5,.5)
        axx[m, n].set_xlim(1920, 2100)
        figlett(axx[m, n], letts[m, n])
        axx[m, n].hlines(0, 1900, 2100, alpha=.5, linewidth=1, color="k")

fig.tight_layout(pad=0)
fig.savefig("bootstrap_1.pdf", format="pdf")

plt.show()

# %%

fig = plt.figure(figsize=size1)
ax = fig.add_subplot(111)

envelope(ax, date_2172, ff_bs_mean, ff_bs_se, "C0")

envelope(ax, date_1932, ghg_bs_mean, ghg_bs_se, "C1")

envelope(ax, date_1932, aer_bs_mean, aer_bs_se, "C2")

envelope(ax, date_1320, bmb_bs_mean, bmb_bs_se, "C3")

envelope(ax, date_1320, luc_bs_mean, luc_bs_se, "C4")

envelope(ax, date_612, ozo_bs_mean, ozo_bs_se, "C5")

ax.set_xlabel("Date")
ax.set_ylabel("Variance")

ax.legend(["FF", "GHG", "AER", "BMB", "LULC", "fixedO3"])

fig.tight_layout()
fig.savefig("5.pdf", format="pdf")

# %%
fig = plt.figure(figsize=size1)
ax = fig.add_subplot(111)

envelope(ax, date_1932, ghg_bs_mean, ghg_bs_se, "C1")

envelope(ax, date_1932, aer_bs_mean, aer_bs_se, "C2")

ax.set_xlabel("Date")
ax.set_ylabel("Variance")

ax.legend(["GHG", "AER"])
ax.hlines(0, 1920, 2080, color="k")

fig.tight_layout()
fig.subplots_adjust()
fig.savefig("bootstrap_2.pdf", format="pdf")

# %%
fig = plt.figure(figsize=size1)
ax = fig.add_subplot(111)

ax.set_title("Mean of Bootstrapped Samples")

ax.hist(np.nanmean(ff_bs, axis=0), bins=35, alpha=.7, label="Fulsl forcing")
ax.hist(np.nanmean(ghg_bs, axis=0), bins=35, alpha=.7, label="Greenhouse Gasses")
ax.hist(np.nanmean(aer_bs, axis=0), bins=35, alpha=.7, label="Aerosols")

ax.set_xlabel('Variance')
ax.set_ylabel('Frequency')
ax.legend()

fig.tight_layout()
fig.subplots_adjust(top=.94)
fig.savefig("7.pdf", format="pdf")

# %%
fig = plt.figure(figsize=size1)
ax = fig.add_subplot(111)

ax.set_title("Mean of Bootstrapped Samples, 1960-2100")

ax.hist(np.nanmean(ff_bs[480:], axis=0), bins=35, alpha=.7, label="Full forcing")
ax.hist(np.nanmean(ghg_bs[480:], axis=0), bins=35, alpha=.7, label="Greenhouse Gasses")
ax.hist(np.nanmean(aer_bs[480:], axis=0), bins=35, alpha=.7, label="Aerosols")

ax.set_xlabel('Variance')
ax.set_ylabel('Frequency')
ax.legend()

fig.tight_layout()
fig.subplots_adjust(top=.94)
fig.savefig("8.pdf", format="pdf")

# %%
fig = plt.figure(figsize=size1)
ax = fig.add_subplot(111)

ax.set_title("Nino 3.4 20-Year Variance, Bootstrapped Samples, \n With ensemble members(not bootstrapped)")

ax.plot(date_2172, ff_bs_mean, color="C0", label="Full Forcing")
ax.fill_between(date_2172, ff_bs_mean-ff_bs_se, ff_bs_mean+ff_bs_se, alpha=.3, color="C0")

ax.plot(date_1932, ghg_bs_mean, color="C1", label="Greenhouse Gasses")
ax.fill_between(date_1932, ghg_bs_mean-ghg_bs_se, ghg_bs_mean+ghg_bs_se, alpha=.3, color="C1")
plt.plot(date_1932, ff_var_set[:1932, :20]-ghg_var_set, color="C1", alpha=.2)

ax.plot(date_1932, aer_bs_mean, color="C2", label="Aerosols")
ax.fill_between(date_1932, aer_bs_mean-aer_bs_se, aer_bs_mean+aer_bs_se, alpha=.3, color="C2")
plt.plot(date_1932, ff_var_set[:1932, :20]-aer_var_set, color="C2", alpha=.2)

ax.set_xlabel("Date")
ax.set_ylabel("Variance")

ax.legend()

fig.tight_layout()
fig.subplots_adjust(top=.90)
fig.savefig("9.pdf", format="pdf")

# %%
# fig = plt.figure(figsize=size1)
# ax = fig.add_subplot(111)

# ax.set_title("Nino 3.4 20-Year Variance, Bootstrapped Samples 1920-1940")

# ax.plot(date_2172, ff_bs_mean, color="C0", label="Full Forcing")
# ax.fill_between(date_2172, ff_bs_mean-ff_bs_se, ff_bs_mean+ff_bs_se, alpha=.2, color="C0")

# ax.plot(date_1932, ghg_bs_mean, color="C1", label="Greenhouse Gasses")
# ax.fill_between(date_1932, ghg_bs_mean-ghg_bs_se, ghg_bs_mean+ghg_bs_se, alpha=.2, color="C1")

# ax.plot(date_1932, aer_bs_mean, color="C2", label="Aerosols")
# ax.fill_between(date_1932, aer_bs_mean-aer_bs_se, aer_bs_mean+aer_bs_se, alpha=.2, color="C2")

# ax.set_xlim(1920,1940)

# ax.legend()

# %%
fig = plt.figure(figsize=size1)
ax = fig.add_subplot(111)

ax.set_title("Mean of Bootstrapped Samples, 1920-1940")

ax.hist(np.nanmean(ff_bs[:240], axis=0), bins=35, alpha=.7, label="Full forcing")
ax.hist(np.nanmean(ghg_bs[:240], axis=0), bins=35, alpha=.7, label="Greenhouse Gasses")
ax.hist(np.nanmean(aer_bs[:240], axis=0), bins=35, alpha=.7, label="Aerosols")

ax.set_xlabel('Variance')
ax.set_ylabel('Frequency')
ax.legend()

fig.tight_layout()
fig.subplots_adjust(top=.94)
fig.savefig("10.pdf", format="pdf")

# %%
fig = plt.figure(figsize=size1)
ax = fig.add_subplot(111)

fig.suptitle("Nino 3.4 20-Year Variance, Bootstrapped Samples, \n With ensemble members GHG only")

ax.plot(date_2172, ff_bs_mean, color="C0", label="Full Forcing")
ax.fill_between(date_2172, ff_bs_mean-ff_bs_se, ff_bs_mean+ff_bs_se, alpha=.3, color="C0")

ax.plot(date_1932, ff_var_set[:1932, 0]-ghg_var_set[:, 0], color="g", alpha=.2, label="Non-bootstrapped ensemble members")
ax.plot(date_1932, ff_var_set[:1932, 1:20]-ghg_var_set[:, 1:20], color="g", alpha=.2)

ax.plot(date_1932, ghg_bs[:, 0], color="C1", alpha=.2, label="bootstrapped ensemble members")
ax.plot(date_1932, ghg_bs[:, 1::20], color="C1", alpha=.2)
ax.plot(date_1932, ghg_bs_mean, color="k", label="bootstrapped mean")

ax.set_xlabel("Date")
ax.set_ylabel("Variance")

ax.legend()

fig.tight_layout()
fig.subplots_adjust(top=.90)
fig.savefig("11.pdf", format="pdf")

# %%
fig = plt.figure(figsize=size1)
ax = fig.add_subplot(111)
ax.plot(date_2172, ff_var_set, color="C0", alpha=.3)
ax.set_xlabel("Date")
ax.set_ylabel("Variance")

fig.tight_layout()
fig.savefig("12.pdf", format="pdf")

# %%
fig = plt.figure(figsize=size1)
ax = fig.add_subplot(111)

ax.plot(date_ctl_1800, ctl_amoc)

ax.hlines(ctl_amoc_mean, 400, 2200)
ax.fill_between(date_ctl_1800, ctl_amoc_mean+ctl_amoc_sd, ctl_amoc_mean-ctl_amoc_sd, color="k", alpha=.1)
ax.fill_between(date_ctl_1800, ctl_amoc_mean+ctl_amoc_sd*2, ctl_amoc_mean-ctl_amoc_sd*2, color="k", alpha=.1)

ax.set_xlabel("Date")
ax.set_ylabel("Variance")
fig.suptitle("Control AMOC index")

fig.tight_layout()
fig.subplots_adjust(top=.94)
fig.savefig("13.pdf", format="pdf")

# %%
fig = plt.figure(figsize=size1)
ax = fig.add_subplot(111)

ax.plot(date_ctl_20600, ctl_amo)

ax.hlines(ctl_amo_mean, 400, 2200)
ax.fill_between(date_ctl_20600, ctl_amo_mean+ctl_amo_sd, ctl_amo_mean-ctl_amo_sd, color="k", alpha=.1)
ax.fill_between(date_ctl_20600, ctl_amo_mean+ctl_amo_sd*2, ctl_amo_mean-ctl_amo_sd*2, color="k", alpha=.1)

ax.set_xlabel("Date")
ax.set_ylabel("Variance")
fig.suptitle("Control AMO index")

fig.tight_layout()
fig.subplots_adjust(top=.94)
fig.savefig("14.pdf", format="pdf")

# %%
fig = plt.figure(figsize=size1)
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()

ax1.plot(date_ctl_1800, ctl_amoc, color="C0")
ax1.hlines(ctl_amoc_mean, 400, 2200)
ax1.fill_between(date_ctl_1800, ctl_amoc_mean+ctl_amoc_sd, ctl_amoc_mean-ctl_amoc_sd, color="k", alpha=.1)
ax1.fill_between(date_ctl_1800, ctl_amoc_mean+ctl_amoc_sd*2, ctl_amoc_mean-ctl_amoc_sd*2, color="k", alpha=.1)
ax1.set_ylabel("AMOC index", color="C0")

ax2.plot(date_ctl_20600, ctl_var[:-12], color="C1")
ax2.set_ylabel("Nino3.4 20-year variance", color="C1")

fig.tight_layout()
fig.subplots_adjust(top=.94)
fig.savefig("15.pdf", format="pdf")

# %%
ctl_var_pt1 = ctl_var[:10800]
ctl_var_pt2 = ctl_var[10800:]
ctl_amo_pt1 = ctl_amo[:10800]
ctl_amo_pt2 = ctl_amo[10800:]

ctl_var_amo_pt1_2 = []
for i in range(10800):
    if (ctl_amo_pt1[i] <= ctl_amo_mean - ctl_amo_sd*2) and ~np.isnan(ctl_var_pt1[i]):
        ctl_var_amo_pt1_2.append(ctl_var_pt1[i])

ctl_var_amo_pt1_2_ = []
for i in range(10800):
    if (ctl_amo_pt1[i] >= ctl_amo_mean + ctl_amo_sd*2) and ~np.isnan(ctl_var_pt1[i]):
        ctl_var_amo_pt1_2_.append(ctl_var_pt1[i])

ctl_var_amo_pt1_1 = []
for i in range(10800):
    if (ctl_amo_pt1[i] <= ctl_amo_mean - ctl_amo_sd) and ~np.isnan(ctl_var_pt1[i]):
        ctl_var_amo_pt1_1.append(ctl_var_pt1[i])

ctl_var_amo_pt1_1_ = []
for i in range(10800):
    if (ctl_amo_pt1[i] >= ctl_amo_mean + ctl_amo_sd) and ~np.isnan(ctl_var_pt1[i]):
        ctl_var_amo_pt1_1_.append(ctl_var_pt1[i])

ctl_var_amo_pt2_2 = []
for i in range(10800):
    if (ctl_amo_pt2[i] <= ctl_amo_mean - ctl_amo_sd*2) and ~np.isnan(ctl_var_pt2[i]):
        ctl_var_amo_pt2_2.append(ctl_var_pt2[i])

ctl_var_amo_pt2_2_ = []
for i in range(10800):
    if (ctl_amo_pt2[i] >= ctl_amo_mean + ctl_amo_sd*2) and ~np.isnan(ctl_var_pt2[i]):
        ctl_var_amo_pt2_2_.append(ctl_var_pt2[i])

ctl_var_amo_pt2_1 = []
for i in range(10800):
    if (ctl_amo_pt2[i] <= ctl_amo_mean - ctl_amo_sd) and ~np.isnan(ctl_var_pt2[i]):
        ctl_var_amo_pt2_1.append(ctl_var_pt2[i])

ctl_var_amo_pt2_1_ = []
for i in range(10800):
    if (ctl_amo_pt2[i] >= ctl_amo_mean + ctl_amo_sd) and ~np.isnan(ctl_var_pt2[i]):
        ctl_var_amo_pt2_1_.append(ctl_var_pt2[i])
# %%
ctl_var_amo_pt1_2_pdf = stats.gaussian_kde(ctl_var_amo_pt1_2).evaluate(x)
ctl_var_amo_pt1_2_pdf_ = stats.gaussian_kde(ctl_var_amo_pt1_2_).evaluate(x)
ctl_var_amo_pt1_1_pdf = stats.gaussian_kde(ctl_var_amo_pt1_1).evaluate(x)
ctl_var_amo_pt1_1_pdf_ = stats.gaussian_kde(ctl_var_amo_pt1_1_).evaluate(x)

ctl_var_amo_pt2_2_pdf = stats.gaussian_kde(ctl_var_amo_pt2_2).evaluate(x)
ctl_var_amo_pt2_2_pdf_ = stats.gaussian_kde(ctl_var_amo_pt2_2_).evaluate(x)
ctl_var_amo_pt2_1_pdf = stats.gaussian_kde(ctl_var_amo_pt2_1).evaluate(x)
ctl_var_amo_pt2_1_pdf_ = stats.gaussian_kde(ctl_var_amo_pt2_1_).evaluate(x)

# %%
fig = plt.figure(figsize=size1)

ax = fig.add_subplot(211)
ax.plot(x, ctl_var_amo_pt1_1_pdf)
ax.plot(x, ctl_var_amo_pt1_1_pdf_)
ax.plot(x, ctl_var_amo_pt1_2_pdf)
ax.plot(x, ctl_var_amo_pt1_2_pdf_)
ax.legend([u"AMO < \u03C3", u"AMO > \u03C3", u"AMO < 2\u03C3", u"AMO > 2\u03C3"])
ax.set_ylabel("Frequency")
ax.set_xlabel("Variance")
ax.set_title("First Half")

ax2 = fig.add_subplot(212)
ax2.plot(x, ctl_var_amo_pt2_1_pdf)
ax2.plot(x, ctl_var_amo_pt2_1_pdf_)
ax2.plot(x, ctl_var_amo_pt2_2_pdf)
ax2.plot(x, ctl_var_amo_pt2_2_pdf_)
ax2.legend([u"AMO < \u03C3", u"AMO > \u03C3", u"AMO < 2\u03C3", u"AMO > 2\u03C3"])
ax2.set_ylabel("Frequency")
ax2.set_xlabel("Variance")
ax2.set_title("Second Half")

fig.suptitle("Control Nino 3.4 20-year variance PDF for various AMO distributions")
figlett(ax, "a")
figlett(ax2, "b")

fig.tight_layout()
fig.subplots_adjust(top=.94)
fig.savefig("18.pdf", format="pdf")

