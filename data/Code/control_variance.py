import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats, signal
from matplotlib import gridspec
from math import sqrt
from random import randint
import os
from matplotlib import cm

from helpers import *
from variance import *

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

fig = plt.figure(figsize=(10, 10))

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
fig.savefig("1.png")


# %%
ctl_var_reshape = ctl_var[:-12].reshape(1800, 12)
ctl_var_ann = np.mean(ctl_var_reshape, axis=1)[750:]
ctl_amoc_750 = ctl_amoc[750:]

ctl_var_amoc_2 = []
for i in range(1050):
    if ctl_amoc_750[i] <= ctl_amoc_mean - ctl_amoc_sd*2:
        ctl_var_amoc_2.append(ctl_var_ann[i])
ctl_var_amoc_2[:]

ctl_var_amoc_2_ = []
for i in range(1050):
    if ctl_amoc_750[i] >= ctl_amoc_mean + ctl_amoc_sd*2:
        ctl_var_amoc_2_.append(ctl_var_ann[i])

ctl_var_amoc_1 = []
for i in range(1050):
    if ctl_amoc_750[i] <= ctl_amoc_mean - ctl_amoc_sd:
        ctl_var_amoc_1.append(ctl_var_ann[i])

ctl_var_amoc_1_ = []
for i in range(1050):
    if ctl_amoc_750[i] >= ctl_amoc_mean + ctl_amoc_sd:
        ctl_var_amoc_1_.append(ctl_var_ann[i])

# %%
ctl_var_amoc_2_pdf = stats.gaussian_kde(ctl_var_amoc_2).evaluate(x)
ctl_var_amoc_2_pdf_ = stats.gaussian_kde(ctl_var_amoc_2_).evaluate(x)
ctl_var_amoc_1_pdf = stats.gaussian_kde(ctl_var_amoc_1).evaluate(x)
ctl_var_amoc_1_pdf_ = stats.gaussian_kde(ctl_var_amoc_1_[:-2]).evaluate(x)


# %%
ctl_var_amo_2 = []
for i in range(21600):
    if (ctl_amo[i] <= ctl_amo_mean - ctl_amo_sd*2) and ~np.isnan(ctl_var[i]):
        ctl_var_amo_2.append(ctl_var[i])

ctl_var_amo_2_ = []
for i in range(21600):
    if (ctl_amo[i] >= ctl_amo_mean + ctl_amo_sd*2) and ~np.isnan(ctl_var[i]):
        ctl_var_amo_2_.append(ctl_var[i])

ctl_var_amo_1 = []
for i in range(21600):
    if (ctl_amo[i] <= ctl_amo_mean - ctl_amo_sd) and ~np.isnan(ctl_var[i]):
        ctl_var_amo_1.append(ctl_var[i])

ctl_var_amo_1_ = []
for i in range(21600):
    if (ctl_amo[i] >= ctl_amo_mean + ctl_amo_sd) and ~np.isnan(ctl_var[i]):
        ctl_var_amo_1_.append(ctl_var[i])

# %%
ctl_var_amo_2_pdf = stats.gaussian_kde(ctl_var_amo_2).evaluate(x)
ctl_var_amo_2_pdf_ = stats.gaussian_kde(ctl_var_amo_2_).evaluate(x)
ctl_var_amo_1_pdf = stats.gaussian_kde(ctl_var_amo_1).evaluate(x)
ctl_var_amo_1_pdf_ = stats.gaussian_kde(ctl_var_amo_1_[:-2]).evaluate(x)

# %%
fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True, figsize=size2)
ax1.plot(x, ctl_var_amoc_1_pdf)
ax1.plot(x, ctl_var_amoc_1_pdf_)
ax1.plot(x, ctl_var_amoc_2_pdf)
ax1.plot(x, ctl_var_amoc_2_pdf_)
ax1.legend([u"AMOC < \u03C3", u"AMOC > \u03C3", u"AMOC < 2\u03C3", u"AMOC > 2\u03C3"])
ax1.set_ylabel("Frequency")
figlett(ax1, "a) AMOC")

ax2.plot(x, ctl_var_amo_1_pdf)
ax2.plot(x, ctl_var_amo_1_pdf_)
ax2.plot(x, ctl_var_amo_2_pdf)
ax2.plot(x, ctl_var_amo_2_pdf_)
ax2.legend([u"AMO < \u03C3", u"AMO > \u03C3", u"AMO < 2\u03C3", u"AMO > 2\u03C3"])
figlett(ax2, "b) AMC")
ax2.set_ylabel("Frequency")
ax2.set_xlabel("Variance")

fig.tight_layout()
fig.savefig("17.pdf", format="pdf")

