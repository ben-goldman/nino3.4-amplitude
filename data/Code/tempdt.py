from helpers import *
from variance import ff_var_mean, ghg_var_mean, aer_var_mean

ff_tempdt_avg = np.load("../Data/ff_tempdt_average.npy")
ff_tempdt_avg_det = ff_tempdt_avg

ff_correlation = np.zeros(ff_tempdt_avg_det[0].shape)
ff_p_vals = np.zeros(ff_tempdt_avg_det[0].shape)
ff_var_mean_det = ff_var_mean
signal.detrend(ff_var_mean_det[~np.isnan(ff_var_mean_det)], overwrite_data=True)
ff_nino_ts = pd.DataFrame(ff_var_mean_det).rolling(360, center=True).mean().to_numpy()[:, 0]
for i in range(len(ff_tempdt_avg_det[0, :, 0])):
    for j in range(len(ff_tempdt_avg_det[0, i, :])):
        print(str(i) + ":" + str(j) )
        if np.isnan(ff_tempdt_avg_det[200, i, j]):
            r, p = (np.nan, np.nan)
        else:
            signal.detrend(ff_tempdt_avg_det[:, i, j], overwrite_data=True)
            ff_tempdt_avg_det[:, i, j] = pd.DataFrame(ff_tempdt_avg_det[:, i, j]).rolling(360, center=True).mean().to_numpy()[:, 0]
            r, p = stats.pearsonr(ff_tempdt_avg_det[300:-300, i, j], ff_nino_ts[300:-300])
        ff_correlation[i, j], ff_p_vals[i, j] = r, p

ghg_tempdt_avg = np.load("../Data/ghg_tempdt_average.npy")
ghg_tempdt_avg_det = ghg_tempdt_avg

ghg_correlation = np.zeros(ghg_tempdt_avg_det[0].shape)
ghg_p_vals = np.zeros(ghg_tempdt_avg_det[0].shape)
ghg_var_mean_det = ghg_var_mean
signal.detrend(ghg_var_mean_det[~np.isnan(ghg_var_mean_det)], overwrite_data=True)
ghg_nino_ts = pd.DataFrame(ghg_var_mean_det).rolling(360, center=True).mean().to_numpy()[:, 0]
for i in range(len(ghg_tempdt_avg_det[0, :, 0])):
    for j in range(len(ghg_tempdt_avg_det[0, i, :])):
        print(str(i) + ":" + str(j) )
        if np.isnan(ghg_tempdt_avg_det[200, i, j]):
            r, p = (np.nan, np.nan)
        else:
            signal.detrend(ghg_tempdt_avg_det[:, i, j], overwrite_data=True)
            ghg_tempdt_avg_det[:, i, j] = pd.DataFrame(ghg_tempdt_avg_det[:, i, j]).rolling(360, center=True).mean().to_numpy()[:, 0]
            r, p = stats.pearsonr(ghg_tempdt_avg_det[300:-300, i, j], ghg_nino_ts[300:-300])
        ghg_correlation[i, j], ghg_p_vals[i, j] = r, p

aer_tempdt_avg = np.load("../Data/aer_tempdt_average.npy")
aer_tempdt_avg_det = aer_tempdt_avg

aer_correlation = np.zeros(aer_tempdt_avg_det[0].shape)
aer_p_vals = np.zeros(aer_tempdt_avg_det[0].shape)
aer_var_mean_det = aer_var_mean
signal.detrend(aer_var_mean_det[~np.isnan(aer_var_mean_det)], overwrite_data=True)
aer_nino_ts = pd.DataFrame(aer_var_mean_det).rolling(360, center=True).mean().to_numpy()[:, 0]
for i in range(len(aer_tempdt_avg_det[0, :, 0])):
    for j in range(len(aer_tempdt_avg_det[0, i, :])):
        print(str(i) + ":" + str(j) )
        if np.isnan(aer_tempdt_avg_det[200, i, j]):
            r, p = (np.nan, np.nan)
        else:
            signal.detrend(aer_tempdt_avg_det[:, i, j], overwrite_data=True)
            aer_tempdt_avg_det[:, i, j] = pd.DataFrame(aer_tempdt_avg_det[:, i, j]).rolling(360, center=True).mean().to_numpy()[:, 0]
            r, p = stats.pearsonr(aer_tempdt_avg_det[300:-300, i, j], aer_nino_ts[300:-300])
        aer_correlation[i, j], aer_p_vals[i, j] = r, p

# %%
cmap = plt.get_cmap('coolwarm')
norm = colors.Normalize(vmin=-1, vmax=1)
cf = cm.ScalarMappable(norm=norm, cmap=cmap)

fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, sharex=True, figsize=size2)
ax1.contourf(lon1, depth[:36], ff_correlation[:36], 32,  cmap=cmap, vmin=-1, vmax=1)
ax1.set_ylabel("Depth, m")
ax1.invert_yaxis()
ax1.set_yscale("log")
figlett(ax1, "a ff")

ax2.contourf(lon1, depth[:36], ghg_correlation[:36], 32, cmap=cmap, vmin=-1, vmax=1)
ax2.set_ylabel("Depth, m")
ax2.invert_yaxis()
ax2.set_yscale("log")
figlett(ax2, "b xghg")

ax3.contourf(lon1, depth[:36], aer_correlation[:36], 32, cmap=cmap, vmin=-1, vmax=1)
ax3.set_xlabel("Longitude")
ax3.set_ylabel("Depth, m")
ax3.invert_yaxis()
ax3.set_yscale("log")
figlett(ax3, "c xaer")

fig.suptitle("TEMPDT Correlation coefficient with Nino 3.4 20-year variance")
fig.subplots_adjust(right=.87, left=.07, top=.94, bottom=0.05, hspace=.02)
cbar_ax = fig.add_axes([0.9, 0.15, 0.03, 0.7])
fig.colorbar(cf, cax=cbar_ax)
fig.savefig("19.pdf", format="pdf")

# %%

ff_tempdt_subsurf = np.average(ff_tempdt_avg_det[:,15:20, 60:125], axis=(1, 2))
ff_tempdt_surf = np.average(ff_tempdt_avg_det[:, 0:10, 60:125], axis=(1, 2))
ghg_tempdt_subsurf = np.average(ghg_tempdt_avg_det[:,15:20, 60:125], axis=(1, 2))
ghg_tempdt_surf = np.average(ghg_tempdt_avg_det[:, 0:10, 60:125], axis=(1, 2))
aer_tempdt_subsurf = np.average(aer_tempdt_avg_det[:,15:20, 60:125], axis=(1, 2))
aer_tempdt_surf = np.average(aer_tempdt_avg_det[:, 0:10, 60:125], axis=(1, 2))

# %%
fig, axs = plt.subplots(nrows=3, ncols=2, sharex=True, sharey=True, figsize=size2)
axt = np.array([
        [axs[0, 0].twinx(), axs[0, 1].twinx()],
        [axs[1, 0].twinx(), axs[1, 1].twinx()],
        [axs[2, 0].twinx(), axs[2, 1].twinx()],
        ])
ln1 = axs[0,0].plot(date_2172, ff_tempdt_surf, label="Surface", color="C0")
ln2 = axt[0,0].plot(date_2172, ff_var_mean_det, label="Nino 3.4 Variance", color="C2")
lns = ln1 + ln2
labs = [l.get_label() for l in lns]
axs[0,0].set_ylabel("Temperature °C", color="C0")
axt[0,0].set_ylabel("Variance", color="C2")
figlett(axs[0,0], "a ff")
axs[0, 0].set_title("Surface")

ln1 = axs[0,1].plot(date_2172, ff_tempdt_subsurf, label="Subsurface", color="C0")
ln2 = axt[0,1].plot(date_2172, ff_var_mean_det, label="Nino 3.4 Variance", color="C2")
lns = ln1 + ln2
labs = [l.get_label() for l in lns]
axs[0,1].set_ylabel("Temperature °C", color="C0")
axt[0,1].set_ylabel("Variance", color="C2")
figlett(axs[0,1], "b ff")
axs[0, 1].set_title("Subsurface")

ln1 = axs[1,0].plot(date_1932, ghg_tempdt_surf, label="Surface", color="C0")
ln2 = axt[1,0].plot(date_1932, ghg_var_mean_det, label="Nino 3.4 Variance", color="C2")
lns = ln1 + ln2
labs = [l.get_label() for l in lns]
axs[1,0].set_ylabel("Temperature °C", color="C0")
axt[1,0].set_ylabel("Variance", color="C2")
figlett(axs[1,0], "c ghg")

ln1 = axs[1,1].plot(date_1932, ghg_tempdt_subsurf, label="Subsurface", color="C0")
ln2 = axt[1,1].plot(date_1932, ghg_var_mean_det, label="Nino 3.4 Variance", color="C2")
lns = ln1 + ln2
labs = [l.get_label() for l in lns]
axs[1,1].set_ylabel("Temperature °C", color="C0")
axt[1,1].set_ylabel("Variance", color="C2")
figlett(axs[1,1], "d ghg")

ln1 = axs[2,0].plot(date_1932, aer_tempdt_surf, label="Surface", color="C0")
ln2 = axt[2,0].plot(date_1932, aer_var_mean_det, label="Nino 3.4 Variance", color="C2")
lns = ln1 + ln2
labs = [l.get_label() for l in lns]
axs[2,0].set_ylabel("Temperature °C", color="C0")
axt[2,0].set_ylabel("Variance", color="C2")
figlett(axs[2,0], "e aer")

ln1 = axs[2,1].plot(date_1932, aer_tempdt_subsurf, label="Subsurface", color="C0")
ln2 = axt[2,1].plot(date_1932, aer_var_mean_det, label="Nino 3.4 Variance", color="C2")
lns = ln1 + ln2
axs[2,1].set_ylabel("Temperature °C", color="C0")
axt[2,1].set_ylabel("Variance", color="C2")
figlett(axs[2,1], "f aer")

fig.suptitle("Comparison of Nino 3.4 variance and TEMPDT timeseries", y=.99)
fig.tight_layout(pad=0.5)
fig.subplots_adjust(top=.95)
fig.savefig("20.pdf", format="pdf")




