from helpers import *
import feather as ft

# %%
print("ff tempdt")
ff_tempdt = get_ensemble("/Volumes/Extreme SSD/LE/TEMPDT/ff", 0, "TEMPDT")
ff_tempdt_avg = np.average(ff_tempdt, axis=0)
del ff_tempdt
os.chdir("/Volumes/Extreme SSD/LE/compiled/")
np.save("ff_tempdt_avg", ff_tempdt_avg)

# %%
print("ff tempcep")
ff_tempcep = get_ensemble("/Volumes/Extreme SSD/LE/TEMPCEP/ff", 0, "TEMPCEP")
ff_tempcep_avg = np.average(ff_tempcep, axis=0)
del ff_tempcep
os.chdir("/Volumes/Extreme SSD/LE/compiled/")
np.save("ff_tempcep_avg", ff_tempcep_avg)

# %%
print("ff tempwep")
ff_tempwep = get_ensemble("/Volumes/Extreme SSD/LE/TEMPWEP/ff", 0, "TEMPWEP")
ff_tempwep_avg = np.average(ff_tempwep, axis=0)
del ff_tempwep
os.chdir("/Volumes/Extreme SSD/LE/compiled/")
np.save("ff_tempwep_avg", ff_tempwep_avg)

# %%
print("ff tempeep")
ff_tempeep = get_ensemble("/Volumes/Extreme SSD/LE/TEMPEEP/ff", 0, "TEMPEEP")
ff_tempeep_avg = np.average(ff_tempeep, axis=0)
del ff_tempeep
os.chdir("/Volumes/Extreme SSD/LE/compiled/")
np.save("ff_tempeep_avg", ff_tempeep_avg)

# %%
print("ghg tempdt")
ghg_tempdt = get_ensemble("/Volumes/Extreme SSD/LE/TEMPDT/xghg", 1, "TEMPDT")
ghg_tempdt_avg = np.average(ghg_tempdt, axis=0)
del ghg_tempdt
os.chdir("/Volumes/Extreme SSD/LE/compiled/")
np.save("ghg_tempdt_avg", ghg_tempdt_avg)

# %%
print("ghg tempcep")
ghg_tempcep = get_ensemble("/Volumes/Extreme SSD/LE/TEMPCEP/xghg", 1, "TEMPCEP")
ghg_tempcep_avg = np.average(ghg_tempcep, axis=0)
del ghg_tempcep
os.chdir("/Volumes/Extreme SSD/LE/compiled/")
np.save("ghg_tempcep_avg", ghg_tempcep_avg)

# %%
print("ghg tempwep")
ghg_tempwep = get_ensemble("/Volumes/Extreme SSD/LE/TEMPWEP/xghg", 1, "TEMPWEP")
ghg_tempwep_avg = np.average(ghg_tempwep, axis=0)
del ghg_tempwep
os.chdir("/Volumes/Extreme SSD/LE/compiled/")
np.save("ghg_tempwep_avg", ghg_tempwep_avg)

# %%
print("ghg tempeep")
ghg_tempeep = get_ensemble("/Volumes/Extreme SSD/LE/TEMPEEP/xghg", 1, "TEMPEEP")
ghg_tempeep_avg = np.average(ghg_tempeep, axis=0)
del ghg_tempeep
os.chdir("/Volumes/Extreme SSD/LE/compiled/")
np.save("ghg_tempeep_avg", ghg_tempeep_avg)

# %%
print("aer tempdt")
aer_tempdt = get_ensemble("/Volumes/Extreme SSD/LE/TEMPDT/xaer", 1, "TEMPDT")
aer_tempdt_avg = np.average(aer_tempdt, axis=0)
del aer_tempdt
os.chdir("/Volumes/Extreme SSD/LE/compiled/")
np.save("aer_tempdt_avg", aer_tempdt_avg)

# %%
print("aer tempcep")
aer_tempcep = get_ensemble("/Volumes/Extreme SSD/LE/TEMPCEP/xaer", 1, "TEMPCEP")
aer_tempcep_avg = np.average(aer_tempcep, axis=0)
del aer_tempcep
os.chdir("/Volumes/Extreme SSD/LE/compiled/")
np.save("aer_tempcep_avg", aer_tempcep_avg)

# %%
print("aer tempwep")
aer_tempwep = get_ensemble("/Volumes/Extreme SSD/LE/TEMPWEP/xaer", 1, "TEMPWEP")
aer_tempwep_avg = np.average(aer_tempwep, axis=0)
del aer_tempwep
os.chdir("/Volumes/Extreme SSD/LE/compiled/")
np.save("aer_tempwep_avg", aer_tempwep_avg)

# %%
print("aer tempeep")
aer_tempeep = get_ensemble("/Volumes/Extreme SSD/LE/TEMPEEP/xaer", 1, "TEMPEEP")
aer_tempeep_avg = np.average(aer_tempeep, axis=0)
del aer_tempeep
os.chdir("/Volumes/Extreme SSD/LE/compiled/")
np.save("aer_tempeep_avg", aer_tempeep_avg)
