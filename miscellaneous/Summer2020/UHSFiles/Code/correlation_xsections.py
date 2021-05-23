from helpers import *
from variance import ff_var_mean, ghg_var_mean, aer_var_mean

# %%
print("ff")
ff_tempdt = np.load("../Data/ff_tempdt_avg.npy")
ff_tempdt_rs, ff_tempdt_ps = correlation_detrended(ff_tempdt, ff_var_mean)

# %%
print("ff")
ff_tempcep = np.load("../Data/ff_tempcep_avg.npy")
ff_tempcep_rs, ff_tempcep_ps = correlation_detrended(ff_tempcep, ff_var_mean)

# %%
print("ff")
ff_tempwep = np.load("../Data/ff_tempwep_avg.npy")
ff_tempwep_rs, ff_tempwep_ps = correlation_detrended(ff_tempwep, ff_var_mean)

# %%
print("ff")
ff_tempeep = np.load("../Data/ff_tempeep_avg.npy")
ff_tempeep_rs, ff_tempeep_ps = correlation_detrended(ff_tempeep, ff_var_mean)

# %%
print("ghg")
ghg_tempdt = np.load("../Data/ghg_tempdt_avg.npy")
ghg_tempdt_rs, ghg_tempdt_ps = correlation_detrended(ghg_tempdt, ghg_var_mean)

# %%
print("ghg")
ghg_tempcep = np.load("../Data/ghg_tempcep_avg.npy")
ghg_tempcep_rs, ghg_tempcep_ps = correlation_detrended(ghg_tempcep, ghg_var_mean)

# %%
print("ghg")
ghg_tempwep = np.load("../Data/ghg_tempwep_avg.npy")
ghg_tempwep_rs, ghg_tempwep_ps = correlation_detrended(ghg_tempwep, ghg_var_mean)

# %%
print("ghg")
ghg_tempeep = np.load("../Data/ghg_tempeep_avg.npy")
ghg_tempeep_rs, ghg_tempeep_ps = correlation_detrended(ghg_tempeep, ghg_var_mean)

# %%
print("aer")
aer_tempdt = np.load("../Data/aer_tempdt_avg.npy")
aer_tempdt_rs, aer_tempdt_ps = correlation_detrended(aer_tempdt, aer_var_mean)

# %%
print("aer")
aer_tempcep = np.load("../Data/aer_tempcep_avg.npy")
aer_tempcep_rs, aer_tempcep_ps = correlation_detrended(aer_tempcep, aer_var_mean)

# %%
print("aer")
aer_tempwep = np.load("../Data/aer_tempwep_avg.npy")
aer_tempwep_rs, aer_tempwep_ps = correlation_detrended(aer_tempwep, aer_var_mean)

# %%
aer_tempeep = np.load("../Data/aer_tempeep_avg.npy")
print("aer")
aer_tempeep_rs, aer_tempeep_ps = correlation_detrended(aer_tempeep, aer_var_mean)

# %%
os.chdir("../Figures")
three_contours(ff_tempdt_rs, ghg_tempdt_rs, aer_tempdt_rs, ff_tempdt_ps>.1, ghg_tempdt_ps>.1, aer_tempdt_ps>.1, ff_tempdt_ps>.2, ghg_tempdt_ps>.2, aer_tempdt_ps>.2, "TEMPDT Correlation With Nino 3.4 Variance", "Longitude", lon1)
plt.savefig("19.pdf")

# %%
three_contours(ff_tempcep_rs, ghg_tempcep_rs, aer_tempcep_rs, ff_tempcep_ps>.1, ghg_tempcep_ps>.1, aer_tempcep_ps>.1, ff_tempcep_ps>.2, ghg_tempcep_ps>.2, aer_tempcep_ps>.2, "TEMPCEP Correlation With Nino 3.4 Variance", "Longitude", lat1)
plt.savefig("20.pdf")

# %%
three_contours(ff_tempwep_rs, ghg_tempwep_rs, aer_tempwep_rs, ff_tempwep_ps>.1, ghg_tempwep_ps>.1, aer_tempwep_ps>.1, ff_tempwep_ps>.2, ghg_tempwep_ps>.2, aer_tempwep_ps>.2, "TEMPWEP Correlation With Nino 3.4 Variance", "Longitude", lat1)
plt.savefig("21.pdf")

# %%
three_contours(ff_tempeep_rs, ghg_tempeep_rs, aer_tempeep_rs, ff_tempeep_ps>.1, ghg_tempeep_ps>.1, aer_tempeep_ps>.1, ff_tempeep_ps>.2, ghg_tempeep_ps>.2, aer_tempeep_ps>.2, "TEMPEEP Correlation With Nino 3.4 Variance", "Longitude", lat1)
plt.savefig("22.pdf")
