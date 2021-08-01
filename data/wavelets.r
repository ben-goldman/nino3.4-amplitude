# Imports
library(ncdf4)
library(zoo)
library(dplyr)
library(ggplot2)
library(WaveletComp)
library(reshape2)

# get dato from file, apply 1 year rolling average to remove seasonality and calculate ensemble means
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

# pair ensemble means with date vectors
ff_mean <- data.frame(temp = ff, date = mydate_2)
ghg_mean <- data.frame(temp = ghg[!is.na(ghg)], date = mydate_3)

colnames(ff_mean) <- c("temp", "date")

# perform wavelet analysis
ff_w <- analyze.wavelet(ff_mean, dt = 1/12)
ghg_w <- analyze.wavelet(ghg_mean, dt = 1/12)

# prepare ff power for plotting, set axes
ff_power_mat <-ff_w$Power
ff_power_p_mat <- ff_w$Power.pval
rownames(ff_power_mat) <- ff_w$Period
colnames(ff_power_mat) <- mydate_2
rownames(ff_power_p_mat) <- ff_w$axis.2
colnames(ff_power_p_mat) <- mydate_2
ff_power <- melt(ff_power_mat)
colnames(ff_power) <- c("Period", "Date", "Power")

# extract sliced data by p < alpha timewise
getsig <- function(data, p, alpha) {
    if(length(data) != length(p))
        return(0)
    else {
        cat(length(data[p < alpha]))
        cat("\n")
        return(mean(data[p < alpha]))
    }
}

# get ff enso? signal by getting ff wavelet power where p = 0.0
ff_sig <- rep(NA, times = 2161)
for (i in c(1:dim(ff_power_mat)[2])){
    ff_sig[i] <- getsig(ff_power_mat[,i], ff_power_p_mat[,i], 0.005)
}

# get ff enso? signal by getting ff wavelet power where 1.5 < log2(period) < 2.5 (ie fourier period is between 2.8 and 5.6 identified by inspection of power spectrum)
ff_nino_thingy <- apply(ff_power_mat[83:104,], 2, mean)

ghg_power <-ghg_w$Power
rownames(ghg_power) <- ghg_w$axis.2
colnames(ghg_power) <- mydate_3
ghg_power <- melt(ghg_power)
colnames(ghg_power) <- c("Period", "Date", "Power")

ggplot(ff_power, aes(Date, Period, z = log(Power))) +
    geom_contour_filled(bins = 5)

ggplot((ff_power_mat %>% melt()), aes(Var1, Var2, z = log(value))) +
    geom_contour_filled(bins = 10)

ggplot((ff_power_p_mat %>% melt()), aes(Var1, Var2, z = log(value))) +
    geom_contour_filled(bins = 5)

hist(ff_power_mat)
hist(log(ff_power_mat))

ggplot(ghg_power, aes(Date, Period, z = Power)) +
    geom_contour_filled()

ff_power_avg <- data.frame(period = ff_w$Period, power = ff_w$Power.avg, pval = ff_w$Power.avg.pval)

## this <- data.frame(power = (ff_w$Power %>% apply(2, mean)), period = ff_w$axis.2)

ggplot(ff_power_avg %>% filter(period < 20), aes(x = period, y = power)) +
    geom_line()



wt.image(ff_w)

wt.image(ghg_w)


wt.avg(ff_w)
