from helpers import *
from variance import ff_var_set

# %%
os.chdir("/Volumes/Extreme SSD/LE/TEMPDT/ff")
ff = get_ensemble(0, "TEMPDT", 2172)
ff_correlation = np.zeros((34, 60, 180))

# %%
correlation = list(map(lambda x, y, z: correlation_detrended(ff_var_set[x, y, z], ff_var_set), ff))
