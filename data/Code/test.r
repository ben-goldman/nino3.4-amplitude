# a little bit of exploratory stuff on what the pacific looks like in different seasons at different times yay

library(dplyr)
library(ncdf4)
library(ggplot2)
library(reshape2)

ncin <- nc_open("/Volumes/Extreme SSD/DATA/BEN/CESM1/TEMP/b.e11.BRCP85C5CNBDRD.f09_g16.001.pop.h.TEMPDT.192001-210012.nc")

tempdt <- ncvar_get(ncin, "TEMPDT")

tempdt_melt <- tempdt[100,,seq(9, 2172, by = 12)] %>% melt
# tempdt_melt <- tempdt[,,1] %>% melt
ggplot(tempdt_melt, aes(Var2, Var1, z = value)) +
    geom_contour_filled(bins = 16)

plot(tempdt[1,1,])
