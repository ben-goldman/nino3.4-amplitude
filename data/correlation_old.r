library(ncdf4)
library(zoo)
library(dplyr)
library(ggplot2)
library(WaveletComp)
library(reshape2)
library(abind)

# subtract ensemble mean from member
prepare <- function(x) {
    x.mean <- x %>% apply(1, mean)
    return(x - x.mean)
}

# calculate 20-year rolling variance
rollvar <- function(x) {
  out <- rollapply(x, width = 240, FUN = var, align = "center", fill = NA)
  return(out)
}

# load variance from ensemble file
load_variance <- function(file) (read.table(file, sep = ",") %>% as.matrix %>% apply(2, rollvar))

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

ncin <- nc_open("/Volumes/Extreme SSD/DATA/stacked/CESM1/TEMP/b.e11.BRCP85C5CNBDRD.f09_g16.all.pop.h.TEMPDT.192001-210012.nc")
lon <- ncvar_get(ncin, "lon", start = 21, count = 121)
depth <- ncvar_get(ncin, "depth") / 100
date <- ncvar_get(ncin, "time") / 365

tempdt <- ncvar_get(ncin, "TEMPDT", start = c(21, 1, 1, 1), count = c(121, -1, -1, 40), verbose = TRUE)

t_melt <- tempdt[,,1,1] %>% melt

record <- c(1:40)

dimnames(tempdt) <- list(lon, depth, date, record)

ggplot(tempdt[,,1,1] %>% melt, aes(Var1, Var2, z = value)) +
    geom_contour_filled(bins = 16)

nino_var <- load_variance("./data/CESM1/ff.csv")

corrs <- array(NA, dim = dim(tempdt)[c(1, 2, 4)])
for(r in 1:dim(tempdt)[4]) {
    corrs[,,r] <- apply(X = tempdt[,,,r],
                        MARGIN = c(1, 2),
                        FUN=na_cor,
                        y = nino_var[,r],
                        use = "complete.obs")
    writeLines(as.character(r))
}

dimnames(corrs) <- list(lon, depth, record)

corrs_mean <- apply(corrs, c(1, 2), mean)
dimnames(corrs_mean) <- list(lon, depth)

ggplot(corrs_mean %>% melt, aes(Var1, log(Var2, base = 10), z = value)) +
    geom_contour_filled(bins = 20) +
    labs(title = "Correlation Coefficient Between Niño 3.4 Variance and Ocean Temperature",
         x = "Longitude",
         y = "log_10(Depth)",
         fill = "Correlation\nCoefficient") +
    scale_y_continuous(trans = "reverse")

gsave <- function(name, plot = last_plot(), dimensions = c(6, 8), path = "./figures/") {
    ggsave(name, path = path, width = dimensions[1], height = dimensions[2])
}

gsave("tempdt.pdf", dimensions = c(8, 6))

# Calculate TEMPDT ensemble mean
# TAKES A VERY LONG TIME!!! BE CAREFUL!!!!!!
base <- array(NA, dim = c(121, 60, 2172))
for(r in 1:40) {
    writeLines(as.character(r))
    if(r == 1) {
        base <- tempdt[,,,1]
    } else {
        base <- apply(abind(base, tempdt[,,,r], along = 4), c(1, 2, 3), mean)
    }
}

write.csv(base, "/Volumes/Extreme SSD/DATA/stacked/CESM1/tempdt_mean.csv", row.names = FALSE)

ggplot(base[,,1] %>% melt, aes(Var1, Var2, z = value)) +
    geom_contour_filled(bins = 16)

tempdt_diff <- array(NA, dim = dim(tempdt))
for(r in 1:40) {
    writeLines(as.character(r))
    tempdt_diff[,,,r] <- tempdt[,,,r] - base
}

load_variance_diff <- function(file) (read.table(file, sep = ",") %>% as.matrix %>% prepare() %>% apply(2, rollvar))

nino_var_diff <- load_variance_diff("./data/CESM1/ff.csv")

corrs_diff <- array(NA, dim = dim(tempdt_diff)[c(1, 2, 4)])
for(r in 1:dim(tempdt_diff)[4]) {
    corrs_diff[,,r] <- apply(X = tempdt_diff[,,,r],
                        MARGIN = c(1, 2),
                        FUN=na_cor,
                        y = nino_var_diff[,r],
                        use = "complete.obs")
    writeLines(as.character(r))
}

corrs_mean_diff <- apply(corrs_diff, c(1, 2), mean)
dimnames(corrs_mean_diff) <- list(lon, depth)

ggplot(corrs_mean_diff %>% melt, aes(Var1, log(Var2, base = 10), z = value)) +
    geom_contour_filled(bins = 20) +
    labs(title = "Correlation Coefficient Between Niño 3.4 Variance and Ocean Temperature",
         x = "Longitude",
         y = "log_10(Depth)",
         fill = "Correlation\nCoefficient") +
    scale_y_continuous(trans = "reverse")

gsave("tempdt_diff.pdf", dimensions = c(8, 6))
