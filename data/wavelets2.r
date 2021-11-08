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

se <- function(x, ...) sd(x, ...)/sqrt(length(x))

wavelet_ensemble <- function(x) {
    wv_raw <- x %>% apply(2, WaveletTransform, dt = 1/12, lowerPeriod = 1)
    nr <- wv_raw[[1]]$nr
    t <- dim(x)[1]
    n <- dim(x)[2]
    pwr <- array(NA, dim = c(nr, t, n))
    writeLines(as.character(dim(pwr)))
    for(r in 1:n) {
        writeLines(as.character(r))
        pwr[,,r] <- wv_raw[[r]]$Power
    }
    return(pwr)
}

bind_stats <- function(this.date, this.mean, this.se, date.start = NA, date.end = NA) {
    if(length(this.mean) == length(this.date)) {
        this.df <- data.frame(date = this.date, mean = this.mean, se = this.se)
    } else {
        if(is.na(date.end)){
            date.end <- length(this.date)
        }
        if(is.na(date.start)){
            date.start <- 0
        }
        this.df <- data.frame(date = this.date, mean = c(rep(NA, date.start),
                                                         this.mean,
                                                         rep(NA, (length(this.date) - date.end))),
                              se = c(rep(NA, date.start),
                                     this.se,
                                     rep(NA, (length(this.date) - date.end))))
        writeLines(as.character(date.start))
        writeLines(as.character(date.end))
        return(this.df)
    }
}

make_df <- function(this, this.date, date.start = NA, date.end = NA) {
    this.mean <- this %>% apply(1, mean)
    this.se <- this %>% apply(1, se)
    writeLines(as.character(length(this.mean)))
    this.df <- bind_stats(this.date, this.mean, this.se, date.start, date.end)
    return(this.df)
}

l <- 0.2
m <- 0.5
d <- 0.8

ff1 <- read.table("./data/CESM1/ff.csv", sep = ",") %>% prepare() %>% rollapply(width = 12, FUN = mean, align = "center") %>% as.matrix()

ff1_pwr <- wavelet_ensemble(ff1)

ff1_period <- WaveletTransform(ff1[,8], dt = 1/12, lowerPeriod = 1)$Period

mydate1 <- seq(1920, 2099, length.out = 2161)

ff1_w_mean <- ff1_pwr %>% apply(c(1, 2), mean)
dimnames(ff1_w_mean) <- list(ff1_period, mydate1)
ff1_w_mean_melt <- ff1_w_mean %>% melt(varnames = c("Period", "Date"))


ff2 <- read.table("./data/CESM2/ff.csv", sep = ",") %>% prepare() %>% rollapply(width = 12, FUN = mean, align = "center") %>% as.matrix()

ff2_pwr <- wavelet_ensemble(ff2)

ff2_period <- WaveletTransform(ff2[,8], dt = 1/12, lowerPeriod = 1)$Period

mydate2 <- seq(1850, 2099, length.out = 3001)

ff2_w_mean <- ff2_pwr %>% apply(c(1, 2), mean)
dimnames(ff2_w_mean) <- list(ff2_period, mydate2)
ff2_w_mean_melt <- ff2_w_mean %>% melt(varnames = c("Period", "Date"))


gsave <- function(name, plot = last_plot(), dimensions = c(8, 6), path = "./figures/") {
    ggsave(name, path = path, width = dimensions[1], height = dimensions[2])
}

ff_comb_melt <- ff1_w_mean_melt  %>% mutate(case = "CESM1") %>%
    bind_rows(ff2_w_mean_melt %>% mutate(case = "CESM2"))

ggplot(ff_comb_melt, aes(Date, Period, z = value)) +
    geom_contour_filled(bins = 10) +
    scale_y_continuous(trans = "log2", breaks = log_breaks(n = 16, base = 2)) +
    labs(title = "Ensemble Mean of Wavelet Power Spectrum",
         x = "Date",
         y = "Period (Years)",
         fill = "Wavelet\npower") +
    facet_wrap(vars(case), dir = "v", scales = "free") +
    theme(text = element_text(size = 20))
gsave("wavelet2.pdf")

ff1_low <- ff1_pwr[21:33, ,] %>% apply(c(2, 3), mean) %>% make_df(mydate1, date.start = 840)
ff1_high <- ff1_pwr[34:61, ,] %>% apply(c(2, 3), mean) %>% make_df(mydate1, date.start = 840)

ff2_low <- ff2_pwr[21:33, ,] %>% apply(c(2, 3), mean) %>% make_df(mydate2, date.start = 840)
ff2_high <- ff2_pwr[34:61, ,] %>% apply(c(2, 3), mean) %>% make_df(mydate2, date.start = 840)

ff_stuff <- ff1_low %>% as.data.frame() %>% mutate(ensemble = "CESM1", group = "T < 3") %>%
    bind_rows(ff1_high %>% as.data.frame() %>% mutate(ensemble = "CESM1", group = "T > 3")) %>%
    bind_rows(ff2_low %>% as.data.frame() %>% mutate(ensemble = "CESM2", group = "T < 3")) %>%
    bind_rows(ff2_high %>% as.data.frame() %>% mutate(ensemble = "CESM2", group = "T > 3"))

ggplot(ff_stuff, aes(y = mean, x = date, color = group, fill = group, ymin = (mean - 2 * se), ymax = (mean + 2 * se))) +
    geom_line() +
    geom_ribbon(alpha = l, color = NA) +
    facet_wrap(vars(ensemble), dir = "v") +
    labs(title = "Mean Wavelet Power", x = "Date", y = "Power", color = "Period", fill = "Period") +
    theme(text = element_text(size = 20))
gsave("wavelet3.pdf")
