
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats, signal
from math import sqrt
from random import randint
import os

# %%

os.chdir('/Users/bengoldman/ENSO-amplitude/Data')
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
