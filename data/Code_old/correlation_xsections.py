# %%
from helpers import *
from variance import ff_var_mean, ghg_var_mean, aer_var_mean, ghg_bs_mean, aer_bs_mean

# %%
ff_tempdt = np.load("/Volumes/Extreme SSD/LE/compiled/ff_tempdt_avg.npy")
ff_tempcep = np.load("/Volumes/Extreme SSD/LE/compiled/ff_tempcep_avg.npy")
ff_tempwep = np.load("/Volumes/Extreme SSD/LE/compiled/ff_tempwep_avg.npy")
ff_tempeep = np.load("/Volumes/Extreme SSD/LE/compiled/ff_tempeep_avg.npy")
ghg_tempdt = np.load("/Volumes/Extreme SSD/LE/compiled/ghg_tempdt_avg.npy")
ghg_tempcep = np.load("/Volumes/Extreme SSD/LE/compiled/ghg_tempcep_avg.npy")
ghg_tempwep = np.load("/Volumes/Extreme SSD/LE/compiled/ghg_tempwep_avg.npy")
ghg_tempeep = np.load("/Volumes/Extreme SSD/LE/compiled/ghg_tempeep_avg.npy")
aer_tempdt = np.load("/Volumes/Extreme SSD/LE/compiled/aer_tempdt_avg.npy")
aer_tempcep = np.load("/Volumes/Extreme SSD/LE/compiled/aer_tempcep_avg.npy")
aer_tempwep = np.load("/Volumes/Extreme SSD/LE/compiled/aer_tempwep_avg.npy")
aer_tempeep = np.load("/Volumes/Extreme SSD/LE/compiled/aer_tempeep_avg.npy")

# %%
print("ghg")
diff_ghg_tempdt_rs, diff_ghg_tempdt_ps = correlation_detrended(-(ghg_tempdt-ff_tempdt[:1932]), ghg_bs_mean)
print("ghg")
diff_ghg_tempcep_rs, diff_ghg_tempcep_ps = correlation_detrended(-(ghg_tempcep-ff_tempcep[:1932]), ghg_bs_mean)
print("ghg")
diff_ghg_tempwep_rs, diff_ghg_tempwep_ps = correlation_detrended(-(ghg_tempwep-ff_tempwep[:1932]), ghg_bs_mean)
print("ghg")
diff_ghg_tempeep_rs, diff_ghg_tempeep_ps = correlation_detrended(-(ghg_tempeep-ff_tempeep[:1932]), ghg_bs_mean)
print("aer")
diff_aer_tempdt_rs, diff_aer_tempdt_ps = correlation_detrended(-(aer_tempdt-ff_tempdt[:1932]), aer_bs_mean)
print("aer")
diff_aer_tempcep_rs, diff_aer_tempcep_ps = correlation_detrended(-(aer_tempcep-ff_tempcep[:1932]), aer_bs_mean)
print("aer")
diff_aer_tempwep_rs, diff_aer_tempwep_ps = correlation_detrended(-(aer_tempwep-ff_tempwep[:1932]), aer_bs_mean)
print("aer")
diff_aer_tempeep_rs, diff_aer_tempeep_ps = correlation_detrended(-(aer_tempeep-ff_tempeep[:1932]), aer_bs_mean)

# %%
print("ff")
ff_tempdt_rs, ff_tempdt_ps = correlation_detrended(ff_tempdt, ff_var_mean)
print("ff")
ff_tempcep_rs, ff_tempcep_ps = correlation_detrended(ff_tempcep, ff_var_mean)
print("ff")
ff_tempwep_rs, ff_tempwep_ps = correlation_detrended(ff_tempwep, ff_var_mean)
print("ff")
ff_tempeep_rs, ff_tempeep_ps = correlation_detrended(ff_tempeep, ff_var_mean)
print("ghg")
ghg_tempdt_rs, diff_ghg_tempdt_ps = correlation_detrended(ghg_tempdt, ghg_var_mean)
print("ghg")
ghg_tempcep_rs, diff_ghg_tempcep_ps = correlation_detrended(ghg_tempcep, ghg_var_mean)
print("ghg")
ghg_tempwep_rs, diff_ghg_tempwep_ps = correlation_detrended(ghg_tempwep, ghg_var_mean)
print("ghg")
ghg_tempeep_rs, diff_ghg_tempeep_ps = correlation_detrended(ghg_tempeep, ghg_var_mean)
print("aer")
aer_tempdt_rs, diff_aer_tempdt_ps = correlation_detrended(aer_tempdt, aer_var_mean)
print("aer")
aer_tempcep_rs, diff_aer_tempcep_ps = correlation_detrended(aer_tempcep, aer_var_mean)
print("aer")
aer_tempwep_rs, diff_aer_tempwep_ps = correlation_detrended(aer_tempwep, aer_var_mean)
print("aer")
aer_tempeep_rs, diff_aer_tempeep_ps = correlation_detrended(aer_tempeep, aer_var_mean)

# %%
os.chdir("/Users/bengoldman/ENSO-amplitude/Data")
np.save("ff_tempdt_rs", ff_tempdt_rs)
np.save("ff_tempcep_rs", ff_tempcep_rs)
np.save("ff_tempwep_rs", ff_tempwep_rs)
np.save("ff_tempeep_rs", ff_tempeep_rs)
np.save("ghg_tempdt_rs", ghg_tempdt_rs)
np.save("ghg_tempcep_rs", ghg_tempcep_rs)
np.save("ghg_tempwep_rs", ghg_tempwep_rs)
np.save("ghg_tempeep_rs", ghg_tempeep_rs)
np.save("aer_tempdt_rs", aer_tempdt_rs)
np.save("aer_tempcep_rs", aer_tempcep_rs)
np.save("aer_tempwep_rs", aer_tempwep_rs)
np.save("aer_tempeep_rs", aer_tempeep_rs)

np.save("ff_tempdt_ps", ff_tempdt_ps)
np.save("ff_tempcep_ps", ff_tempcep_ps)
np.save("ff_tempwep_ps", ff_tempwep_ps)
np.save("ff_tempeep_ps", ff_tempeep_ps)
np.save("ghg_tempdt_ps", ghg_tempdt_ps)
np.save("ghg_tempcep_ps", ghg_tempcep_ps)
np.save("ghg_tempwep_ps", ghg_tempwep_ps)
np.save("ghg_tempeep_ps", ghg_tempeep_ps)
np.save("aer_tempdt_ps", aer_tempdt_ps)
np.save("aer_tempcep_ps", aer_tempcep_ps)
np.save("aer_tempwep_ps", aer_tempwep_ps)
np.save("aer_tempeep_ps", aer_tempeep_ps)

# %%
os.chdir("/Users/bengoldman/ENSO-amplitude/Data")
np.save("diff_ghg_tempdt_rs", diff_ghg_tempdt_rs)
np.save("diff_ghg_tempcep_rs", diff_ghg_tempcep_rs)
np.save("diff_ghg_tempwep_rs", diff_ghg_tempwep_rs)
np.save("diff_ghg_tempeep_rs", diff_ghg_tempeep_rs)
np.save("diff_aer_tempdt_rs", diff_aer_tempdt_rs)
np.save("diff_aer_tempcep_rs", diff_aer_tempcep_rs)
np.save("diff_aer_tempwep_rs", diff_aer_tempwep_rs)
np.save("diff_aer_tempeep_rs", diff_aer_tempeep_rs)

np.save("diff_ghg_tempdt_ps", diff_ghg_tempdt_ps)
np.save("diff_ghg_tempcep_ps", diff_ghg_tempcep_ps)
np.save("diff_ghg_tempwep_ps", diff_ghg_tempwep_ps)
np.save("diff_ghg_tempeep_ps", diff_ghg_tempeep_ps)
np.save("diff_aer_tempdt_ps", diff_aer_tempdt_ps)
np.save("diff_aer_tempcep_ps", diff_aer_tempcep_ps)
np.save("diff_aer_tempwep_ps", diff_aer_tempwep_ps)
np.save("diff_aer_tempeep_ps", diff_aer_tempeep_ps)

# %%
os.chdir("/Users/bengoldman/ENSO-amplitude/Data")
ff_tempdt_rs = np.load("ff_tempdt_rs.npy")
ff_tempcep_rs = np.load("ff_tempcep_rs.npy")
ff_tempwep_rs = np.load("ff_tempwep_rs.npy")
ff_tempeep_rs = np.load("ff_tempeep_rs.npy")
ghg_tempdt_rs = np.load("ghg_tempdt_rs.npy")
ghg_tempcep_rs = np.load("ghg_tempcep_rs.npy")
ghg_tempwep_rs = np.load("ghg_tempwep_rs.npy")
ghg_tempeep_rs = np.load("ghg_tempeep_rs.npy")
aer_tempdt_rs = np.load("aer_tempdt_rs.npy")
aer_tempcep_rs = np.load("aer_tempcep_rs.npy")
aer_tempwep_rs = np.load("aer_tempwep_rs.npy")
aer_tempeep_rs = np.load("aer_tempeep_rs.npy")

ff_tempdt_ps = np.load("ff_tempdt_ps.npy")
ff_tempcep_ps = np.load("ff_tempcep_ps.npy")
ff_tempwep_ps = np.load("ff_tempwep_ps.npy")
ff_tempeep_ps = np.load("ff_tempeep_ps.npy")
ghg_tempdt_ps = np.load("ghg_tempdt_ps.npy")
ghg_tempcep_ps = np.load("ghg_tempcep_ps.npy")
ghg_tempwep_ps = np.load("ghg_tempwep_ps.npy")
ghg_tempeep_ps = np.load("ghg_tempeep_ps.npy")
aer_tempdt_ps = np.load("aer_tempdt_ps.npy")
aer_tempcep_ps = np.load("aer_tempcep_ps.npy")
aer_tempwep_ps = np.load("aer_tempwep_ps.npy")
aer_tempeep_ps = np.load("aer_tempeep_ps.npy")

# %%
os.chdir("/Users/bengoldman/ENSO-amplitude/Data")
diff_ghg_tempdt_rs = np.load("diff_ghg_tempdt_rs.npy")
diff_ghg_tempcep_rs = np.load("diff_ghg_tempcep_rs.npy")
diff_ghg_tempwep_rs = np.load("diff_ghg_tempwep_rs.npy")
diff_ghg_tempeep_rs = np.load("diff_ghg_tempeep_rs.npy")
diff_aer_tempdt_rs = np.load("diff_aer_tempdt_rs.npy")
diff_aer_tempcep_rs = np.load("diff_aer_tempcep_rs.npy")
diff_aer_tempwep_rs = np.load("diff_aer_tempwep_rs.npy")
diff_aer_tempeep_rs = np.load("diff_aer_tempeep_rs.npy")

diff_ghg_tempdt_ps = np.load("diff_ghg_tempdt_ps.npy")
diff_ghg_tempcep_ps = np.load("diff_ghg_tempcep_ps.npy")
diff_ghg_tempwep_ps = np.load("diff_ghg_tempwep_ps.npy")
diff_ghg_tempeep_ps = np.load("diff_ghg_tempeep_ps.npy")
diff_aer_tempdt_ps = np.load("diff_aer_tempdt_ps.npy")
diff_aer_tempcep_ps = np.load("diff_aer_tempcep_ps.npy")
diff_aer_tempwep_ps = np.load("diff_aer_tempwep_ps.npy")
diff_aer_tempeep_ps = np.load("diff_aer_tempeep_ps.npy")

# %%
os.chdir("../Figures")
three_contours(ff_tempdt_rs, ghg_tempdt_rs, aer_tempdt_rs, ff_tempdt_ps>.1, ghg_tempdt_ps>.1, aer_tempdt_ps>.1, ff_tempdt_ps>.2, ghg_tempdt_ps>.2, aer_tempdt_ps>.2, "TEMPDT Correlation With Nino 3.4 Variance", "Longitude (Degrees east)", lon1, "Depth (m)", depth)
plt.savefig("tempdt.pdf")

# %%
three_contours(ff_tempcep_rs, ghg_tempcep_rs, aer_tempcep_rs, ff_tempcep_ps>.1, ghg_tempcep_ps>.1, aer_tempcep_ps>.1, ff_tempcep_ps>.2, ghg_tempcep_ps>.2, aer_tempcep_ps>.2, "TEMPCEP Correlation With Nino 3.4 Variance", "Latitude", lat1, "Depth (m)", depth)
plt.savefig("tempcep.pdf")

# %%
three_contours(ff_tempwep_rs, ghg_tempwep_rs, aer_tempwep_rs, ff_tempwep_ps>.1, ghg_tempwep_ps>.1, aer_tempwep_ps>.1, ff_tempwep_ps>.2, ghg_tempwep_ps>.2, aer_tempwep_ps>.2, "TEMPWEP Correlation With Nino 3.4 Variance", "Latitude", lat1, "Depth (m)", depth)
plt.savefig("tempwep.pdf")

# %%
three_contours(ff_tempeep_rs, ghg_tempeep_rs, aer_tempeep_rs, ff_tempeep_ps>.1, ghg_tempeep_ps>.1, aer_tempeep_ps>.1, ff_tempeep_ps>.2, ghg_tempeep_ps>.2, aer_tempeep_ps>.2, "TEMPEEP Correlation With Nino 3.4 Variance", "Latitude", lat1, "Depth (m)", depth)
plt.savefig("tempeep.pdf")

# %%
os.chdir("../Figures")
three_contours(ff_tempdt_rs, diff_ghg_tempdt_rs, diff_aer_tempdt_rs, ff_tempdt_ps>.1, diff_ghg_tempdt_ps>.1, diff_aer_tempdt_ps>.1, ff_tempdt_ps>.2, diff_ghg_tempdt_ps>.2, diff_aer_tempdt_ps>.2, "TEMPDT Correlation With Nino 3.4 Variance", "Longitude (Degrees east)", lon1, "Depth (m)", depth)
plt.savefig("diff_tempdt.pdf")

# %%
three_contours(ff_tempcep_rs, diff_ghg_tempcep_rs, diff_aer_tempcep_rs, ff_tempcep_ps>.1, diff_ghg_tempcep_ps>.1, diff_aer_tempcep_ps>.1, ff_tempcep_ps>.2, diff_ghg_tempcep_ps>.2, diff_aer_tempcep_ps>.2, "TEMPCEP Correlation With Nino 3.4 Variance", "Latitude", lat1, "Depth (m)", depth)
plt.savefig("diff_tempcep.pdf")

# %%
three_contours(ff_tempwep_rs, diff_ghg_tempwep_rs, diff_aer_tempwep_rs, ff_tempwep_ps>.1, diff_ghg_tempwep_ps>.1, diff_aer_tempwep_ps>.1, ff_tempwep_ps>.2, diff_ghg_tempwep_ps>.2, diff_aer_tempwep_ps>.2, "TEMPWEP Correlation With Nino 3.4 Variance", "Latitude", lat1, "Depth (m)", depth)
plt.savefig("diff_tempwep.pdf")

# %%
three_contours(ff_tempeep_rs, diff_ghg_tempeep_rs, diff_aer_tempeep_rs, ff_tempeep_ps>.1, diff_ghg_tempeep_ps>.1, diff_aer_tempeep_ps>.1, ff_tempeep_ps>.2, diff_ghg_tempeep_ps>.2, diff_aer_tempeep_ps>.2, "TEMPEEP Correlation With Nino 3.4 Variance", "Latitude", lat1, "Depth (m)", depth)
plt.savefig("diff_tempeep.pdf")

# %%
ff_tempdt_surf = pd.DataFrame(np.mean(signal.detrend(ff_tempdt[:, 0:12, 60:120], axis=0), axis=(1, 2))).rolling(240, center=True).mean().to_numpy()[:, 0]
ff_tempdt_subsurf = pd.DataFrame(np.mean(signal.detrend(ff_tempdt[:, 12:22, 60:120], axis=0), axis=(1, 2))).rolling(240, center=True).mean().to_numpy()[:, 0]
ff_var_mean_det = np.copy(ff_var_mean)
signal.detrend(ff_var_mean_det[120:-119], overwrite_data=True)

ghg_tempdt_surf = pd.DataFrame(np.mean(signal.detrend(ghg_tempdt[:, 0:12, 60:120], axis=0), axis=(1, 2))).rolling(240, center=True).mean().to_numpy()[:, 0]
ghg_tempdt_subsurf = pd.DataFrame(np.mean(signal.detrend(ghg_tempdt[:, 12:22, 60:120], axis=0), axis=(1, 2))).rolling(240, center=True).mean().to_numpy()[:, 0]
ghg_var_mean_det = np.copy(ghg_var_mean)
signal.detrend(ghg_var_mean_det[120:-119], overwrite_data=True)

aer_tempdt_surf = pd.DataFrame(np.mean(signal.detrend(aer_tempdt[:, 0:12, 60:120], axis=0), axis=(1, 2))).rolling(240, center=True).mean().to_numpy()[:, 0]
aer_tempdt_subsurf = pd.DataFrame(np.mean(signal.detrend(aer_tempdt[:, 12:22, 60:120], axis=0), axis=(1, 2))).rolling(240, center=True).mean().to_numpy()[:, 0]
aer_var_mean_det = np.copy(aer_var_mean)
signal.detrend(aer_var_mean_det[120:-119], overwrite_data=True)

# %%
fig = plt.figure(figsize=size2)
ax1 = fig.add_subplot(311)
ax2 = ax1.twinx()
ax1.plot(date_2172, ff_var_mean_det, color="C0")
ax2.plot(date_2172, ff_tempdt_subsurf, color="C1")
figlett(ax1, "a) ff")

ax3 = fig.add_subplot(312)
ax4 = ax3.twinx()
ax3.plot(date_1932, ghg_var_mean_det, color="C0")
ax4.plot(date_1932, ghg_tempdt_subsurf, color="C1")
ax3.set_ylabel("Detrended Nino 3.4 Variance", color="C0")
ax4.set_ylabel("Detrended Subsurface Temperature Anomaly", color="C1")
figlett(ax3, "b) xghg")

ax5 = fig.add_subplot(313)
ax6 = ax5.twinx()
ax5.plot(date_1932, aer_var_mean_det, color="C0")
ax6.plot(date_1932, aer_tempdt_subsurf, color="C1")
figlett(ax5, "c) xaer")

plt.savefig("tempdttimeseries")
