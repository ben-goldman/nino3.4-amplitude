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
