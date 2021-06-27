# %%
import numpy as np
import netCDF4 as nc
import os

os.chdir("/Volumes/Extreme SSD/LE/TEMPEEP/ff/")

# %%
ff_tempeep_set = np.zeros((34, 2172, 60, 41))
for i in range(2, 36):
    print(i, end="|")
    if i < 10:
        f1 = nc.Dataset("b.e11.B20TRC5CNBDRD.f09_g16.00%s.pop.h.TEMPEEP.192001-200512.nc" % i)
        f2 = nc.Dataset("b.e11.BRCP85C5CNBDRD.f09_g16.00%s.pop.h.TEMPEEP.200601-208012.nc" % i)
        f3 = nc.Dataset("b.e11.BRCP85C5CNBDRD.f09_g16.00%s.pop.h.TEMPEEP.208101-210012.nc" % i)

        v1 = f1.variables["TEMPEEP"][:, :, :]
        v2 = f2.variables["TEMPEEP"][:, :, :]
        v3 = f3.variables["TEMPEEP"][:, :, :]

        v1[v1.mask] = np.nan
        v2[v2.mask] = np.nan
        v3[v3.mask] = np.nan
        ff_tempeep_set[i-2, :, :, :] = np.concatenate((v1, v2, v3))

        f1.close()
        f2.close()
        f3.close()

    elif i < 34:
        f1 = nc.Dataset("b.e11.B20TRC5CNBDRD.f09_g16.0%s.pop.h.TEMPEEP.192001-200512.nc" % i)
        f2 = nc.Dataset("b.e11.BRCP85C5CNBDRD.f09_g16.0%s.pop.h.TEMPEEP.200601-208012.nc" % i)
        f3 = nc.Dataset("b.e11.BRCP85C5CNBDRD.f09_g16.0%s.pop.h.TEMPEEP.208101-210012.nc" % i)


        v1 = f1.variables["TEMPEEP"][:, :, :]
        v2 = f2.variables["TEMPEEP"][:, :, :]
        v3 = f3.variables["TEMPEEP"][:, :, :]
        
        v1[v1.mask] = np.nan
        v2[v2.mask] = np.nan
        v3[v3.mask] = np.nan
        ff_tempeep_set[i-2, :, :, :] = np.concatenate((v1, v2, v3))

        f1.close()
        f2.close()
        f3.close()

    else:
        f1 = nc.Dataset("b.e11.B20TRC5CNBDRD.f09_g16.0%s.pop.h.TEMPEEP.192001-200512.nc" % i)
        f2 = nc.Dataset("b.e11.BRCP85C5CNBDRD.f09_g16.0%s.pop.h.TEMPEEP.200601-210012.nc" % i)

        v1 = f1.variables["TEMPEEP"][:, :, :]
        v2 = f2.variables["TEMPEEP"][:, :, :]

        v1[v1.mask] = np.nan
        v2[v2.mask] = np.nan
        ff_tempeep_set[i-2, :, :, :] = np.concatenate((v1, v2))

        f1.close()
        f2.close()

ff_avg = np.average(ff_tempeep_set, axis=0)
del ff_tempeep_set

# %%

os.chdir("/Volumes/Extreme SSD/LE/TEMPEEP/xghg/")

ghg_tempeep_set = np.zeros((20, 1932, 60, 41))
for i in range(1, 21):
    print(i)
    if i < 10:
        f1 = nc.Dataset("b.e11.B20TRLENS_RCP85.f09_g16.xghg.00%s.pop.h.TEMPEEP.192001-200512.nc" % i)
        f2 = nc.Dataset("b.e11.B20TRLENS_RCP85.f09_g16.xghg.00%s.pop.h.TEMPEEP.200601-208012.nc" % i)

        v1 = f1.variables["TEMPEEP"][:, :, :]
        v2 = f2.variables["TEMPEEP"][:, :, :]

        v1[v1.mask] = np.nan
        v2[v2.mask] = np.nan
        ghg_tempeep_set[i-1, :, :, :] = np.concatenate((v1, v2))

        f1.close()
        f2.close()

    else:
        f1 = nc.Dataset("b.e11.B20TRLENS_RCP85.f09_g16.xghg.0%s.pop.h.TEMPEEP.192001-200512.nc" % i)
        f2 = nc.Dataset("b.e11.B20TRLENS_RCP85.f09_g16.xghg.0%s.pop.h.TEMPEEP.200601-208012.nc" % i)

        v1 = f1.variables["TEMPEEP"][:, :, :]
        v2 = f2.variables["TEMPEEP"][:, :, :]

        v1[v1.mask] = np.nan
        v2[v2.mask] = np.nan
        ghg_tempeep_set[i-1, :, :, :] = np.concatenate((v1, v2))

        f1.close()
        f2.close()

ghg_avg = np.average(ghg_tempeep_set, axis=0)
del ghg_tempeep_set

os.chdir("/Volumes/Extreme SSD/LE/TEMPEEP/xaer/")

aer_tempeep_set = np.zeros((20, 1932, 60, 41))
for i in range(1, 21):
    print(i)
    if i < 10:
        f1 = nc.Dataset("b.e11.B20TRLENS_RCP85.f09_g16.xaer.00%s.pop.h.TEMPEEP.192001-200512.nc" % i)
        f2 = nc.Dataset("b.e11.B20TRLENS_RCP85.f09_g16.xaer.00%s.pop.h.TEMPEEP.200601-208012.nc" % i)

        v1 = f1.variables["TEMPEEP"][:, :, :]
        v2 = f2.variables["TEMPEEP"][:, :, :]

        v1[v1.mask] = np.nan
        v2[v2.mask] = np.nan
        aer_tempeep_set[i-1, :, :, :] = np.concatenate((v1, v2))

        f1.close()
        f2.close()

    else:
        f1 = nc.Dataset("b.e11.B20TRLENS_RCP85.f09_g16.xaer.0%s.pop.h.TEMPEEP.192001-200512.nc" % i)
        f2 = nc.Dataset("b.e11.B20TRLENS_RCP85.f09_g16.xaer.0%s.pop.h.TEMPEEP.200601-208012.nc" % i)

        v1 = f1.variables["TEMPEEP"][:, :, :]
        v2 = f2.variables["TEMPEEP"][:, :, :]

        v1[v1.mask] = np.nan
        v2[v2.mask] = np.nan
        aer_tempeep_set[i-1, :, :, :] = np.concatenate((v1, v2))

        f1.close()
        f2.close()
aer_avg = np.average(aer_tempeep_set, axis=0)
del aer_tempeep_set

os.chdir("/Users/bengoldman/ENSO-amplitude/Data")
np.save("ff_tempeep_average",ff_avg)
np.save("ghg_tempeep_average", ghg_avg)
np.save("aer_tempeep_average", aer_avg)

