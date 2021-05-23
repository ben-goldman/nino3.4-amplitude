from helpers import *

import cartopy.crs as ccrs
import cartopy
import matplotlib.patches as mpatches

fig = plt.figure(figsize=(4, 4))
ax = fig.add_subplot(projection=ccrs.PlateCarree(central_longitude=180))
ax.coastlines()
ax.gridlines()
ax.add_patch(mpatches.Rectangle(xy=[-170, -5], width=50, height=10, color="C0", transform=ccrs.PlateCarree()))
ax.set_xlim((-75, 100))
ax.set_ylim((-80, 80))
plt.tight_layout()
plt.savefig("../Figures/nino.pdf")

