# Imports
library(ncdf4)
library(zoo)
library(dplyr)
library(ggplot2)
library(WaveletComp)
library(reshape2)
library(scales)

prepare <- function(x) {
    x.mean <- x %>% apply(1, mean)
    return(x - x.mean)
}

ff <- read.table("./data/CESM1/ff.csv", sep = ",") %>% prepare() %>% rollapply(width = 12, FUN = mean, align = "center") %>% as.matrix()
ghg <- read.table("./data/CESM1/ghg.csv", sep = ",") %>% prepare() %>% rollapply(width = 12, FUN = mean, align = "center")
aer <- read.table("./data/CESM1/aer.csv", sep = ",") %>% prepare() %>% rollapply(width = 12, FUN = mean, align = "center")
bmb <- read.table("./data/CESM1/bmb.csv", sep = ",") %>% prepare() %>% rollapply(width = 12, FUN = mean, align = "center")
luc <- read.table("./data/CESM1/luc.csv", sep = ",") %>% prepare() %>% rollapply(width = 12, FUN = mean, align = "center")


ff_mean <- ff %>% apply(1, mean) %>% as.data.frame()

ff_w_raw <- ff %>% apply(2, WaveletTransform, dt = 1/12, lowerPeriod = 1)

ff_w <- array(NA, dim = c(119, 2161, 40))
for(r in 1:40) {
    writeLines(as.character(r))
    ff_w[, , r] <- ff_w_raw[[r]]$Power
}

mydate <- seq(1920, 2099, length.out = 2161)
period <- ff_w_raw[[1]]$Period
nr <- ff_w_raw[[1]]$nr

ff_w_mean <- ff_w %>% apply(c(1, 2), mean)
dimnames(ff_w_mean) <- list(period, mydate)
ff_w_mean_melt <- ff_w_mean %>% melt(varnames = c("Period", "Date"))


gsave <- function(name, plot = last_plot(), dimensions = c(8, 6), path = "./figures/") {
    ggsave(name, path = path, width = dimensions[1], height = dimensions[2])
}

ggplot(ff_w_mean_melt, aes(Date, Period, z = value)) +
    geom_contour_filled() +
    scale_y_continuous(trans = "log2", breaks = log_breaks(n = 16, base = 2)) +
    labs(title = "Ensemble Mean of Wavelet Power Spectrum",
         x = "Date",
         y = "Period",
         fill = "Wavelet\npower")

gsave("spectrum1.pdf")




ff_w_big <- ff_w
ff_w_big[ff_w_big < 0.4] <- NA

ff_w_ts <- ff_w_big %>% apply(2, mean, na.rm = TRUE)

ff_w_ts_df <- data.frame(power = ff_w_ts, date = mydate)

ggplot(ff_w_ts_df, aes(x = date, y = power)) +
    geom_line()
