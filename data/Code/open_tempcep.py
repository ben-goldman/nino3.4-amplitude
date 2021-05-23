# %%
import numpy as np
import netCDF4 as nc
import os

os.chdir("/Volumes/Extreme SSD/LE/TEMPCEP/ff/")

# %%
ff_tempcep_set = np.zeros((34, 2172, 60, 41))
for i in range(2, 36):
    print(i, end="|")
    if i < 10:
        f1 = nc.Dataset("b.e11.B20TRC5CNBDRD.f09_g16.00%s.pop.h.TEMPCEP.192001-200512.nc" % i)
        f2 = nc.Dataset("b.e11.BRCP85C5CNBDRD.f09_g16.00%s.pop.h.TEMPCEP.200601-208012.nc" % i)
        f3 = nc.Dataset("b.e11.BRCP85C5CNBDRD.f09_g16.00%s.pop.h.TEMPCEP.208101-210012.nc" % i)

        v1 = f1.variables["TEMPCEP"][:, :, :]
        v2 = f2.variables["TEMPCEP"][:, :, :]
        v3 = f3.variables["TEMPCEP"][:, :, :]

        v1[v1.mask] = np.nan
        v2[v2.mask] = np.nan
        v3[v3.mask] = np.nan
        ff_tempcep_set[i-2, :, :, :] = np.concatenate((v1, v2, v3))

        f1.close()
        f2.close()
        f3.close()

    elif i < 34:
        f1 = nc.Dataset("b.e11.B20TRC5CNBDRD.f09_g16.0%s.pop.h.TEMPCEP.192001-200512.nc" % i)
        f2 = nc.Dataset("b.e11.BRCP85C5CNBDRD.f09_g16.0%s.pop.h.TEMPCEP.200601-208012.nc" % i)
        f3 = nc.Dataset("b.e11.BRCP85C5CNBDRD.f09_g16.0%s.pop.h.TEMPCEP.208101-210012.nc" % i)


        v1 = f1.variables["TEMPCEP"][:, :, :]
        v2 = f2.variables["TEMPCEP"][:, :, :]
        v3 = f3.variables["TEMPCEP"][:, :, :]
        
        v1[v1.mask] = np.nan
        v2[v2.mask] = np.nan
        v3[v3.mask] = np.nan
        ff_tempcep_set[i-2, :, :, :] = np.concatenate((v1, v2, v3))

        f1.close()
        f2.close()
        f3.close()

    else:
        f1 = nc.Dataset("b.e11.B20TRC5CNBDRD.f09_g16.0%s.pop.h.TEMPCEP.192001-200512.nc" % i)
        f2 = nc.Dataset("b.e11.BRCP85C5CNBDRD.f09_g16.0%s.pop.h.TEMPCEP.200601-210012.nc" % i)

        v1 = f1.variables["TEMPCEP"][:, :, :]
        v2 = f2.variables["TEMPCEP"][:, :, :]

        v1[v1.mask] = np.nan
        v2[v2.mask] = np.nan
        ff_tempcep_set[i-2, :, :, :] = np.concatenate((v1, v2))

        f1.close()
        f2.close()

ff_avg = np.average(ff_tempcep_set, axis=0)
del ff_tempcep_set

# %%

os.chdir("/Volumes/Extreme SSD/LE/TEMPCEP/xghg/")

ghg_tempcep_set = np.zeros((20, 1932, 60, 41))
for i in range(1, 21):
    print(i)
    if i < 10:
        f1 = nc.Dataset("b.e11.B20TRLENS_RCP85.f09_g16.xghg.00%s.pop.h.TEMPCEP.192001-200512.nc" % i)
        f2 = nc.Dataset("b.e11.B20TRLENS_RCP85.f09_g16.xghg.00%s.pop.h.TEMPCEP.200601-208012.nc" % i)

        v1 = f1.variables["TEMPCEP"][:, :, :]
        v2 = f2.variables["TEMPCEP"][:, :, :]

        v1[v1.mask] = np.nan
        v2[v2.mask] = np.nan
        ghg_tempcep_set[i-1, :, :, :] = np.concatenate((v1, v2))

        f1.close()
        f2.close()

    else:
        f1 = nc.Dataset("b.e11.B20TRLENS_RCP85.f09_g16.xghg.0%s.pop.h.TEMPCEP.192001-200512.nc" % i)
        f2 = nc.Dataset("b.e11.B20TRLENS_RCP85.f09_g16.xghg.0%s.pop.h.TEMPCEP.200601-208012.nc" % i)

        v1 = f1.variables["TEMPCEP"][:, :, :]
        v2 = f2.variables["TEMPCEP"][:, :, :]

        v1[v1.mask] = np.nan
        v2[v2.mask] = np.nan
        ghg_tempcep_set[i-1, :, :, :] = np.concatenate((v1, v2))

        f1.close()
        f2.close()

ghg_avg = np.average(ghg_tempcep_set, axis=0)
del ghg_tempcep_set

os.chdir("/Volumes/Extreme SSD/LE/TEMPCEP/xaer/")

aer_tempcep_set = np.zeros((20, 1932, 60, 41))
for i in range(1, 21):
    print(i)
    if i < 10:
        f1 = nc.Dataset("b.e11.B20TRLENS_RCP85.f09_g16.xaer.00%s.pop.h.TEMPCEP.192001-200512.nc" % i)
        f2 = nc.Dataset("b.e11.B20TRLENS_RCP85.f09_g16.xaer.00%s.pop.h.TEMPCEP.200601-208012.nc" % i)

        v1 = f1.variables["TEMPCEP"][:, :, :]
        v2 = f2.variables["TEMPCEP"][:, :, :]

        v1[v1.mask] = np.nan
        v2[v2.mask] = np.nan
        aer_tempcep_set[i-1, :, :, :] = np.concatenate((v1, v2))

        f1.close()
        f2.close()

    else:
        f1 = nc.Dataset("b.e11.B20TRLENS_RCP85.f09_g16.xaer.0%s.pop.h.TEMPCEP.192001-200512.nc" % i)
        f2 = nc.Dataset("b.e11.B20TRLENS_RCP85.f09_g16.xaer.0%s.pop.h.TEMPCEP.200601-208012.nc" % i)

        v1 = f1.variables["TEMPCEP"][:, :, :]
        v2 = f2.variables["TEMPCEP"][:, :, :]

        v1[v1.mask] = np.nan
        v2[v2.mask] = np.nan
        aer_tempcep_set[i-1, :, :, :] = np.concatenate((v1, v2))

        f1.close()
        f2.close()
aer_avg = np.average(aer_tempcep_set, axis=0)
del aer_tempcep_set

os.chdir("/Users/bengoldman/ENSO-amplitude/Data")
np.save("ff_tempcep_average",ff_avg)
np.save("ghg_tempcep_average", ghg_avg)
np.save("aer_tempcep_average", aer_avg)
