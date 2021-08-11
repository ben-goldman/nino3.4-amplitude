library(ncdf4)
library(zoo)
library(dplyr)
library(ggplot2)
library(WaveletComp)
library(reshape2)

ncin <- nc_open("/Volumes/Extreme SSD/DATA/stacked/CESM1/TEMP/b.e11.BRCP85C5CNBDRD.f09_g16.all.pop.h.TEMPDT.192001-210012.nc")
tempdt <- ncvar_get(ncin, "TEMPDT", start = c(21, 1, 1, 1), count = c(121, -1, -1, 1))
lon <- ncvar_get(ncin, "lon", start = 21, count = 121)
depth <- ncvar_get(ncin, "depth") / 100
date <- ncvar_get(ncin, "time") / 365

woohoo <- ncvar_get(ncin, "TEMPDT", start = c(21, 1, 1, 1), count = c(1, 1, -1, -1))

dimnames(tempdt) <- list(lon, depth, date)

ggplot(tempdt[,,4] %>% melt, aes(Var1, log(Var2), z = value)) +
    geom_contour_filled(bins = 16)
