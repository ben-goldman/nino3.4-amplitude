# Imports
library(ncdf4)
library(zoo)
library(dplyr)
library(ggplot2)
library(WaveletComp)
library(reshape2)

# little bit of wavelet stuff :)
ff <- read.table("ff.csv", sep = ",") %>% apply(1, mean) %>% rollapply(width = 12, FUN = mean, align = "center")
ghg <- read.table("ghg.csv", sep = ",") %>% apply(1, mean) %>% rollapply(width = 12, FUN = mean, align = "center")
aer <- read.table("aer.csv", sep = ",") %>% apply(1, mean) %>% rollapply(width = 12, FUN = mean, align = "center")
bmb <- read.table("bmb.csv", sep = ",") %>% apply(1, mean) %>% rollapply(width = 12, FUN = mean, align = "center")
luc <- read.table("luc.csv", sep = ",") %>% apply(1, mean) %>% rollapply(width = 12, FUN = mean, align = "center")

# mydate <- read.table("mydate.csv", sep = ",")$x

mydate_1 <- seq(1920, 2100, length.out = 2172)
mydate_2 <- seq(1920, 2099, length.out = 2161)
mydate_3 <- seq(1920, 2079, length.out = 1921)

## ff_raw_mean <- read.table("ff.csv", sep = ",") %>% apply(1, mean)

## ff_rw_ts_dec <- ts(ff_raw_mean, frequency = 12) %>% decompose()
## ff_resid <- ff_rw_ts_dec$random
## ff_resid_wvlt_power <- WaveletTransform(ff_resid[7:2166])$Power %>% melt()

## ff_reg_wvlt_power <- WaveletTransform(ff_raw_mean)$Power %>% melt

## ff_resid_wvlt_power$Var1 <- (2172 / ff_resid_wvlt_power)$Var1 / 12
## ff_reg_wvlt_power$Var1 <- (2172 / ff_reg_wvlt_power$Var1) / 12

## ggplot(ff_resid_wvlt_power, aes(Var2, Var1, z = value)) +
##     geom_contour_filled() +
##     scale_y_log10()

## ggplot(ff_reg_wvlt_power, aes(Var2, Var1, z = value)) +
##     geom_contour_filled() +
##     scale_y_log10()

ff_mean <- data.frame(temp = ff, date = mydate_2)
ghg_mean <- data.frame(temp = ghg[!is.na(ghg)], date = mydate_3)

colnames(ff_mean) <- c("temp", "date")


ff_w <- analyze.wavelet(ff_mean, dt = 1/12)
ghg_w <- analyze.wavelet(ghg_mean, dt = 1/12)

ff_power <-ff_w$Power
rownames(ff_power) <- ff_w$axis.2
colnames(ff_power) <- mydate_2
ff_power <- melt(ff_power)
colnames(ff_power) <- c("Period", "Date", "Power")

ghg_power <-ghg_w$Power
rownames(ghg_power) <- ghg_w$axis.2
colnames(ghg_power) <- mydate_3
ghg_power <- melt(ghg_power)
colnames(ghg_power) <- c("Period", "Date", "Power")

ggplot(ff_power, aes(Date, Period, z = Power)) +
    geom_contour_filled()

ggplot(ghg_power, aes(Date, Period, z = Power)) +
    geom_contour_filled()

ff_power_avg <- data.frame(period = ff_w$axis.2, power = ff_w$Power.avg, pval = ff_w$Power.avg.pval)

this <- data.frame(power = (ff_w$Power %>% apply(2, mean)), period = ff_w$axis.2)

ggplot(this, aes(x = period, y = power)) +
    geom_line()



wt.image(ff_w)

wt.image(ghg_w)


wt.avg(ff_w)
