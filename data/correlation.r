library(pracma)
library(ncdf4)
library(zoo)
library(dplyr)
library(ggplot2)
library(WaveletComp)
library(reshape2)
library(abind)
library(scales)

# calculate 20-year rolling variance
rollvar <- function(x) {
  out <- rollapply(x, width = 240, FUN = var, align = "center", fill = NA)
  return(out)
}

rollmean <- function(x) {
  out <- rollapply(x, width = 12, FUN = mean, align = "center", fill = NA)
  return(out)
}

getvar <- function(x) {
    apply(x, 2, rollvar)
}

prepare <- function(x) {
    x.mean <- x %>% apply(1, mean)
    return(x - x.mean)
}

# load variance from ensemble file
load_temp <- function(file) (read.table(file, sep = ",") %>% as.matrix %>% apply(2, rollmean))

se <- function(x, ...) sd(x, ...)/sqrt(length(x))

# bind ensemble statistics into dataframe while preserving date offset
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
        this.df <- data.frame(date = this.date, mean = c(
                                                    rep(NA, date.start),
                                                    this.mean,
                                                    rep(NA, (length(this.date) - date.end))),
                              se =
                                  c(rep(NA, date.start),
                                    this.se,
                                    rep(NA, (length(this.date) - date.end))))
        writeLines(as.character(date.start))
        writeLines(as.character(date.end))
        return(this.df)
    }
}

# Produce ensemble stats dataframe
make_df <- function(this, this.date, date.start = NA, date.end = NA) {
    this.mean <- this %>% apply(1, mean)
    this.se <- this %>% apply(1, se)
    writeLines(as.character(length(this.mean)))
    this.df <- bind_stats(this.date, this.mean, this.se, date.start, date.end)
    return(this.df)
}

na_cor <- function(x, y, ...) {
    if(all(is.na(x)) || all(is.na(y))) {
        return(NA)
    } else {
        return(cor(x, y, ...))
    }
}

date1 <- seq(1920, 2100, length.out = 2172)

ff1 <- load_temp("./data/CESM1/ff.csv")
ff1_df <- make_df(ff1 %>% prepare () %>% getvar(), date1)

ncin <- nc_open("/Volumes/Extreme-SSD/DATA/stacked/CESM1/TEMP/b.e11.BRCP85C5CNBDRD.f09_g16.all.pop.h.TEMPDT.192001-210012.average.nc")

lon <- ncvar_get(ncin, "lon", start = 21, count = 121)
depth <- ncvar_get(ncin, "depth") / 100
date <- ncvar_get(ncin, "time") / 365

tempdt <- ncvar_get(ncin, "TEMPDT", start = c(21, 1, 1), count = c(121, -1, -1), verbose = TRUE)

t_melt <- tempdt[,,1] %>% melt

dimnames(tempdt) <- list(lon, depth, date)

ggplot(tempdt[,,1] %>% melt, aes(Var1, Var2, z = value)) +
    geom_contour_filled(bins = 16)

corrs <- apply(X = tempdt,
                    MARGIN = c(1, 2),
                    FUN=na_cor,
                    y = ff1_df$mean,
                    use = "complete.obs")

dimnames(corrs) <- list(lon, depth)


ggplot(corrs[,1:38] %>% melt, aes(Var1, Var2, z = value)) +
    geom_contour_filled() +
    labs(title = "Correlation Coefficient",
         x = "Longitude",
         y = "Depth (m)",
         fill = "Correlation\nCoefficient") +
    scale_color_gradientn(colors = viridis_pal()(9), limits = c(1, 1)) +
    scale_y_continuous(trans = "reverse") +
    theme(text = element_text(size = 20))

gsave <- function(name, plot = last_plot(), dimensions = c(6, 8), path = "./figures/") {
    ggsave(name, path = path, width = dimensions[1], height = dimensions[2])
}

gsave("tempdt.pdf", dimensions = c(8, 6))

