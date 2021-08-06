library(ncdf4)
library(zoo)
library(dplyr)
library(ggplot2)
library(reshape2)

ncin <- nc_open("/Volumes/Extreme SSD/DATA/HadISST_sst.nc")

sst <- ncvar_get(ncin, "sst")
sst[sst == -1000] <- NA

lat <- ncvar_get(ncin, "latitude")
lon <- ncvar_get(ncin, "longitude")

rownames(sst) <- lon
colnames(sst) <- lat

sst_wrap <- array(NA, dim = dim(sst))
## lon_wrap <- rep(NA, times = length(lon))
## lon_wrap[0:211] <- lon[150:360]
## lon_wrap[212:360] <- lon[1:149]
lon_wrap <- lon + 180
sst_wrap[0:180,,] <- sst[181:360,,]
sst_wrap[181:360,,] <- sst[1:180,,]
rownames(sst_wrap) <- lon_wrap
colnames(sst_wrap) <- lat

## NEED TO MAKE ANOMALY PLOT!

sst_example <- apply(sst_wrap[,,1356:1360], c(1, 2), mean)
sst_example2 <- apply(sst_wrap[,,1359 + 24 :1360 + 24], c(1, 2), mean)

sst_melt <- sst_example2 %>% melt(varnames = c("longitude", "latitude"))
ggplot(sst_melt %>% filter(latitude < 50 &
                           latitude > -50 &
                           longitude > 50 &
                           longitude < 300), aes(longitude, latitude, z = value)) +
    geom_contour_filled(bins = 16)

#  %>% filter(latitude < 20 & latitude > -20),
